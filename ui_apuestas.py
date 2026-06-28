#!/usr/bin/env python3
"""
Pantalla de apuestas — formulario, tabla de apuestas, cuotas provisionales.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from config import CABALLOS, N, COMISION, texto_legible


def construir_pantalla_apuestas(app):
    """Construye la pantalla de apuestas en app.container."""
    app.sel_color = None
    app.color_btns = []

    cont = app.container

    # Encabezado
    head = tk.Frame(cont, bg="#1d2433")
    head.pack(fill="x", padx=20, pady=(16, 6))
    tk.Label(head, text="🐎  Mesa de Apuestas", font=("Segoe UI", 22, "bold"),
             fg="#ffffff", bg="#1d2433").pack(side="left")
    app.lbl_acum = tk.Label(head, text="", font=("Segoe UI", 13, "bold"),
                             fg="#ffd166", bg="#1d2433")
    app.lbl_acum.pack(side="right")

    # Barra de seed + historial
    barra = tk.Frame(cont, bg="#1d2433")
    barra.pack(fill="x", padx=20)
    tk.Label(barra, text="Seed de la carrera:", font=("Segoe UI", 11),
             fg="#cdd6e6", bg="#1d2433").pack(side="left")
    if not app.seed_var.get():
        app._nueva_seed()
    tk.Entry(barra, textvariable=app.seed_var, font=("Consolas", 12, "bold"),
             width=10, justify="center").pack(side="left", padx=(6, 4))
    tk.Button(barra, text="🎲", font=("Segoe UI", 10), relief="flat",
              bg="#3a465f", fg="white", command=app._nueva_seed).pack(side="left")
    tk.Label(barra, text="(determina la carrera; igual seed = igual resultado)",
             font=("Segoe UI", 9), fg="#7e8aa0", bg="#1d2433").pack(side="left",
                                                                     padx=8)
    tk.Button(barra, text=f"📜  Historial ({len(app.historial)})",
              font=("Segoe UI", 11), relief="flat", bg="#3a465f", fg="white",
              command=app.mostrar_historial).pack(side="right")

    cuerpo = tk.Frame(cont, bg="#1d2433")
    cuerpo.pack(fill="both", expand=True, padx=20, pady=6)

    # ---- Columna izquierda: formulario ----
    form = tk.Frame(cuerpo, bg="#262f42", bd=0)
    form.pack(side="left", fill="y", padx=(0, 14))
    form.configure(highlightbackground="#3a465f", highlightthickness=1)

    tk.Label(form, text="Nueva apuesta", font=("Segoe UI", 14, "bold"),
             fg="#ffffff", bg="#262f42").grid(row=0, column=0, columnspan=2,
                                              sticky="w", padx=16, pady=(14, 8))

    tk.Label(form, text="Nombre:", font=("Segoe UI", 12), fg="#cdd6e6",
             bg="#262f42").grid(row=1, column=0, sticky="w", padx=16)
    app.ent_nombre = tk.Entry(form, font=("Segoe UI", 12), width=20)
    app.ent_nombre.grid(row=1, column=1, sticky="w", padx=(0, 16), pady=4)

    tk.Label(form, text="Color:", font=("Segoe UI", 12), fg="#cdd6e6",
             bg="#262f42").grid(row=2, column=0, sticky="nw", padx=16, pady=(8, 0))
    colorgrid = tk.Frame(form, bg="#262f42")
    colorgrid.grid(row=2, column=1, sticky="w", padx=(0, 16), pady=(8, 0))
    for i, (nombre, hexcol) in enumerate(CABALLOS):
        b = tk.Button(colorgrid, text=nombre, width=8,
                      font=("Segoe UI", 10, "bold"),
                      bg=hexcol, fg=texto_legible(hexcol),
                      relief="raised", bd=2,
                      activebackground=hexcol,
                      command=lambda idx=i: _seleccionar_color(app, idx))
        b.grid(row=i // 2, column=i % 2, padx=3, pady=3, sticky="we")
        app.color_btns.append(b)

    tk.Label(form, text="Fichas:", font=("Segoe UI", 12), fg="#cdd6e6",
             bg="#262f42").grid(row=3, column=0, sticky="w", padx=16, pady=(10, 0))
    app.ent_fichas = tk.Entry(form, font=("Segoe UI", 12), width=10)
    app.ent_fichas.grid(row=3, column=1, sticky="w", padx=(0, 16), pady=(10, 0))
    app.ent_fichas.bind("<Return>", lambda e: _agregar_apuesta(app))

    tk.Button(form, text="➕  Agregar apuesta", font=("Segoe UI", 12, "bold"),
              bg="#3a7bd5", fg="white", relief="flat", padx=10, pady=6,
              activebackground="#2f66b3",
              command=lambda: _agregar_apuesta(app)).grid(
        row=4, column=0, columnspan=2, sticky="we", padx=16, pady=(16, 14))

    # ---- Columna derecha: listas ----
    der = tk.Frame(cuerpo, bg="#1d2433")
    der.pack(side="left", fill="both", expand=True)

    # Apuestas registradas
    tk.Label(der, text="Apuestas registradas", font=("Segoe UI", 13, "bold"),
             fg="#ffffff", bg="#1d2433").pack(anchor="w")
    marco_ap = tk.Frame(der, bg="#1d2433")
    marco_ap.pack(fill="both", expand=True, pady=(4, 10))
    app.tree_ap = ttk.Treeview(marco_ap, columns=("nombre", "color", "fichas"),
                                show="headings", height=7)
    app.tree_ap.heading("nombre", text="Nombre")
    app.tree_ap.heading("color", text="Color")
    app.tree_ap.heading("fichas", text="Fichas")
    app.tree_ap.column("nombre", width=180)
    app.tree_ap.column("color", width=120, anchor="center")
    app.tree_ap.column("fichas", width=90, anchor="e")
    app.tree_ap.pack(side="left", fill="both", expand=True)
    sb = ttk.Scrollbar(marco_ap, orient="vertical", command=app.tree_ap.yview)
    sb.pack(side="right", fill="y")
    app.tree_ap.configure(yscrollcommand=sb.set)
    for i, (nombre, hexcol) in enumerate(CABALLOS):
        app.tree_ap.tag_configure(f"c{i}", foreground=hexcol)

    tk.Button(der, text="🗑  Quitar seleccionada", font=("Segoe UI", 11),
              bg="#5a4a4a", fg="white", relief="flat", padx=8, pady=4,
              command=lambda: _quitar_apuesta(app)).pack(anchor="w")

    # Resumen por color (cuotas provisionales)
    tk.Label(der, text="Pozo por color (cuota provisional)",
             font=("Segoe UI", 13, "bold"),
             fg="#ffffff", bg="#1d2433").pack(anchor="w", pady=(14, 4))
    app.tree_res = ttk.Treeview(der, columns=("color", "fichas", "cuota"),
                                 show="headings", height=8)
    app.tree_res.heading("color", text="Color")
    app.tree_res.heading("fichas", text="Apostado")
    app.tree_res.heading("cuota", text="Cuota si gana")
    app.tree_res.column("color", width=140)
    app.tree_res.column("fichas", width=110, anchor="e")
    app.tree_res.column("cuota", width=120, anchor="e")
    app.tree_res.pack(fill="x")
    for i, (nombre, hexcol) in enumerate(CABALLOS):
        app.tree_res.tag_configure(f"c{i}", foreground=hexcol)

    # Pie: pozo total + correr
    pie = tk.Frame(cont, bg="#1d2433")
    pie.pack(fill="x", padx=20, pady=(8, 16))
    app.lbl_pozo = tk.Label(pie, text="", font=("Segoe UI", 16, "bold"),
                             fg="#9be29b", bg="#1d2433")
    app.lbl_pozo.pack(side="left")
    app.btn_correr = tk.Button(pie, text="▶  CORRER CARRERA",
                                font=("Segoe UI", 15, "bold"),
                                bg="#2ecc71", fg="#10331f", relief="flat",
                                padx=18, pady=8, activebackground="#27b366",
                                command=app.iniciar_carrera)
    app.btn_correr.pack(side="right")

    _refrescar_vistas(app)


def _seleccionar_color(app, idx):
    """Marca visualmente el color seleccionado en el formulario."""
    app.sel_color = idx
    for i, b in enumerate(app.color_btns):
        if i == idx:
            b.configure(relief="sunken", bd=4)
        else:
            b.configure(relief="raised", bd=2)


def _agregar_apuesta(app):
    """Valida y agrega una apuesta a la lista."""
    nombre = app.ent_nombre.get().strip()
    if not nombre:
        messagebox.showwarning("Falta nombre", "Escribe el nombre de la persona.")
        return
    if app.sel_color is None:
        messagebox.showwarning("Falta color", "Selecciona un color.")
        return
    try:
        fichas = int(app.ent_fichas.get())
    except ValueError:
        messagebox.showwarning("Fichas inválidas", "Ingresa un número de fichas.")
        return
    if fichas <= 0:
        messagebox.showwarning("Fichas inválidas", "Las fichas deben ser > 0.")
        return

    app.apuestas.append({"nombre": nombre, "color": app.sel_color,
                          "fichas": fichas})
    # limpiar para la siguiente
    app.ent_nombre.delete(0, "end")
    app.ent_fichas.delete(0, "end")
    app.ent_nombre.focus_set()
    _refrescar_vistas(app)


def _quitar_apuesta(app):
    """Elimina la apuesta seleccionada de la tabla."""
    sel = app.tree_ap.selection()
    if not sel:
        return
    idx = app.tree_ap.index(sel[0])
    del app.apuestas[idx]
    _refrescar_vistas(app)


def _refrescar_vistas(app):
    """Actualiza las tablas de apuestas, cuotas y el pozo total."""
    # tabla de apuestas
    app.tree_ap.delete(*app.tree_ap.get_children())
    for a in app.apuestas:
        nombre_color = CABALLOS[a["color"]][0]
        app.tree_ap.insert("", "end",
                            values=(a["nombre"], nombre_color, a["fichas"]),
                            tags=(f"c{a['color']}",))

    # resumen por color + cuotas provisionales
    apostado = sum(a["fichas"] for a in app.apuestas)
    pozo_total = apostado + app.pozo_acumulado
    repartible = pozo_total * (1 - COMISION)
    app.tree_res.delete(*app.tree_res.get_children())
    for i, (nombre, hexcol) in enumerate(CABALLOS):
        pool = sum(a["fichas"] for a in app.apuestas if a["color"] == i)
        cuota = (repartible / pool) if pool > 0 else 0
        cuota_txt = f"{cuota:.2f}x" if pool > 0 else "—"
        app.tree_res.insert("", "end",
                             values=(nombre, pool, cuota_txt), tags=(f"c{i}",))

    # pozo total y acumulado
    app.lbl_pozo.config(text=f"Pozo total: {pozo_total} fichas"
                              f"   ({len(app.apuestas)} apuestas)")
    if app.pozo_acumulado > 0:
        app.lbl_acum.config(text=f"💰 Pozo acumulado: {app.pozo_acumulado}")
    else:
        app.lbl_acum.config(text="")

    # habilitar correr solo con apuestas
    if app.apuestas:
        app.btn_correr.config(state="normal", bg="#2ecc71")
    else:
        app.btn_correr.config(state="disabled", bg="#5a6b5a")
