import matplotlib.pyplot as plt


def crear_grafica_propiedad(presiones, valores, Pb, nombre_y, titulo):
    # Crear figura y ejes
    fig, ax = plt.subplots(figsize=(7, 4.5))

    # 1. Graficar la curva principal (Datos)
    ax.plot(presiones, valores, linewidth=2, color='blue', label=nombre_y)

    # 2. Agregar línea vertical roja en el Pb
    # axvline = Axis Vertical Line
    ax.axvline(x=Pb, color='red', linestyle='--', linewidth=1.5, label=f'Pb = {Pb} psi')

    # 3. Estética (Títulos, Grid, Leyenda)
    ax.set_title(titulo, fontsize=11, fontweight='bold')
    ax.set_xlabel("Presión (psia)")
    ax.set_ylabel(nombre_y)
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.legend()

    # Ajustar márgenes para que no se corte nada
    plt.tight_layout()

    return fig