import json
import sys
import os
from datetime import datetime

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST_PATH = os.path.join(ROOT_DIR, "docs", "manifest.json")

# Palabras clave que activan el cierre automático
CLOSING_KEYWORDS = ["finish", "close", "complete", "done", "release"]

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

def start_ticket(ticket_id):
    data = load_manifest()
    if not data: return

    queue = data.get('workflow', {}).get('queue', [])
    found_ticket = next((t for t in queue if ticket_id.upper() in t['id']), None)

    if found_ticket:
        if data['workflow'].get('active_ticket'):
            # Devolver el actual a la cola
            old = data['workflow']['active_ticket']
            if 'started_at' in old: del old['started_at']
            queue.insert(0, old)

        queue.remove(found_ticket)
        found_ticket['started_at'] = datetime.now().isoformat()
        data['workflow']['active_ticket'] = found_ticket
        data['meta']['last_updated'] = datetime.now().isoformat()
        data['context']['health_status'] = "WORKING"

        if save_manifest(data):
            print(f"🚀 TAREA INICIADA: {found_ticket['id']}")
            return True
    else:
        print(f"❌ No encontré '{ticket_id}' en la cola.")
        return False

def finish_current_task(data):
    """Lógica interna para cerrar la tarea activa"""
    active = data['workflow'].get('active_ticket')
    if not active: return False

    active['completed_at'] = datetime.now().isoformat()
    if 'history' not in data['workflow']: data['workflow']['history'] = []
    data['workflow']['history'].insert(0, active)
    data['workflow']['active_ticket'] = None
    return True

def auto_advance():
    """Cierra la actual y arranca la siguiente automáticamente"""
    data = load_manifest()
    if not data: return

    # 1. Cerrar la actual
    if data['workflow'].get('active_ticket'):
        finished_id = data['workflow']['active_ticket']['id']
        finish_current_task(data)
        print(f"✅ AUTO-COMPLETE: {finished_id}")

    # 2. Iniciar la siguiente
    queue = data['workflow'].get('queue', [])
    if queue:
        next_ticket = queue[0] # Tomamos el primero
        queue.remove(next_ticket)
        next_ticket['started_at'] = datetime.now().isoformat()
        data['workflow']['active_ticket'] = next_ticket
        data['context']['health_status'] = "WORKING"
        print(f"🚀 AUTO-START: {next_ticket['id']} - {next_ticket['title']}")
    else:
        print("🏁 COLA VACÍA. Proyecto en estado IDLE.")
        data['context']['health_status'] = "IDLE"

    data['meta']['last_updated'] = datetime.now().isoformat()
    save_manifest(data)

def handle_git_hook(commit_msg):
    """Analiza el mensaje de commit para decidir acciones"""
    msg_lower = commit_msg.lower()

    # ¿Es un commit de cierre?
    # Buscamos: "finish:", "close:", "finish #TASK-001" o tipos "finish(scope):"
    is_closing = any(keyword in msg_lower for keyword in CLOSING_KEYWORDS)

    if is_closing:
        print("\n🤖 SISTEMA DETECTÓ CIERRE DE TAREA...")
        auto_advance()
        print("📄 Manifest actualizado. Se subirá en el próximo commit.\n")
    else:
        # Es un commit normal, solo actualizamos timestamp
        data = load_manifest()
        if data:
            data['meta']['last_updated'] = datetime.now().isoformat()
            save_manifest(data)

def status():
    data = load_manifest()
    if not data: return
    active = data['workflow'].get('active_ticket')
    print(f"\n📊 PROYECTO: {data['meta']['project_name']}")
    if active:
        print(f"🔨 EN CURSO: [{active['id']}] {active['title']}")
    else:
        print("💤 IDLE (Esperando 'pm.py start' o commit de cierre)")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python pm.py [start | hook | status]")

    cmd = sys.argv[1]

    if cmd == "start":
        if len(sys.argv) > 2: start_ticket(sys.argv[2])
    elif cmd == "hook":
        # El mensaje de commit viene como argumento completo
        if len(sys.argv) > 2: handle_git_hook(sys.argv[2])
    elif cmd == "status":
        status()
    elif cmd == "finish":
        # Manual finish (legacy support)
        auto_advance()