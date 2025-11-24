# PROMPT: INGENIERÍA DE UI Y NAVEGACIÓN [DEF-002]
# Rol: Senior Frontend Engineer (Jetpack Compose)

Tu objetivo es definir las pantallas, estados y flujos de navegación. NO diseñes colores, define estructuras.

INSTRUCCIONES:
1. Define el Grafo de Navegación (Rutas y Argumentos).
2. Para cada Pantalla, define su `UiState` (Data Class) y sus `Events` (Lambda).
3. Identifica componentes reutilizables (Átomos/Moléculas).

GENERA EL DOCUMENTO "docs/specs/02_ui_engineering.md" CON:
- **Mapa de Navegación:** Rutas, DeepLinks y Argumentos.
- **Especificación de Pantallas:**
    - `LibraryScreen`: States (Loading, Success, Error), Events (OnSongClick).
- **Design System:** Lista de componentes base necesarios en `:core:ui`.

🔴 SALIDA JSON OBLIGATORIA (AL FINAL DEL DOCUMENTO):
Genera un bloque JSON para crear los esqueletos de Compose.
Formato:
```json
{
  "type": "ui_scaffold",
  "screens": [
    { 
      "name": "LibraryScreen", 
      "module": "features/library", 
      "route": "library_root",
      "state_fields": ["isLoading: Boolean", "songs: List<Song>"]
    }
  ],
  "components": [
    { "name": "SongCard", "module": "core/common" }
  ]
}