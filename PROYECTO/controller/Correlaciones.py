import xlwings as xw
import numpy as np
import math
from PROYECTO.model import funciones
from PROYECTO.model import graficas


def main():
    # 1. CONEXIÓN CON EXCEL
    wb = xw.Book.caller()
    sheet = wb.sheets[0]

    try:
        # ---------------------------------------------------------
        # 2. LECTURA DE DATOS (INPUTS)
        # Mapeo exacto según tu imagen (Rango B4:B10)
        # ---------------------------------------------------------

        # B4: Presión de burbuja (Pb)
        Pb = sheet.range('B4').value

        # B5: Relación Gas-Petróleo en burbuja (Rsb)
        Rsb = sheet.range('B5').value

        # B6: Gravedad API
        API = sheet.range('B6').value

        # B7: Gravedad específica del gas (SGgas / yg)
        yg = sheet.range('B7').value

        # B8: Presión del reservorio (Pr)
        P_res = sheet.range('B8').value

        # B9: Temperatura (T) en Fahrenheit
        T = sheet.range('B9').value

        # B10: Presión Atmosférica (Patm)
        P_atm = sheet.range('B10').value

        # Validación: Verificar que no falte ningún dato
        if None in [Pb, Rsb, API, yg, P_res, T, P_atm]:
            sheet.range('D4').value = "Error: Faltan datos en el rango B4:B10"
            return

        # ---------------------------------------------------------
        # 3. CÁLCULOS PREVIOS
        # ---------------------------------------------------------

        # Calcular Gravedad específica del petróleo (yo) usando el API (B6)
        yo = 141.5 / (131.5 + API)

        # Generar barrido de presiones desde Patm (B10) hasta Pr (B8)
        # Agregamos 500 psi extra para ver la tendencia más allá de Pr si se desea
        presiones = np.linspace(P_atm, P_res + 200, 60)

        valores_rs = []
        valores_bo = []
        valores_mu = []

        # Calculamos propiedades base en el punto de burbuja (Pb)
        # para usarlas como referencia en la zona subsaturada
        Bob = funciones.standing_bo_saturado(Rsb, yg, yo, T)
        mu_od = funciones.beggs_robinson_mu_dead(API, T)
        mu_ob = funciones.beggs_robinson_mu_saturado(mu_od, Rsb)

        # ---------------------------------------------------------
        # 4. BUCLE DE CÁLCULO (Propiedades vs Presión)
        # ---------------------------------------------------------
        for p in presiones:

            # === ZONA SATURADA (Presión < Pb) ===
            if p < Pb:
                # 1. Rs varía (Standing)
                rs_calc = funciones.standing_rs(p, yg, API, T)

                # 2. Bo saturado
                bo_calc = funciones.standing_bo_saturado(rs_calc, yg, yo, T)

                # 3. Viscosidad saturada
                mu_calc = funciones.beggs_robinson_mu_saturado(mu_od, rs_calc)

            # === ZONA SUBSATURADA (Presión >= Pb) ===
            else:
                # 1. Rs constante (igual a Rsb de la celda B5)
                rs_calc = Rsb

                # 2. Calcular Compresibilidad (Co) instantánea
                co_calc = funciones.vasquez_beggs_co(Rsb, yg, API, T, p)

                # 3. Bo Subsaturado (Comprimiendo desde Bob)
                bo_calc = funciones.bo_subsaturado(Bob, co_calc, Pb, p)

                # 4. Viscosidad Subsaturada
                mu_calc = funciones.vasquez_beggs_mu_subsaturado(mu_ob, p, Pb)

            # Guardar datos
            valores_rs.append(rs_calc)
            valores_bo.append(bo_calc)
            valores_mu.append(mu_calc)

        # ---------------------------------------------------------
        # 5. GENERACIÓN DE GRÁFICAS
        # ---------------------------------------------------------

        # Gráfica Rs
        fig_rs = graficas.crear_grafica_propiedad(
            presiones, valores_rs, Pb, "Rs (scf/STB)", "Solubilidad vs Presión"
        )

        # Gráfica Bo
        fig_bo = graficas.crear_grafica_propiedad(
            presiones, valores_bo, Pb, "Bo (bbl/STB)", "Factor Vol. vs Presión"
        )

        # Gráfica Viscosidad
        fig_mu = graficas.crear_grafica_propiedad(
            presiones, valores_mu, Pb, "Mu (cp)", "Viscosidad vs Presión"
        )

        # ---------------------------------------------------------
        # 6. SALIDA A EXCEL
        # ---------------------------------------------------------

        def pegar_grafica(figura, nombre, celda_ref):
            # Limpiar gráfica anterior si existe
            if sheet.pictures.count > 0:
                try:
                    sheet.pictures[nombre].delete()
                except:
                    pass

            # Pegar nueva gráfica
            sheet.pictures.add(
                figura,
                name=nombre,
                update=True,
                left=sheet.range(celda_ref).left,
                top=sheet.range(celda_ref).top,
                scale=0.8
            )

        # Ubicación de las gráficas (Columna E, a la derecha de tus datos)
        pegar_grafica(fig_rs, 'Plot_Rs', 'E4')
        pegar_grafica(fig_bo, 'Plot_Bo', 'E23')
        pegar_grafica(fig_mu, 'Plot_Mu', 'M4')

        sheet.range('D4').value = "Cálculo Finalizado Correctamente"

    except Exception as e:
        sheet.range('D4').value = f"Error: {str(e)}"


if __name__ == "__main__":
    xw.Book("TuArchivo.xlsm").set_mock_caller()
    main()