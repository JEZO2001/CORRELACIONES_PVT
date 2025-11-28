import numpy as np
import math


# ==========================================
# 1. UTILIDADES
# ==========================================
def generar_presiones(P_res, P_atm):
    # Genera presiones descendentes de 10 en 10
    return np.arange(P_res, P_atm - 1, -10)


def calcular_gamma_o(API):
    return 141.5 / (131.5 + API)