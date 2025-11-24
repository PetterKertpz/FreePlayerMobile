import os
import json
import subprocess
from datetime import datetime

# Rutas
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST_PATH = os.path.join(PROJECT_ROOT, "docs", "manifest.json")
RULES_PATH = os.path.join(PROJECT_ROOT, "docs", "GLOBAL_RULES.md")
OUTPUT_PATH = os.path.join(PROJECT_ROOT, "tools", "ai_context", "snapshot.txt")

def run_command(command):
    try:
        return subprocess.check_output(command, shell=True).decode('utf-8').strip()
    except:
        return "Git info unavailable"

def get_project_structure():
    # Versión compatible Windows sin grep
    raw = run_command("git ls-tree -r HEAD --name-only")
    if "unavailable" in raw: return "No files tracked yet."

    lines = raw.splitlines()
    # Filtro inteligente para no ensuciar el contexto
    filtered = [l for l in lines if not any(x in l for x in ['gradle/wrapper', 'tools/', '.idea', 'gradlew'])]
    return "\n".join(filtered)

def main():
    print("📸 Generando Snapshot Inteligente v3...")

    manifest_data = {}
    if os.path.exists(MANIFEST_PATH):
        with open(MANIFEST_PATH, 'r', encoding='utf-8') as f:
            manifest_data = json.load(f)

    # Extraer gobernanza para inyectarla como texto plano (ahorra tokens a la IA)
    tech_stack = "Unknown"
    active_task = "None"

    if 'governance' in manifest_data:
        tech_stack = json.dumps(manifest_data['governance']['tech_stack'], indent=2)

    if 'workflow' in manifest_data and manifest_data['workflow']['active_ticket']:
        t = manifest_data['workflow']['active_ticket']
        active_task = f"[{t['id']}] {t['title']} ({t['type']})"

    commits = run_command('git log -n 5 --pretty=format:"%h - %s (%ar)"')
    files = get_project_structure()

    snapshot_content = f"""
==============================================================================
🧠 CONTEXTO PROYECTO: {manifest_data.get('meta', {}).get('project_name', 'Unknown')}
📅 SNAPSHOT: {datetime.now().isoformat()}
🎯 TAREA ACTIVA: {active_task}
==============================================================================

--- 1. STACK TECNOLÓGICO (OBLIGATORIO) ---
{tech_stack}

--- 2. ESTADO COMPLETO (MANIFEST) ---
{json.dumps(manifest_data, indent=2)}

--- 3. ESTRUCTURA DE ARCHIVOS ---
{files}

--- 4. HISTORIAL RECIENTE ---
{commits}

==============================================================================
INSTRUCCIONES DEL SISTEMA:
1. Estás trabajando en la TAREA ACTIVA. No te desvíes.
2. Respeta estrictamente el STACK TECNOLÓGICO (Kotlin 2.x, Compose, Hilt).
3. Si el manifest dice que un módulo está vacío, ASUME que debes crearlo.
==============================================================================
"""

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write(snapshot_content)

    print(f"✅ Snapshot actualizado en: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()