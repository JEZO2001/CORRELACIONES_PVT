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

# ==========================================
# 3. COMPRESIBILIDAD (Co) - Vasquez-Beggs
# ==========================================
def vasquez_beggs_co(Rsb, yg, API, T, P, T_sep=100, P_sep=100):
    # Vasquez-Beggs (1980) - PDF Pag 29
    # Corrección de gravedad de gas (ygc)
    ygc = yg * (1 + 5.912e-5 * API * T_sep * math.log10(P_sep / 114.7))

    numerator = -1433 + 5 * Rsb + 17.2 * T - 1180 * ygc + 12.61 * API
    denominator = 10 ** 5 * P
    co = numerator / denominator
    return co


# ==========================================
# 4. FACTOR VOLUMÉTRICO (Bo)
# ==========================================
def standing_bo_saturado(Rs, yg, yo, T):
    # Standing (1981) - PDF Pag 33
    term = Rs * ((yg / yo) ** 0.5) + 1.25 * T
    bo = 0.9759 + 1.2e-4 * (term ** 1.2)
    return bo


def bo_subsaturado(Bob, Co, Pb, P):
    # Ecuación general usando Co - PDF Pag 37
    # Nota: Usamos exponencial para ajustar el volumen
    return Bob * math.exp(Co * (Pb - P))


# ==========================================
# 5. DENSIDAD DEL PETRÓLEO (rho_o)
# ==========================================
def standing_densidad_saturado(Rs, yg, yo, T):
    # Standing (1947) - PDF Pag 39
    num = 62.4 * yo + 0.0136 * Rs * yg
    term = Rs * ((yg / yo) ** 0.5) + 1.25 * T
    den_val = 0.972 + 0.000147 * (term ** 1.175)

    rho = num / den_val
    return rho


def densidad_subsaturado(rho_ob, Co, Pb, P):
    # Ecuación general - PDF Pag 40
    # La densidad aumenta con la presión (exponente positivo P - Pb)
    return rho_ob * math.exp(Co * (P - Pb))


# ==========================================
# 6. VISCOSIDAD DEL PETRÓLEO (mu_o)
# ==========================================
def beggs_robinson_mu_dead(API, T):
    # Beggs-Robinson (1975) - PDF Pag 43
    z = 3.0324 - 0.02023 * API
    y = 10 ** z
    x = y * (T ** -1.163)
    mu_od = (10 ** x) - 1.0
    return mu_od


def beggs_robinson_mu_saturado(mu_od, Rs):
    # Beggs-Robinson (1975) - PDF Pag 44
    a = 10.715 * ((Rs + 100) ** -0.515)
    b = 5.44 * ((Rs + 150) ** -0.338)
    mu_ob = a * (mu_od ** b)
    return mu_ob


def vasquez_beggs_mu_subsaturado(mu_ob, P, Pb):
    # Vasquez-Beggs (1980) - PDF Pag 45
    m = 2.6 * (P ** 1.187) * math.exp(-11.513 - 8.98e-5 * P)
    mu = mu_ob * ((P / Pb) ** m)
    return mu