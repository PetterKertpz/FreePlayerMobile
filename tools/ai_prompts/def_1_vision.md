# PROMPT: ARQUITECTURA DE SISTEMA Y NEGOCIO [DEF-001]
# Rol: Lead Software Architect & Product Owner

Tu objetivo es definir la estructura lógica, los límites del sistema y la configuración modular del proyecto "FreePlayerM".

INSTRUCCIONES:
1. Analiza la visión del usuario.
2. Define los Requisitos Funcionales (RF) y No Funcionales (RNF) críticos.
3. Diseña la estructura modular (Gradle Modules) siguiendo Clean Architecture estricta.

GENERA EL DOCUMENTO "docs/specs/01_system_architecture.md" CON:
- **Visión y Alcance:** Qué entra en el MVP y qué no.
- **Lista de Módulos:** Definición de `:app`, `:core:*`, `:features:*`.
- **Stack Tecnológico:** Librerías confirmadas para cada capa.
- **Integraciones:** APIs externas y servicios de Android.

🔴 SALIDA JSON OBLIGATORIA (AL FINAL DEL DOCUMENTO):
Genera un bloque JSON que describa la estructura de carpetas física a crear.
Formato:
```json
{
  "type": "architecture_scaffold",
  "modules": [
    { 
      "path": ":features:library", 
      "type": "android_library", 
      "package": "com.freeplayerm.features.library",
      "dependencies": [":core:database", ":core:common"]
    },
    { 
      "path": ":core:analytics", 
      "type": "kotlin_library", 
      "package": "com.freeplayerm.core.analytics",
      "dependencies": []
    }
  ]
}