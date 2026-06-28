#!/usr/bin/env python3
"""
Pantalla de resultados — desglose de pagos y acciones post-carrera.
"""

import tkinter as tk
from tkinter import ttk
from datetime import datetime
from config import CABALLOS, COMISION, UNIDAD
from pagos import calcular_pagos


def construir_pantalla_resultados(app, ganador_idx):
    """Construye la pantalla de resultados/pagos en app.container."""
    nombre_g, hex_g = CABALLOS[ganador_idx]
    res = calcular_pagos(app.apuestas, ganador_idx, app.pozo_acumulado,
                         COMISION, UNIDAD)

    # ---- detalle por persona (sirve para la tabla y el historial) ----
    detalle = []
    idx_p = 0
    for a in app.apuestas:
        if a["color"] == ganador_idx and not res["nadie_gano"]:
            cobra = res["pagos"][idx_p]["pago"]
            idx_p += 1
            gano = True
        else:
            cobra = 0
            gano = False
        detalle.append({
            "nombre": a["nombre"],
            "color_apostado": CABALLOS[a["color"]][0],
            "fichas": a["fichas"],
            "cobra": cobra,
            "gano": gano,
        })

    # ---- registrar en el historial ----
    app.historial.append({
        "n": len(app.historial) + 1,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "seed": app.current_seed,
        "ganador": nombre_g,
        "pozo_total": res["pozo_total"],
        "pool_ganador": res["pool_ganador"],
        "cuota": res["cuota"],
        "n_apuestas": len(app.apuestas),
        "nadie_gano": res["nadie_gano"],
        "detalle": detalle,
    })

    cont = app.container
    head = tk.Frame(cont, bg="#1d2433")
    head.pack(fill="x", padx=20, pady=(18, 6))
    tk.Label(head, text="🏆  GANADOR:", font=("Segoe UI", 22, "bold"),
             fg="#ffffff", bg="#1d2433").pack(side="left")
    tk.Label(head, text=f" {nombre_g.upper()}", font=("Segoe UI", 22, "bold"),
             fg=hex_g, bg="#1d2433").pack(side="left")
    tk.Label(head, text=f"Carrera #{len(app.historial)}  ·  seed "
                        f"{app.current_seed}", font=("Segoe UI", 11),
             fg="#7e8aa0", bg="#1d2433").pack(side="right")

    # panel de desglose
    info = tk.Frame(cont, bg="#262f42", highlightbackground="#3a465f",
                    highlightthickness=1)
    info.pack(fill="x", padx=20, pady=8)

    if res["nadie_gano"]:
        txt = (f"Nadie le apostó al {nombre_g}.\n"
               f"Todo el pozo ({res['pozo_total']} fichas) pasa ACUMULADO "
               f"a la próxima carrera.")
        tk.Label(info, text=txt, font=("Segoe UI", 14, "bold"),
                 fg="#ffd166", bg="#262f42", justify="left").pack(
            padx=16, pady=14, anchor="w")
    else:
        lineas = [
            f"Pozo total: {res['pozo_total']} fichas"
            + (f"  (incluye {res['pozo_acumulado_previo']} acumulados)"
               if res['pozo_acumulado_previo'] else ""),
            f"Apostado al {nombre_g}: {res['pool_ganador']} fichas",
            f"CUOTA = {res['pozo_total']} / {res['pool_ganador']} "
            f"= {res['cuota']:.2f}x",
        ]
        if res["comision_monto"] > 0:
            lineas.insert(1, f"Comisión casa ({COMISION:.0%}): "
                             f"{res['comision_monto']} fichas")
        tk.Label(info, text="\n".join(lineas), font=("Segoe UI", 13),
                 fg="#e6ecf7", bg="#262f42", justify="left").pack(
            padx=16, pady=12, anchor="w")

    # tabla de pagos
    tk.Label(cont, text="Pagos", font=("Segoe UI", 14, "bold"),
             fg="#ffffff", bg="#1d2433").pack(anchor="w", padx=20, pady=(8, 2))
    marco = tk.Frame(cont, bg="#1d2433")
    marco.pack(fill="both", expand=True, padx=20)
    tree = ttk.Treeview(marco,
                        columns=("nombre", "color", "fichas", "cobra"),
                        show="headings", height=10)
    tree.heading("nombre", text="Nombre")
    tree.heading("color", text="Apostó a")
    tree.heading("fichas", text="Fichas")
    tree.heading("cobra", text="Cobra")
    tree.column("nombre", width=240)
    tree.column("color", width=140, anchor="center")
    tree.column("fichas", width=120, anchor="e")
    tree.column("cobra", width=140, anchor="e")
    tree.pack(side="left", fill="both", expand=True)
    sb = ttk.Scrollbar(marco, orient="vertical", command=tree.yview)
    sb.pack(side="right", fill="y")
    tree.configure(yscrollcommand=sb.set)
    tree.tag_configure("gana", background="#22351f", foreground="#9be29b")
    tree.tag_configure("pierde", foreground="#9aa6ba")

    # los pagos vienen del detalle ya calculado
    for d in detalle:
        tag = "gana" if d["gano"] else "pierde"
        tree.insert("", "end",
                    values=(d["nombre"], d["color_apostado"],
                            d["fichas"], d["cobra"]),
                    tags=(tag,))

    # pie con sobrante y botón nueva carrera
    pie = tk.Frame(cont, bg="#1d2433")
    pie.pack(fill="x", padx=20, pady=12)
    nota = ""
    if not res["nadie_gano"]:
        nota = (f"Repartido: {res['pagado']} fichas.  "
                f"Sobrante por redondeo: {res['sobrante']} "
                f"→ pozo acumulado próxima carrera.")
    tk.Label(pie, text=nota, font=("Segoe UI", 11),
             fg="#cdd6e6", bg="#1d2433").pack(side="left")

    botones = tk.Frame(pie, bg="#1d2433")
    botones.pack(side="right")
    tk.Button(botones, text="📜  Historial", font=("Segoe UI", 12),
              bg="#3a465f", fg="white", relief="flat", padx=12, pady=8,
              command=app.mostrar_historial).pack(side="left", padx=(0, 8))
    tk.Button(botones, text="🔄  Nueva carrera", font=("Segoe UI", 14, "bold"),
              bg="#3a7bd5", fg="white", relief="flat", padx=16, pady=8,
              command=lambda: _nueva_carrera(app, res)).pack(side="left")


def _nueva_carrera(app, res):
    """Prepara el estado para una nueva carrera y vuelve a la pantalla de apuestas."""
    app.pozo_acumulado = res["nuevo_acumulado"]
    app.apuestas = []
    app._nueva_seed()
    app.mostrar_apuestas()
