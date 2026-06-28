#!/usr/bin/env python3
"""
Ventana de historial de carreras y exportación CSV.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv


def mostrar_historial(app):
    """Abre una ventana Toplevel con el historial completo de carreras."""
    win = tk.Toplevel(app.root)
    win.title("Historial de carreras")
    win.configure(bg="#1d2433")
    win.geometry("820x520")

    tk.Label(win, text="📜  Historial de la noche", font=("Segoe UI", 18, "bold"),
             fg="#ffffff", bg="#1d2433").pack(anchor="w", padx=16, pady=(14, 6))

    if not app.historial:
        tk.Label(win, text="Todavía no se ha corrido ninguna carrera.",
                 font=("Segoe UI", 12), fg="#cdd6e6", bg="#1d2433").pack(
            padx=16, pady=20)
        return

    marco = tk.Frame(win, bg="#1d2433")
    marco.pack(fill="both", expand=True, padx=16)
    cols = ("n", "fecha", "seed", "ganador", "pozo", "cuota", "apuestas")
    tree = ttk.Treeview(marco, columns=cols, show="headings")
    encabezados = {"n": "#", "fecha": "Fecha", "seed": "Seed",
                   "ganador": "Ganador", "pozo": "Pozo",
                   "cuota": "Cuota", "apuestas": "Apuestas"}
    anchos = {"n": 40, "fecha": 150, "seed": 80, "ganador": 110,
              "pozo": 80, "cuota": 80, "apuestas": 80}
    for c in cols:
        tree.heading(c, text=encabezados[c])
        tree.column(c, width=anchos[c],
                    anchor="center" if c != "fecha" else "w")
    tree.pack(side="left", fill="both", expand=True)
    sb = ttk.Scrollbar(marco, orient="vertical", command=tree.yview)
    sb.pack(side="right", fill="y")
    tree.configure(yscrollcommand=sb.set)

    total_fichas = 0
    for h in app.historial:
        cuota = "—" if h["nadie_gano"] else f"{h['cuota']:.2f}x"
        gan = h["ganador"] + (" (nadie)" if h["nadie_gano"] else "")
        tree.insert("", "end", values=(h["n"], h["fecha"], h["seed"], gan,
                                       h["pozo_total"], cuota, h["n_apuestas"]))
        total_fichas += h["pozo_total"]

    pie = tk.Frame(win, bg="#1d2433")
    pie.pack(fill="x", padx=16, pady=12)
    tk.Label(pie, text=f"{len(app.historial)} carreras  ·  "
                      f"{total_fichas} fichas movidas en total",
             font=("Segoe UI", 11), fg="#cdd6e6", bg="#1d2433").pack(side="left")
    tk.Button(pie, text="💾  Exportar CSV", font=("Segoe UI", 12, "bold"),
              bg="#2ecc71", fg="#10331f", relief="flat", padx=14, pady=6,
              command=lambda: _exportar_csv(app)).pack(side="right")


def _exportar_csv(app):
    """Exporta todo el historial de carreras a un archivo CSV."""
    if not app.historial:
        messagebox.showinfo("Sin datos", "Aún no hay carreras que exportar.")
        return
    ruta = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV", "*.csv"), ("Todos", "*.*")],
        initialfile="historial_hipodromo.csv",
        title="Guardar historial como…")
    if not ruta:
        return
    try:
        # utf-8-sig para que Excel muestre bien los acentos
        with open(ruta, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.writer(f)
            w.writerow(["carrera", "fecha", "seed", "color_ganador", "cuota",
                        "pozo_total", "nombre", "color_apostado", "fichas",
                        "cobra", "gano"])
            for h in app.historial:
                cuota = "" if h["nadie_gano"] else f"{h['cuota']:.4f}"
                for d in h["detalle"]:
                    w.writerow([h["n"], h["fecha"], h["seed"], h["ganador"],
                                cuota, h["pozo_total"], d["nombre"],
                                d["color_apostado"], d["fichas"], d["cobra"],
                                "si" if d["gano"] else "no"])
        messagebox.showinfo("Exportado",
                            f"Historial guardado en:\n{ruta}")
    except OSError as e:
        messagebox.showerror("Error al guardar", str(e))
