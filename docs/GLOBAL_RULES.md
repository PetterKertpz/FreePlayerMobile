# GLOBAL RULES - FreePlayerM

## 1. Arquitectura
* **Patrón:** Clean Architecture (Presentation -> Domain -> Data).
* **Modularización:** * `app`: Solo configuración de DI y Navegación.
    * `core/*`: Componentes reutilizables (Database, Network, UI System).
    * `features/*`: Lógica de negocio encapsulada (Player, Library).
* **UI:** Jetpack Compose ÚNICAMENTE (No XML layouts).
* **Inyección de Dependencias:** Hilt.

## 2. Flujo de Trabajo IA
* **Contract-First:** Antes de crear una clase, se debe definir su `interface` en la capa de Dominio.
* **Tests:** Cada PR debe incluir Unit Tests para ViewModels y UseCases.

## 3. Stack Tecnológico
* Lenguaje: Kotlin.
* Asincronía: Coroutines & Flow.
* Base de Datos: Room.
* Audio: Media3 (ExoPlayer).