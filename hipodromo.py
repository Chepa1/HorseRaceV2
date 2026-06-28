#!/usr/bin/env python3
"""
HIPÓDROMO — Noche de Apuestas (sistema parimutuel / totalizador)
================================================================

No usa dependencias externas: solo tkinter, que viene con Python.
La carrera visual usa Pygame (carpeta Game/).

Ejecuta:   python hipodromo.py
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import os
import secrets

from config import CABALLOS, N
from ui_apuestas import construir_pantalla_apuestas
from ui_resultados import construir_pantalla_resultados
from ui_historial import mostrar_historial as _mostrar_historial

# Rutas absolutas derivadas de la ubicación de este script
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GANADOR_FILE = os.path.join(_BASE_DIR, "ganador.txt")
GAME_DIR = os.path.join(_BASE_DIR, "Game")
GAME_MAIN = os.path.join(GAME_DIR, "main.py")


class Hipodromo:
    def __init__(self, root):
        self.root = root
        self.root.title("🐎 Hipódromo — Noche de Apuestas")
        self.root.configure(bg="#1d2433")
        self.root.geometry("1060x720")

        self.apuestas = []          # [{'nombre', 'color', 'fichas'}]
        self.pozo_acumulado = 0
        self.sel_color = None       # índice de color seleccionado en el form
        self.color_btns = []
        self.historial = []         # resumen de cada carrera corrida
        self.current_seed = None    # semilla de la carrera en curso
        self.seed_var = tk.StringVar()
        self.game_process = None    # subproceso de Pygame

        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("Treeview", rowheight=26, font=("Segoe UI", 11))
        style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"))

        self.container = tk.Frame(root, bg="#1d2433")
        self.container.pack(fill="both", expand=True)

        self.mostrar_apuestas()

    # -- utilidades de pantalla --
    def _limpiar(self):
        for w in self.container.winfo_children():
            w.destroy()

    def _nueva_seed(self):
        """Genera una nueva seed aleatoria (impredecible, usa secrets)."""
        self.seed_var.set(str(secrets.randbelow(900000) + 100000))

    # ===================================================================
    # PANTALLA 1: APUESTAS (delegada a ui_apuestas.py)
    # ===================================================================
    def mostrar_apuestas(self):
        self._limpiar()
        construir_pantalla_apuestas(self)

    # ===================================================================
    # CARRERA: lanza Game/main.py como subproceso Pygame
    # ===================================================================
    def iniciar_carrera(self):
        if not self.apuestas:
            return

        # fijar la semilla
        try:
            self.current_seed = int(self.seed_var.get())
        except (ValueError, tk.TclError):
            self.current_seed = secrets.randbelow(900000) + 100000
            self.seed_var.set(str(self.current_seed))

        # limpiar ganador.txt
        with open(GANADOR_FILE, "w") as f:
            pass

        # lanzar el juego de Pygame como subproceso
        try:
            self.game_process = subprocess.Popen(
                [sys.executable, GAME_MAIN,
                 str(self.current_seed), GANADOR_FILE],
                cwd=GAME_DIR
            )
        except Exception as e:
            messagebox.showerror("Error",
                                 f"No se pudo lanzar la carrera:\n{e}")
            return

        # mostrar pantalla de espera
        self._limpiar()
        tk.Label(self.container, text="🏇  ¡Carrera en curso!",
                 font=("Segoe UI", 28, "bold"),
                 fg="#ffd166", bg="#1d2433").pack(expand=True)
        tk.Label(self.container, text=f"Seed: {self.current_seed}",
                 font=("Segoe UI", 14),
                 fg="#7e8aa0", bg="#1d2433").pack()
        tk.Label(self.container,
                 text="La ventana de Pygame se abrió.  ¡Mira la carrera!",
                 font=("Segoe UI", 12),
                 fg="#cdd6e6", bg="#1d2433").pack(pady=20)

        # comenzar a monitorear ganador.txt
        self._monitorear_ganador()

    def _monitorear_ganador(self):
        """Revisa periódicamente si el subproceso de Pygame terminó y si
        hay un ganador escrito en ganador.txt."""

        # ¿Terminó el proceso?
        if self.game_process and self.game_process.poll() is not None:
            ganador = self._leer_ganador()
            if ganador is not None:
                self._procesar_ganador(ganador)
                return
            else:
                # El usuario cerró la ventana sin que hubiera ganador
                messagebox.showwarning(
                    "Carrera cancelada",
                    "La ventana de la carrera se cerró sin un ganador.")
                self.mostrar_apuestas()
                return

        # ¿Se escribió un ganador aunque el proceso siga vivo?
        ganador = self._leer_ganador()
        if ganador is not None:
            if self.game_process:
                try:
                    self.game_process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    self.game_process.kill()
            self._procesar_ganador(ganador)
            return

        # Seguir esperando
        self.root.after(500, self._monitorear_ganador)

    def _leer_ganador(self):
        """Lee ganador.txt. Devuelve el nombre (lowercase) o None."""
        try:
            if (os.path.exists(GANADOR_FILE)
                    and os.path.getsize(GANADOR_FILE) > 0):
                with open(GANADOR_FILE, "r", encoding="utf-8") as f:
                    nombre = f.readline().strip().lower()
                    if nombre:
                        return nombre
        except (OSError, ValueError):
            pass
        return None

    def _procesar_ganador(self, nombre_ganador):
        """Mapea el nombre del caballo ganador a su índice en CABALLOS
        y muestra la pantalla de resultados."""
        ganador_idx = None
        for i, (nombre, _) in enumerate(CABALLOS):
            if nombre.lower() == nombre_ganador:
                ganador_idx = i
                break

        if ganador_idx is None:
            messagebox.showerror(
                "Error",
                f"El ganador '{nombre_ganador}' no coincide con "
                f"ningún caballo registrado.")
            self.mostrar_apuestas()
            return

        # limpiar ganador.txt para la próxima carrera
        with open(GANADOR_FILE, "w") as f:
            pass

        self.mostrar_resultados(ganador_idx)

    # ===================================================================
    # PANTALLA 3: RESULTADOS (delegada a ui_resultados.py)
    # ===================================================================
    def mostrar_resultados(self, ganador_idx):
        self._limpiar()
        construir_pantalla_resultados(self, ganador_idx)

    # ===================================================================
    # HISTORIAL (delegado a ui_historial.py)
    # ===================================================================
    def mostrar_historial(self):
        _mostrar_historial(self)


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = Hipodromo(root)
    root.mainloop()
