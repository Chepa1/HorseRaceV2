# HorseRace 🐎

¡Bienvenido a **HorseRace**, un juego y simulador de carreras de caballos tipo hipódromo con apuestas! 

Este proyecto es una versión refactorizada y mejorada del proyecto original [angelesdepapel/HorseRace](https://github.com/angelesdepapel/HorseRace). Toda la reestructuración, la integración de la interfaz gráfica y la refactorización del código fue realizada a base de puro **Claude Opus 4.6**.

## Características Principales

*   **Sistema de Apuestas Parimutuel:** Las cuotas y pagos se calculan dinámicamente según el total apostado al caballo ganador versus el pozo total, emulando el sistema real de un hipódromo.
*   **Interfaz Gráfica (UI):** Construida con `tkinter` nativo de Python para una experiencia fluida sin dependencias externas pesadas. Permite:
    *   Ingresar apuestas (Nombre, Color del Caballo, Fichas).
    *   Ver cuotas provisionales y pozo total en tiempo real.
    *   Revisar el historial de todas las carreras de la sesión.
    *   Exportar el historial a CSV.
*   **Carrera Visual Interactiva:** Una vez realizadas las apuestas, la carrera se ejecuta utilizando **Pygame**. 
    *   Participan 8 caballos con colores únicos (sprites generados en tiempo real).
    *   Los caballos rebotan libremente por un mapa con obstáculos y chocan entre sí de forma realista.
    *   El primero en alcanzar la zanahoria (meta) se declara ganador.
*   **Resultados y Pagos Automáticos:** Al finalizar la carrera de Pygame, la interfaz de apuestas retoma el control y muestra automáticamente los ganadores, lo que cobran y actualiza el pozo acumulado para la siguiente ronda.

## Requisitos

El único requerimiento externo es la librería del juego:

```bash
pip install -r requirements.txt
```
*(Instalará `pygame-ce`)*

## Cómo Jugar

1.  Ejecuta el orquestador principal:
    ```bash
    python hipodromo.py
    ```
2.  Registra las apuestas de todos los jugadores en la ventana principal.
3.  Presiona el botón **▶ CORRER CARRERA**.
4.  ¡Disfruta de la caótica carrera visual en Pygame!
5.  Una vez terminada la carrera, cierra la ventana de Pygame (si no se cierra sola) para ver los resultados y el reparto de premios en la ventana principal.

## Cambios desde la versión original

*   **Integración UI-Juego:** Antes, el sistema de apuestas y la carrera de Pygame estaban separados en distintos scripts (`carrera.py`, `inscripciones.py`, etc.). Ahora todo se orquesta desde `hipodromo.py`.
*   **Limpieza de Código:** Se eliminaron 13 archivos obsoletos, reduciendo el ruido y unificando la lógica de pagos (`pagos.py`) y la configuración (`config.py`).
*   **Soporte Dinámico de Sprites:** `Game/main.py` ahora genera versiones de los caballos con diferentes colores en tiempo de ejecución (tinteando un `horse.png` base), permitiendo 8 competidores sin necesidad de múltiples archivos de imagen pre-fabricados.
*   **Transiciones sin archivos:** Ya no se usan archivos `.txt` para almacenar el estado de las apuestas entre menús; todo se maneja en memoria para mayor fluidez.