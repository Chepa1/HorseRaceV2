#!/usr/bin/env python3
"""
Configuración central del Hipódromo.
Constantes compartidas por la UI (tkinter) y la carrera (Pygame).
"""

UNIDAD = 1        # ficha más chica; pagos se redondean a múltiplos de esto
COMISION = 0.0    # 0.0 = sin comisión. 0.10 = la casa retiene 10%.

# Colores de los caballos: (nombre, color hex de relleno)
CABALLOS = [
    ("Rojo",     "#dc3c3c"),
    ("Azul",     "#466ed8"),
    ("Verde",    "#46b45a"),
    ("Amarillo", "#ecc835"),
    ("Naranja",  "#eb8c32"),
    ("Morado",   "#9650c8"),
    ("Cian",     "#3fb6c4"),
    ("Rosado",   "#e678b4"),
]
N = len(CABALLOS)


def texto_legible(hex_color):
    """Devuelve negro o blanco según el brillo del color de fondo."""
    r = int(hex_color[1:3], 16)
    g = int(hex_color[3:5], 16)
    b = int(hex_color[5:7], 16)
    lum = (0.299 * r + 0.587 * g + 0.114 * b)
    return "#000000" if lum > 150 else "#ffffff"


def oscurecer(hex_color, factor=0.6):
    """Devuelve una versión más oscura del color hex."""
    r = int(int(hex_color[1:3], 16) * factor)
    g = int(int(hex_color[3:5], 16) * factor)
    b = int(int(hex_color[5:7], 16) * factor)
    return f"#{r:02x}{g:02x}{b:02x}"
