import os
import json
import subprocess
from datetime import datetime

# CONFIGURACIÓN DE RUTAS
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST_PATH = os.path.join(PROJECT_ROOT, "docs", "manifest.json")
RULES_PATH = os.path.join(PROJECT_ROOT, "docs", "GLOBAL_RULES.md")
OUTPUT_PATH = os.path.join(PROJECT_ROOT, "tools", "ai_context", "snapshot.txt")

def run_command(command):
    try:
        return subprocess.check_output(command, shell=True).decode('utf-8').strip()
    except:
        return "unknown"

def read_file(path):
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    return f"[ARCHIVO NO ENCONTRADO: {path}]"

def main():
    print(f"🚀 Generando Snapshot de Contexto para FreePlayerM...")

    # 1. Obtener info de Git
    branch = run_command("git rev-parse --abbrev-ref HEAD")
    commit = run_command("git rev-parse --short HEAD")
    last_log = run_command("git log -1 --pretty=%B")

    # 2. Leer archivos de gobernanza
    manifest = read_file(MANIFEST_PATH)
    rules = read_file(RULES_PATH)

    # 3. Estructura del árbol de archivos (ignora .git, build, etc)
    tree_structure = run_command("git ls-tree -r HEAD --name-only")
    if "fatal" in tree_structure: # Si no hay commits aún
        tree_structure = "Repositorio nuevo - Sin estructura git trackeada aún."

    # 4. Construir el Prompt de Contexto
    content = f"""
==============================================================================
🤖 CONTEXTO INMUTABLE DEL PROYECTO: FreePlayerM
📅 FECHA: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
🌿 GIT: {branch} @ {commit}
==============================================================================

--- 1. REGLAS GLOBALES (GLOBAL_RULES.md) ---
{rules}

--- 2. ESTADO ACTUAL (manifest.json) ---
{manifest}

--- 3. ESTRUCTURA DE ARCHIVOS ---
{tree_structure}

--- 4. ÚLTIMO CAMBIO ---
{last_log}

==============================================================================
INSTRUCCIONES PARA LA IA:
1. Este es el ESTADO ACTUAL y VERDADERO del proyecto.
2. No asumas la existencia de archivos que no están en la lista de estructura.
3. Sigue estrictamente las REGLAS GLOBALES.
==============================================================================
"""

    # 5. Guardar
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ SNAPSHOT GENERADO: {OUTPUT_PATH}")
    print("📋 Copia el contenido de este archivo al inicio de cada chat.")

if __name__ == "__main__":
    main()