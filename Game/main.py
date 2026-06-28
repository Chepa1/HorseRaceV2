#!/usr/bin/env python3
"""
Carrera de Caballos — Pygame
============================
Lanza la carrera visual. Los caballos rebotan libremente, chocan entre sí
y con los obstáculos del laberinto. El primero en tocar la zanahoria gana.

Uso:
    python main.py <seed> <ruta_ganador.txt>

Si no se pasan argumentos, pide la seed por consola y escribe ganador.txt
en el directorio actual.
"""

import pygame
import sys
import os
import random
from Horse import Horse
from sound import SoundManager
from map import Map
from premio import Carrot

# ---------------------------------------------------------------------------
# Definición de caballos (debe coincidir con config.py del proyecto padre)
# ---------------------------------------------------------------------------
HORSES_DEF = [
    ("rojo",     "#dc3c3c"),
    ("azul",     "#466ed8"),
    ("verde",    "#46b45a"),
    ("amarillo", "#ecc835"),
    ("naranja",  "#eb8c32"),
    ("morado",   "#9650c8"),
    ("cian",     "#3fb6c4"),
    ("rosado",   "#e678b4"),
]

# Posiciones iniciales para 8 caballos (dentro de la primera sección del laberinto)
START_POSITIONS = [
    (113, 40),  (196, 40),
    (100, 100), (179, 100),
    (239, 100), (113, 160),
    (196, 160), (150, 220),
]

# ---------------------------------------------------------------------------
# Argumentos
# ---------------------------------------------------------------------------
if len(sys.argv) >= 2:
    seed = int(sys.argv[1])
else:
    seed = int(input("semilla: "))

ganador_file = sys.argv[2] if len(sys.argv) >= 3 else "ganador.txt"

random.seed(seed)

# ---------------------------------------------------------------------------
# Inicializar Pygame
# ---------------------------------------------------------------------------
pygame.init()

screen = pygame.display.set_mode((1080, 720))
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("Carrera de Caballos")

BACKGROUND_COLOR = (0, 204, 102)


# ---------------------------------------------------------------------------
# Generación de sprites tinteados
# ---------------------------------------------------------------------------
def hex_to_rgb(hex_color):
    """Convierte un color hex (#RRGGBB) a tupla (R, G, B)."""
    return (int(hex_color[1:3], 16),
            int(hex_color[3:5], 16),
            int(hex_color[5:7], 16))


def generate_tinted_sprites():
    """Carga horse.png y genera una versión tinteada por cada caballo.
    Los guarda como PNGs individuales en resources/images/ para que
    Horse.py los cargue sin modificaciones."""
    base_path = os.path.join("resources", "images", "horse.png")
    base = pygame.image.load(base_path).convert_alpha()
    base = pygame.transform.scale(base, (50, 50))

    for name, hex_color in HORSES_DEF:
        r, g, b = hex_to_rgb(hex_color)
        tinted = base.copy()
        # Capa semitransparente del color del caballo
        overlay = pygame.Surface(tinted.get_size(), pygame.SRCALPHA)
        overlay.fill((r, g, b, 160))
        tinted.blit(overlay, (0, 0))
        out_path = os.path.join("resources", "images", f"{name}.png")
        pygame.image.save(tinted, out_path)


generate_tinted_sprites()

# ---------------------------------------------------------------------------
# Generar zanahoria (meta) si no existe
# ---------------------------------------------------------------------------
carrot_path = os.path.join("resources", "images", "carrot.png")
if not os.path.exists(carrot_path):
    carrot_surf = pygame.Surface((30, 30), pygame.SRCALPHA)
    # Círculo dorado como meta
    pygame.draw.circle(carrot_surf, (255, 200, 0), (15, 15), 14)
    pygame.draw.circle(carrot_surf, (200, 150, 0), (15, 15), 14, 3)
    # Tallito verde
    pygame.draw.rect(carrot_surf, (0, 180, 0), (12, 0, 6, 6))
    pygame.image.save(carrot_surf, carrot_path)

# ---------------------------------------------------------------------------
# Sonido
# ---------------------------------------------------------------------------
sound_manager = SoundManager()
sound_manager.load_sound("clop", "resources/sounds/clop.wav")

# ---------------------------------------------------------------------------
# Crear caballos
# ---------------------------------------------------------------------------
horses = []
for i, (name, hex_color) in enumerate(HORSES_DEF):
    horse = Horse(WIDTH, HEIGHT,
                  start_pos=START_POSITIONS[i],
                  image=f"{name}.png",
                  name=name)
    horses.append(horse)

for horse in horses:
    for rival in horses:
        if horse != rival:
            horse.rivals.append(rival)

# ---------------------------------------------------------------------------
# Crear mapa y meta
# ---------------------------------------------------------------------------
game_map = Map(WIDTH, HEIGHT)
boxes = game_map.box_list()

carrot = Carrot(WIDTH, HEIGHT)

# ---------------------------------------------------------------------------
# Bucle principal
# ---------------------------------------------------------------------------
clock = pygame.time.Clock()
running = True
winner_name = None

while running:
    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Actualizar caballos
    for horse in horses:
        bounced = horse.update(boxes)
        if bounced:
            sound_manager.play_sound("clop", volume=0.3)

    # Dibujar
    screen.fill(BACKGROUND_COLOR)

    for box in boxes:
        box.draw(screen)

    for horse in horses:
        horse.draw(screen)
        if horse._winner(carrot):
            winner_name = horse.name
            running = False

    carrot.draw(screen)

    pygame.display.flip()
    clock.tick(60)

# ---------------------------------------------------------------------------
# Escribir ganador y salir
# ---------------------------------------------------------------------------
if winner_name:
    try:
        with open(ganador_file, 'w', encoding='utf-8') as f:
            f.write(winner_name)
        print(f"{winner_name} es el ganador :)")
    except Exception as e:
        print(f"Error al escribir ganador: {e}")

pygame.quit()
sys.exit()