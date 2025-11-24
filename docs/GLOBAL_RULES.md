# GLOBAL RULES v2.0 - FreePlayerM

## 1. Arquitectura & Diseño
* **Clean Architecture:** Dependencias: `App -> Feature -> Domain <- Data`.
* **Single Responsibility:** Una clase, una responsabilidad. Si supera 200 líneas, refactoriza.
* **Contract-First:** NUNCA implementar lógica sin antes definir la `interface` en la capa Domain.
* **Inmutabilidad:** Usa `val` por defecto. Usa `data class` para modelos.

## 2. Stack Tecnológico (Estricto)
* **Lenguaje:** Kotlin 2.2.21 (K2 Compiler).
* **UI:** Jetpack Compose (Material 3). NO XML layouts.
* **Async:** Coroutines & Flow. NO RxJava. NO Callbacks.
* **DI:** Hilt. NO Koin (por estandarización de este proyecto).
* **DB:** Room con Flow.

## 3. Estándares de Código
* **Nomenclatura:**
    * Clases: `PascalCase` (ej: `SongRepository`).
    * Funciones/Variables: `camelCase` (ej: `getSongById`).
    * Constantes: `UPPER_SNAKE_CASE` (ej: `MAX_RETRY_COUNT`).
* **Result Pattern:** Los Repositories NUNCA lanzan excepciones. Retornan `Result<T>` o `Flow<Result<T>>`.
* **UI State:** Cada pantalla tiene una única `data class UiState`.

## 4. Flujo de Trabajo IA
* **Contexto:** Cada prompt debe iniciar con el contenido de `snapshot.txt`.
* **Validación:** Si la IA genera código que viola estas reglas, recházalo inmediatamente.
* **Tests:** Cada Feature nueva debe incluir al menos un Test Unitario del ViewModel.

## 5. Estándares de Documentación y Comentarios (OBLIGATORIO)
* **KDoc:** Todas las clases públicas (`public`), interfaces y métodos complejos deben tener bloque KDoc (`/** ... */`) explicando:
    * Qué hace.
    * `@param`: Qué recibe.
    * `@return`: Qué devuelve.
* **Comentarios Inline:** La lógica compleja dentro de funciones debe tener comentarios `//` explicando el "por qué", no el "qué".
* **Contexto:** Si una clase llama a un servicio externo o DB, comenta explícitamente esa dependencia.
* **Idioma:** Todos los comentarios en Español.