import json
import sys
import os
import re
from datetime import datetime

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST_PATH = os.path.join(ROOT_DIR, "docs", "manifest.json")

def load_manifest():
    try:
        with open(MANIFEST_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except: return None

def save_manifest(data):
    try:
        with open(MANIFEST_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        return True
    except: return False

def extract_json_from_text(text):
    """Busca un bloque de código JSON dentro de la respuesta de Claude"""
    # Intenta encontrar bloques ```json ... ```
    match = re.search(r'```json\s*(\{.*?\})\s*```', text, re.DOTALL)
    if match:
        return json.loads(match.group(1))

    # Si no hay bloques, intenta parsear todo el texto si parece JSON
    try:
        return json.loads(text)
    except:
        return None

def import_sprint_plan(file_path):
    # 1. Leer el archivo con la respuesta de Claude (o input directo)
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        print(f"❌ No pude leer el archivo: {file_path}")
        return

    # 2. Extraer el JSON del plan
    plan_data = extract_json_from_text(content)
    if not plan_data:
        print("❌ No encontré un bloque JSON válido en el archivo.")
        return

    # 3. Validar estructura mínima
    if 'sprint_name' not in plan_data or 'tasks' not in plan_data:
        print("❌ El JSON no tiene el formato esperado ('sprint_name', 'tasks').")
        return

    # 4. Actualizar Manifiesto
    manifest = load_manifest()
    if not manifest: return

    # Respaldar tareas pendientes actuales si las hay
    current_queue = manifest['workflow']['queue']
    if current_queue:
        print(f"⚠️  Advertencia: La cola actual tenía {len(current_queue)} tareas. Se moverán al final.")

    # Actualizar Contexto
    manifest['context']['current_sprint'] = plan_data['sprint_name']
    if 'phase' in plan_data:
        manifest['context']['current_phase'] = plan_data['phase']

    # Reemplazar/Llenar la cola
    new_queue = plan_data['tasks']
    # Asegurar formato correcto de tareas
    formatted_queue = []
    for t in new_queue:
        formatted_queue.append({
            "id": t.get('id'),
            "title": t.get('title'),
            "type": t.get('type', 'feat'),
            "priority": t.get('priority', 'MEDIUM')
        })

    # Fusionar: Nuevas primero, viejas después (o reemplazar según prefieras)
    manifest['workflow']['queue'] = formatted_queue + current_queue

    # Resetear estado
    manifest['workflow']['active_ticket'] = None
    manifest['meta']['last_updated'] = datetime.now().isoformat()

    if save_manifest(manifest):
        print(f"✅ PLAN IMPORTADO EXITOSAMENTE: {plan_data['sprint_name']}")
        print(f"🚀 {len(formatted_queue)} tareas añadidas a la cola.")
        print("💡 Usa 'python tools/pm.py start <ID>' para comenzar.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python tools/import_plan.py <archivo_respuesta_claude.md>")
    else:
        import_sprint_plan(sys.argv[1])