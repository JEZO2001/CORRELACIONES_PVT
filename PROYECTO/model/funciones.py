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

# ==========================================
# 2. SOLUBILIDAD DEL GAS (Rs) - Standing
# ==========================================
def standing_rs(P, yg, API, T):
    # Standing (1947) - PDF Pag 25
    x = 0.0125 * API - 0.00091 * T
    term = (P / 18.2) + 1.4
    rs = yg * (term * (10 ** x)) ** 1.2048
    return rs
