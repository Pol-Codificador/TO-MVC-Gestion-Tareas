"""
Generador de diagramas visuales en alta resolución (PNG) para los patrones
Observer, Strategy y Command, utilizados en el informe (.docx) y en las diapositivas (.pptx).
"""
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Paleta limpia y profesional
NAVY = "#1E293B"
SLATE = "#334155"
GUINDA = "#8B1E2D"
BLUE = "#1D4ED8"
TEAL = "#0F766E"
AMBER = "#B45309"
LIGHT_BG = "#F8FAFC"
SOFT_BLUE = "#EFF6FF"
SOFT_TEAL = "#F0FDFA"
SOFT_AMBER = "#FFFBEB"
SOFT_RED = "#FEF2F2"
WHITE = "#FFFFFF"
BORDER = "#CBD5E1"


def draw_box(ax, x, y, w, h, title, subtitle, facecolor, edgecolor,
             title_color=WHITE, sub_color=WHITE, title_fs=11.5, sub_fs=8.8):
    box = patches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.02,rounding_size=0.06",
        linewidth=2.0, edgecolor=edgecolor, facecolor=facecolor, zorder=3
    )
    ax.add_patch(box)
    ax.text(x + w / 2, y + h * 0.67, title, ha="center", va="center",
            fontsize=title_fs, fontweight="bold", color=title_color, zorder=4, family="DejaVu Sans")
    ax.text(x + w / 2, y + h * 0.28, subtitle, ha="center", va="center",
            fontsize=sub_fs, color=sub_color, zorder=4, family="DejaVu Sans")


def generate_observer_diagram(output_path):
    fig, ax = plt.subplots(figsize=(10.5, 5.4), dpi=220)
    fig.patch.set_facecolor(WHITE)
    ax.set_facecolor(WHITE)
    ax.set_xlim(0, 10.5)
    ax.set_ylim(0, 5.4)
    ax.axis("off")

    ax.text(5.25, 5.05, "Patrón Observer: Sistema de Notificaciones",
            ha="center", va="center", fontsize=15, fontweight="bold", color=NAVY)

    # Sujeto
    draw_box(ax, 0.4, 1.85, 3.1, 1.85,
             "SistemaNotificaciones\n(Sujeto / Observable)",
             "- observadores: List<Observer>\n+ registrar(Observer)\n+ eliminar(Observer)\n+ notificar(mensaje)",
             BLUE, BLUE, title_fs=11.2, sub_fs=8.4)

    # Interfaz Observer
    draw_box(ax, 4.45, 2.25, 2.35, 1.1,
             "<<interface>>\nObserver",
             "+ actualizar(mensaje)",
             SOFT_BLUE, BLUE, title_color=BLUE, sub_color=NAVY, title_fs=11, sub_fs=9)

    # Observadores concretos
    users = [
        (7.75, 3.55, "Usuario: Ana", "Recibe todas las alertas"),
        (7.75, 2.25, "Usuario: Carlos", "Suscrito -> luego se desuscribe"),
        (7.75, 0.95, "Usuario: Lucía", "Recibe todas las alertas"),
    ]
    for ux, uy, utitle, usub in users:
        draw_box(ax, ux, uy, 2.35, 0.98, utitle, usub,
                 LIGHT_BG, SLATE, title_color=NAVY, sub_color=SLATE, title_fs=10.5, sub_fs=8.3)

    # Flechas
    ax.annotate("", xy=(4.40, 2.80), xytext=(3.55, 2.80),
                arrowprops=dict(arrowstyle="-|>,head_length=0.65,head_width=0.35", lw=2.2, color=BLUE, zorder=5))
    ax.text(3.98, 3.22, "notificar()\nllama a", ha="center", va="center", fontsize=8.4, fontweight="bold", color=BLUE)

    for uy_mid in [4.04, 2.74, 1.44]:
        ax.annotate("", xy=(6.84, 2.80), xytext=(7.70, uy_mid),
                    arrowprops=dict(arrowstyle="-|>,head_length=0.6,head_width=0.32", lw=1.8, ls="--", color=SLATE, zorder=5))

    ax.text(7.25, 4.42, "implementan", ha="center", va="center", fontsize=8.5, style="italic", color=SLATE)

    # Nota inferior
    note = patches.FancyBboxPatch(
        (0.4, 0.35), 6.4, 0.92,
        boxstyle="round,pad=0.02,rounding_size=0.05",
        linewidth=1.4, edgecolor=BLUE, facecolor=SOFT_BLUE, zorder=2
    )
    ax.add_patch(note)
    ax.text(3.6, 0.81,
            "Flujo clave: al llamar a notificar(), solo los usuarios en la lista reciben actualizar().\n"
            "Cuando Carlos ejecuta eliminar(carlos), deja de recibir futuros mensajes.",
            ha="center", va="center", fontsize=8.8, color=NAVY, zorder=3)

    plt.tight_layout()
    plt.savefig(output_path, dpi=220, bbox_inches="tight")
    plt.close(fig)


def generate_strategy_diagram(output_path):
    fig, ax = plt.subplots(figsize=(10.5, 5.5), dpi=220)
    fig.patch.set_facecolor(WHITE)
    ax.set_facecolor(WHITE)
    ax.set_xlim(0, 10.5)
    ax.set_ylim(0, 5.5)
    ax.axis("off")

    ax.text(5.25, 5.15, "Patrón Strategy: Calculadora con Estrategias de Promoción",
            ha="center", va="center", fontsize=15, fontweight="bold", color=NAVY)

    # Contexto
    draw_box(ax, 0.4, 2.85, 3.2, 1.75,
             "CalculadoraPrecios\n(Contexto)",
             "- estrategia: EstrategiaPromocion\n+ setEstrategia(Estrategia)\n+ calcularTotal(precio, cant)",
             TEAL, TEAL, title_fs=11.2, sub_fs=8.5)

    # Interfaz Strategy
    draw_box(ax, 4.9, 2.95, 5.1, 1.55,
             "<<interface>>  EstrategiaPromocion",
             "+ aplicarPromocion(precioUnitario, cantidad): double\n+ getDescripcion(): String",
             SOFT_TEAL, TEAL, title_color=TEAL, sub_color=NAVY, title_fs=11.5, sub_fs=9.0)

    # 4 estrategias concretas abajo
    strategies = [
        (0.4, 0.45, "SinDescuento", "Precio regular\n100% del subtotal"),
        (2.9, 0.45, "DescuentoPorcentaje", "Aplica % de rebaja\nEj: 20% menos"),
        (5.4, 0.45, "DescuentoMontoFijo", "Resta monto fijo\nEj: -S/ 75.00"),
        (7.9, 0.45, "PromocionDosPorUno", "Paga 1 de cada 2\nunidades"),
    ]
    centers_x = []
    for sx, sy, stitle, ssub in strategies:
        draw_box(ax, sx, sy, 2.2, 1.22, stitle, ssub,
                 LIGHT_BG, TEAL, title_color=NAVY, sub_color=SLATE, title_fs=9.8, sub_fs=8.3)
        cx = sx + 1.1
        centers_x.append(cx)
        ax.plot([cx, cx], [1.72, 2.18], ls="--", lw=1.7, color=TEAL, zorder=4)

    # Barra horizontal conectora (bus UML de implementación) hacia la interfaz
    ax.plot([centers_x[0], centers_x[-1]], [2.18, 2.18], ls="--", lw=1.7, color=TEAL, zorder=4)
    ax.annotate("", xy=(7.45, 2.90), xytext=(7.45, 2.18),
                arrowprops=dict(arrowstyle="-|>,head_length=0.65,head_width=0.34", lw=1.9, ls="--", color=TEAL, zorder=5))
    ax.text(8.35, 2.52, "implementan", ha="center", va="center", fontsize=8.8, style="italic", color=TEAL)

    # Conexion Contexto -> Estrategia
    ax.annotate("", xy=(4.85, 3.72), xytext=(3.65, 3.72),
                arrowprops=dict(arrowstyle="-|>,head_length=0.65,head_width=0.35", lw=2.2, color=TEAL, zorder=5))
    ax.text(4.25, 4.05, "delega", ha="center", va="center", fontsize=9.0, fontweight="bold", color=TEAL)

    # Caja intercambio en tiempo de ejecucion (sin pisar líneas)
    ax.text(2.0, 2.50, "setEstrategia() cambia la regla en tiempo real",
            ha="center", va="center", fontsize=8.6, fontweight="bold", color=GUINDA,
            bbox=dict(boxstyle="round,pad=0.28", facecolor=SOFT_RED, edgecolor=GUINDA, lw=1.2))

    plt.tight_layout()
    plt.savefig(output_path, dpi=220, bbox_inches="tight")
    plt.close(fig)


def generate_command_diagram(output_path):
    fig, ax = plt.subplots(figsize=(10.8, 5.6), dpi=220)
    fig.patch.set_facecolor(WHITE)
    ax.set_facecolor(WHITE)
    ax.set_xlim(0, 10.8)
    ax.set_ylim(0, 5.6)
    ax.axis("off")

    ax.text(5.4, 5.25, "Patrón Command: Control Remoto de Televisor (5 Funcionalidades)",
            ha="center", va="center", fontsize=14.8, fontweight="bold", color=NAVY)

    # Cliente
    draw_box(ax, 0.35, 3.55, 2.25, 1.15,
             "Main (Cliente)",
             "Crea comandos y los\nasigna al control",
             NAVY, NAVY, title_fs=10.8, sub_fs=8.4)

    # Invocador
    draw_box(ax, 0.35, 0.95, 2.25, 1.55,
             "ControlRemoto\n(Invocador)",
             "- comando: Command\n+ setCommand()\n+ presionarBoton()",
             AMBER, AMBER, title_fs=10.8, sub_fs=8.4)

    # Interfaz Command
    draw_box(ax, 3.45, 3.55, 2.95, 1.15,
             "<<interface>>\nCommand",
             "+ execute(): void",
             SOFT_AMBER, AMBER, title_color=AMBER, sub_color=NAVY, title_fs=10.8, sub_fs=9.0)

    # 5 Comandos Concretos
    cmds = [
        (3.45, 2.52, "1. EncenderTelevisorCommand"),
        (3.45, 1.97, "2. SubirVolumenCommand"),
        (3.45, 1.42, "3. CambiarCanalCommand(canal)"),
        (3.45, 0.87, "4. BajarVolumenCommand"),
        (3.45, 0.32, "5. ApagarTelevisorCommand"),
    ]
    for cx, cy, ctitle in cmds:
        box = patches.FancyBboxPatch(
            (cx, cy), 3.25, 0.43,
            boxstyle="round,pad=0.015,rounding_size=0.04",
            linewidth=1.4, edgecolor=AMBER, facecolor=LIGHT_BG, zorder=3
        )
        ax.add_patch(box)
        ax.text(cx + 1.625, cy + 0.215, ctitle, ha="center", va="center",
                fontsize=8.8, fontweight="bold", color=NAVY, zorder=4)

    # Receptor Televisor
    draw_box(ax, 7.65, 1.10, 2.8, 2.45,
             "Televisor\n(Receptor)",
             "Acciones reales:\n• encender()\n• apagar()\n• subirVolumen()\n• bajarVolumen()\n• cambiarCanal(n)",
             GUINDA, GUINDA, title_fs=11.5, sub_fs=8.8)

    # Cliente -> Control (etiqueta a la izquierda)
    ax.annotate("", xy=(1.47, 2.55), xytext=(1.47, 3.50),
                arrowprops=dict(arrowstyle="-|>,head_length=0.55,head_width=0.3", lw=1.9, color=NAVY, zorder=5))
    ax.text(1.33, 3.03, "configura", ha="right", va="center", fontsize=8.5, color=NAVY, fontweight="bold")

    # Control -> Command (etiqueta limpia en el espacio central)
    ax.annotate("", xy=(3.40, 4.05), xytext=(2.65, 1.95),
                arrowprops=dict(arrowstyle="-|>,head_length=0.6,head_width=0.32", lw=2.0, color=AMBER, zorder=5))
    ax.text(2.90, 3.12, "execute()", ha="center", va="center", fontsize=8.8, fontweight="bold",
            color=AMBER, bbox=dict(boxstyle="round,pad=0.2", facecolor=WHITE, edgecolor=AMBER, lw=1.0), zorder=6)

    # Comandos -> Interfaz Command (vertical)
    ax.annotate("", xy=(4.92, 3.50), xytext=(4.92, 3.00),
                arrowprops=dict(arrowstyle="-|>,head_length=0.55,head_width=0.3", lw=1.7, ls="--", color=AMBER, zorder=5))
    ax.text(5.72, 3.24, "implementan", ha="center", va="center", fontsize=8.4, style="italic", color=SLATE)

    # Comandos -> Televisor
    for cy in [2.73, 2.18, 1.63, 1.08, 0.53]:
        ax.annotate("", xy=(7.60, 2.32), xytext=(6.75, cy),
                    arrowprops=dict(arrowstyle="-|>,head_length=0.55,head_width=0.28", lw=1.5, color=GUINDA, zorder=5))
    ax.text(7.15, 3.10, "invocan\nacción", ha="center", va="center", fontsize=8.4, fontweight="bold", color=GUINDA)

    plt.tight_layout()
    plt.savefig(output_path, dpi=220, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    base = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.path.join(base, "diagramas")
    os.makedirs(out_dir, exist_ok=True)
    generate_observer_diagram(os.path.join(out_dir, "diagrama_observer.png"))
    generate_strategy_diagram(os.path.join(out_dir, "diagrama_strategy.png"))
    generate_command_diagram(os.path.join(out_dir, "diagrama_command.png"))
    print("Diagramas generados correctamente en:", out_dir)
