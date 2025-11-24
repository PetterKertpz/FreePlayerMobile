import json
import os
import subprocess
import sys

# --- CONFIGURACIÓN DE RUTAS ---
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST_PATH = os.path.join(ROOT_DIR, "docs", "manifest.json")
SNAPSHOT_SCRIPT = os.path.join(ROOT_DIR, "tools", "gen_snapshot.py")
SNAPSHOT_FILE = os.path.join(ROOT_DIR, "tools", "ai_context", "snapshot.txt")
PROMPTS_DIR = os.path.join(ROOT_DIR, "tools", "ai_prompts")
OUTPUT_FILE = os.path.join(ROOT_DIR, "PROMPT_READY.txt")

# --- MAPA DE PLANTILLAS INTELIGENTE v5.0 ---
PROMPT_MAP = {
    # ==========================================
    # FASE 0: DEFINICIÓN (Specs & JSON)
    # ==========================================
    "vision": "def_1_vision.md",
    "business": "def_1_vision.md",
    "logic": "def_1_vision.md",

    "ui": "def_2_ui.md",
    "ux": "def_2_ui.md",
    "visual": "def_2_ui.md", # Definición escrita/JSON

    "data": "def_3_data.md",
    "schema": "def_3_data.md",

    "roadmap": "def_4_roadmap.md", # El plan maestro inicial
    "adr": "3_adrs_generator.md",
    "decision": "3_adrs_generator.md",
    # ==========================================
    # VISUALIZACIÓN (Diagramas - Todo al Master)
    # ==========================================
    "viz": "viz_master.md",
    "diagram": "viz_master.md",
    "draw": "viz_master.md",
    "chart": "viz_master.md",

    # Redirecciones de legado (para que no fallen si usas nombres viejos)
    "viz_biz": "viz_master.md",
    "viz_nav": "viz_master.md",
    "viz_erd": "viz_master.md",

    # ==========================================
    # FASE 1+: DESARROLLO TÉCNICO
    # ==========================================
    # Estructura & Configuración
    "arch": "2_gemini_arch_code.md",
    "gradle": "2_gemini_arch_code.md",
    "hilt": "2_gemini_arch_code.md",
    "di": "2_gemini_arch_code.md",

    # Datos & Backend Local
    "database": "5_data_layer_impl.md",
    "room": "5_data_layer_impl.md",
    "dao": "5_data_layer_impl.md",
    "entity": "5_data_layer_impl.md",

    # Frontend & UI
    "screen": "6_ui_component.md",
    "compose": "6_ui_component.md",
    "viewmodel": "6_ui_component.md",

    # ==========================================
    # GESTIÓN & DOCUMENTACIÓN
    # ==========================================
    "doc": "doc_tech_writer.md",
    "readme": "doc_tech_writer.md",

    # Planificación Recurrente (Sprints)
    "plan": "1_claude_sprint_spec.md",
    "sprint": "1_claude_sprint_spec.md"
}

def load_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return f"[ERROR: No se pudo leer {path}]"

def load_manifest():
    try:
        with open(MANIFEST_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return None

def refresh_snapshot():
    print("📸 Actualizando Snapshot...")
    # Usamos sys.executable para garantizar compatibilidad con entorno portable
    subprocess.call([sys.executable, SNAPSHOT_SCRIPT])

def save_to_file(text):
    """Método infalible: Guardar en disco"""
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write(text)
        return True
    except Exception as e:
        print(f"❌ Error crítico escribiendo archivo: {e}")
        return False

def try_clipboard(text):
    """Intenta copiar al portapapeles con múltiples estrategias"""

    # INTENTO 1: Ruta Absoluta a clip.exe (Windows System32)
    clip_path = r"C:\Windows\System32\clip.exe"
    if os.path.exists(clip_path):
        try:
            process = subprocess.Popen(clip_path, stdin=subprocess.PIPE, shell=False, stderr=subprocess.DEVNULL)
            process.communicate(input=text.encode('utf-16le'))
            if process.returncode == 0:
                print("📋 ¡Prompt copiado al portapapeles (vía clip.exe)!")
                return True
        except:
            pass

    # INTENTO 2: PowerShell
    try:
        cmd = ["powershell", "-command", "$input | Set-Clipboard"]
        process = subprocess.Popen(cmd, stdin=subprocess.PIPE, shell=True, stderr=subprocess.DEVNULL)
        process.communicate(input=text.encode('utf-8'))
        if process.returncode == 0:
            print("📋 ¡Prompt copiado al portapapeles (vía PowerShell)!")
            return True
    except:
        pass

    return False

def detect_template(ticket_id, ticket_title):
    """Selecciona la plantilla basada en ID o Título"""
    # 1. Prioridad por ID (Para Fase 0)
    if "DEF-" in ticket_id:
        if "001" in ticket_id: return "def_1_vision.md"
        if "002" in ticket_id: return "def_2_ui.md"
        if "003" in ticket_id: return "def_3_data.md"
        if "004" in ticket_id: return "def_4_roadmap.md"

    # 2. Búsqueda por palabras clave en título
    title_lower = ticket_title.lower()
    for key, val in PROMPT_MAP.items():
        if key in title_lower:
            return val

    # 3. Default Genérico
    return "2_gemini_arch_code.md"

def generate_prompt(mode):
    refresh_snapshot()
    snapshot = load_file(SNAPSHOT_FILE)
    manifest = load_manifest()

    # --- MODO PLANIFICACIÓN (Generar Sprints) ---
    if mode == "plan":
        template_path = os.path.join(PROMPTS_DIR, "1_claude_sprint_spec.md")
        if not os.path.exists(template_path):
            # Fallback si no existe el archivo de prompt de planificación
            template_content = "ACTÚA COMO PROJECT MANAGER. PLANIFICA EL SIGUIENTE SPRINT."
        else:
            template_content = load_file(template_path)

        current_phase = manifest.get('context', {}).get('current_phase', 'Unknown Phase')

        # INSTRUCCIÓN JSON CRÍTICA PARA AUTOMATIZACIÓN
        json_instruction = """
==============================================================================
🔴 REQUISITO DE SALIDA OBLIGATORIO (PARA AUTOMATIZACIÓN) 🔴
Al final de tu respuesta, DEBES incluir un bloque de código JSON parseable 
con este formato exacto. NO agregues comentarios dentro del JSON.

```json
{
  "phase": "NOMBRE_FASE_ACTUAL",
  "sprint_name": "Sprint X: Titulo",
  "tasks": [
    { 
      "id": "ID-001", 
      "title": "Titulo descriptivo de la tarea", 
      "type": "feat", 
      "priority": "HIGH" 
    },
    { 
      "id": "ID-002", 
      "title": "Titulo tarea 2", 
      "type": "test", 
      "priority": "MEDIUM" 
    }
  ]
}