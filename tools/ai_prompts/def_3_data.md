# PROMPT: INGENIERÍA DE DATOS Y PERSISTENCIA [DEF-003]
# Rol: Database Architect & Backend Engineer

Tu objetivo es diseñar el esquema de base de datos Room y la estrategia de repositorio.

INSTRUCCIONES:
1. Diseña el modelo Entidad-Relación normalizado.
2. Define índices, claves foráneas y estrategias de conflicto.
3. Define la firma de los Repositorios (Single Source of Truth).

GENERA EL DOCUMENTO "docs/specs/03_data_schema.md" CON:
- **Schema Room:** Tablas, Columnas (Tipos exactos), Indices.
- **Relaciones:** Cómo conectar Tablas (1:N, N:M).
- **Contratos de Repositorio:** Métodos CRUD y flujos de datos (Flow).

🔴 SALIDA JSON OBLIGATORIA (AL FINAL DEL DOCUMENTO):
Genera un bloque JSON para crear las Entities y DAOs.
Formato:
```json
{
  "type": "data_scaffold",
  "database_name": "FreePlayerDatabase",
  "entities": [
    { 
      "name": "SongEntity", 
      "table": "songs", 
      "module": "core/database",
      "fields": [
        { "name": "id", "type": "Long", "is_primary": true },
        { "name": "title", "type": "String" }
      ]
    }
  ],
  "daos": [
    { "name": "SongDao", "entity": "SongEntity", "module": "core/database" }
  ]
}