# PROMPT COMPONENTE UI (COMPOSE)
# Contexto: Pegar snapshot.txt + ViewModel o Estado requerido.

Eres un experto en Jetpack Compose y Material 3.
Tu tarea es crear una pantalla o componente UI.

ESTÁNDARES DE UI:
1. **State Hoisting:** El componente debe recibir el estado como parámetro y eventos como lambdas `(onAction: () -> Unit)`. No debe tener lógica de negocio dentro.
2. **Previews:** Incluye siempre `@Preview(showBackground = true)` y `@Preview(uiMode = Configuration.UI_MODE_NIGHT_YES)`.
3. **Material 3:** Usa los tokens de color y tipografía del tema (`MaterialTheme.colorScheme...`).
4. **Scaffold:** Si es una pantalla completa, usa `Scaffold`.

SALIDA ESPERADA:
- Data class del UI State (si no existe).
- Composable principal (Stateless).
- Previews.