import sys
import subprocess
import json
import os
import re

# --- CONFIGURACIÓN ---
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST_PATH = os.path.join(ROOT_DIR, "docs", "manifest.json")

# Mapa de Prefijos de Ticket -> Conventional Commit Type
TYPE_MAP = {
    "TASK": "feat",     # Nueva funcionalidad
    "FEAT": "feat",
    "FIX": "fix",       # Bug fix
    "BUG": "fix",
    "HOTFIX": "fix",
    "INFRA": "chore",   # Configuración, herramientas
    "CHORE": "chore",
    "DEF": "docs",      # Definición / Documentación
    "DOC": "docs",
    "DOCS": "docs",
    "TEST": "test",     # Tests
    "PERF": "perf",     # Rendimiento
    "REF": "refactor",  # Refactorización
    "STYLE": "style",   # Formato
    "CI": "ci",         # CI/CD
    "BUILD": "build"    # Build system
}

def get_active_ticket():
    """Lee el ticket activo del manifest v3.0"""
    try:
        with open(MANIFEST_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('workflow', {}).get('active_ticket')
    except:
        return None

def get_staged_files():
    """Obtiene la lista de archivos en el área de preparación (staged)"""
    try:
        # git diff --cached muestra lo que se va a commitear
        output = subprocess.check_output(
            ["git", "diff", "--name-only", "--cached"],
            stderr=subprocess.DEVNULL
        ).decode("utf-8")
        return [f.strip() for f in output.splitlines() if f.strip()]
    except:
        return []

def detect_scope(files):
    """
    Analiza la topología del proyecto para determinar el alcance (scope).
    Prioridad: Features > Core > App > Tools > Build > Docs
    """
    if not files: return "global"

    scopes = set()

    for f in files:
        # 1. Features (features/library -> library)
        if f.startswith("features/"):
            try:
                # features/nombre_modulo/...
                module = f.split("/")[1]
                scopes.add(module)
            except:
                scopes.add("features")

        # 2. Core (core/database -> database)
        elif f.startswith("core/"):
            try:
                module = f.split("/")[1]
                scopes.add(module)
            except:
                scopes.add("core")

        # 3. App Main
        elif f.startswith("app/"):
            scopes.add("app")

        # 4. Herramientas y Scripts
        elif f.startswith("tools/"):
            scopes.add("tools")

        # 5. Documentación
        elif f.startswith("docs/") or f.endswith(".md"):
            scopes.add("docs")

        # 6. Build System
        elif f.endswith(".gradle.kts") or f.endswith(".toml") or f.startswith("gradle/"):
            scopes.add("build")

        # 7. Configuración Raíz
        elif f in [".gitignore", "local.properties", "gradle.properties"]:
            scopes.add("config")

    # Lógica de decisión
    if len(scopes) == 0:
        return "root"
    elif len(scopes) == 1:
        return list(scopes)[0]
    else:
        # Si hay mezcla, pero una es 'docs' o 'build' y la otra es código, priorizamos código?
        # Por ahora, ser honestos: es mixed.
        sorted_scopes = sorted(list(scopes))
        return f"mixed" # Opcional: return "+".join(sorted_scopes[:2]) para ser más descriptivo

def determine_type(ticket_id, detected_scope):
    """Decide el tipo de commit basado en el ticket o en los archivos"""

    # 1. Si hay ticket, el ticket manda (casi siempre)
    if ticket_id:
        prefix = ticket_id.split("-")[0].upper()
        return TYPE_MAP.get(prefix, "feat") # Default a feat si no reconoce el prefijo

    # 2. Si NO hay ticket (hotfix rápido o docs), deducir por archivos
    if detected_scope == "docs": return "docs"
    if detected_scope == "build": return "build"
    if detected_scope == "tools": return "chore"
    if detected_scope == "config": return "chore"

    # 3. Fallback genérico
    return "feat"

def main():
    # El argumento 1 es la ruta al archivo temporal del mensaje de commit
    try:
        commit_msg_filepath = sys.argv[1]
    except IndexError:
        return # No se llamó como hook

    ticket = get_active_ticket()
    files = get_staged_files()

    # Análisis inteligente
    scope = detect_scope(files)

    # Datos del ticket
    ticket_id = ticket['id'] if ticket else ""
    ticket_title = ticket['title'] if ticket else ""

    # Determinar tipo
    msg_type = determine_type(ticket_id, scope)

    # Construir el sufijo del ID
    suffix = f" [{ticket_id}]" if ticket_id else ""

    # Construir la línea de asunto (Header)
    # Formato: type(scope): [ID]
    header = f"{msg_type}({scope}): {suffix}"

    # Preparar el contenido a inyectar
    # Leemos el contenido original (puede ser un merge message o nada)
    with open(commit_msg_filepath, 'r+', encoding='utf-8') as f:
        original_content = f.read()
        f.seek(0, 0)

        # Inyectamos encabezado y recordatorio
        f.write(f"{header}\n")
        if ticket_title:
            f.write(f"\n# 🎯 TAREA ACTIVA: {ticket_title}")
            f.write(f"\n# 📂 ARCHIVOS: {len(files)} modificados en scope '{scope}'")

        f.write(f"\n\n{original_content}")

if __name__ == "__main__":
    main()