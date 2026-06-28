#!/usr/bin/env python3
"""
Lógica de pagos parimutuel / totalizador.

CÓMO FUNCIONA (independiente de la interfaz, fácil de verificar):
- Cada persona apuesta fichas a un color.
- Todas las fichas forman un POZO común.
- Gana el color del caballo que cruza primero la meta.
- cuota = pozo total / total apostado al color ganador
- Cada ganador cobra:  sus fichas × cuota
- Si NADIE apostó al ganador, todo el pozo se acumula a la próxima carrera.
"""


def calcular_pagos(apuestas, ganador_idx, pozo_acumulado, comision, unidad):
    """
    apuestas : lista de dicts {'nombre', 'color', 'fichas'}
    ganador_idx : índice del caballo ganador en CABALLOS
    pozo_acumulado : fichas acumuladas de carreras anteriores
    comision : fracción retenida por la casa (0.0 = nada)
    unidad : ficha más chica (pagos se redondean a este múltiplo)

    Devuelve un dict con todo el desglose del reparto.
    """
    apostado = sum(a["fichas"] for a in apuestas)
    pozo_total = apostado + pozo_acumulado
    pool_ganador = sum(a["fichas"] for a in apuestas if a["color"] == ganador_idx)

    if pool_ganador == 0:
        # Nadie le apostó al ganador -> todo el pozo se acumula a la próxima.
        return {
            "nadie_gano": True,
            "pozo_total": pozo_total,
            "apostado": apostado,
            "pozo_acumulado_previo": pozo_acumulado,
            "pool_ganador": 0,
            "cuota": 0.0,
            "comision_monto": 0,
            "repartible": 0,
            "pagos": [],
            "pagado": 0,
            "sobrante": 0,
            "nuevo_acumulado": pozo_total,
        }

    comision_monto = int(pozo_total * comision)
    repartible = pozo_total - comision_monto
    cuota = repartible / pool_ganador

    pagos = []
    pagado = 0
    for a in apuestas:
        if a["color"] == ganador_idx:
            # redondeo HACIA ABAJO a la unidad de ficha
            pago = int((a["fichas"] * cuota) // unidad) * unidad
            pagos.append({"nombre": a["nombre"], "fichas": a["fichas"], "pago": pago})
            pagado += pago

    sobrante = repartible - pagado  # lo que no se pudo repartir por redondeo

    return {
        "nadie_gano": False,
        "pozo_total": pozo_total,
        "apostado": apostado,
        "pozo_acumulado_previo": pozo_acumulado,
        "pool_ganador": pool_ganador,
        "cuota": cuota,
        "comision_monto": comision_monto,
        "repartible": repartible,
        "pagos": pagos,
        "pagado": pagado,
        "sobrante": sobrante,
        "nuevo_acumulado": sobrante,  # el redondeo pasa a la próxima carrera
    }
