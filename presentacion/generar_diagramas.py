"""
Generador de diagramas arquitectónicos MVC en alta resolución (PNG)
para incluir en la presentación (.pptx) y en el informe académico (.docx).
"""
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Paleta corporativa/académica (Rojo carmesí, gris oscuro, blanco)
CRIMSON = "#9B1B30"
DARK_BG = "#1F242D"
SLATE = "#334155"
LIGHT_GRAY = "#F4F6F9"
BORDER_GRAY = "#CBD5E1"
WHITE = "#FFFFFF"
ACCENT_BLUE = "#1D4ED8"
ACCENT_TEAL = "#0F766E"


def draw_box(ax, x, y, w, h, title, subtitle, facecolor, edgecolor, title_color=WHITE, sub_color=WHITE):
    box = patches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.02,rounding_size=0.03",
        linewidth=2, edgecolor=edgecolor, facecolor=facecolor, zorder=3
    )
    ax.add_patch(box)
    ax.text(x + w / 2, y + h * 0.65, title, ha="center", va="center",
            fontsize=13, fontweight="bold", color=title_color, zorder=4, family="DejaVu Sans")
    ax.text(x + w / 2, y + h * 0.28, subtitle, ha="center", va="center",
            fontsize=9.5, color=sub_color, zorder=4, family="DejaVu Sans")


def generate_mvc_flow(output_path):
    fig, ax = plt.subplots(figsize=(10, 5.2), dpi=220)
    fig.patch.set_facecolor(WHITE)
    ax.set_facecolor(WHITE)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.2)
    ax.axis("off")

    ax.text(5.0, 4.85, "Flujo Arquitectónico Modelo - Vista - Controlador (MVC)",
            ha="center", va="center", fontsize=15, fontweight="bold", color=DARK_BG)

    # Usuario
    draw_box(ax, 0.3, 1.85, 1.8, 1.4, "USUARIO", "Interactúa vía\nconsola / menú",
             DARK_BG, DARK_BG)

    # Controlador
    draw_box(ax, 3.3, 1.85, 2.5, 1.4, "CONTROLADOR", "TaskController\nRecibe acciones y coordina",
             CRIMSON, CRIMSON)

    # Modelo
    draw_box(ax, 7.1, 3.1, 2.5, 1.3, "MODELO", "Task (+ Repository)\nDatos y lógica de estado",
             SLATE, SLATE)

    # Vista
    draw_box(ax, 7.1, 0.7, 2.5, 1.3, "VISTA", "TaskView\nFormatea y muestra salida",
             LIGHT_GRAY, CRIMSON, title_color=CRIMSON, sub_color=DARK_BG)

    arrow_kw = dict(arrowstyle="-|>,head_length=0.7,head_width=0.4", lw=2.0, color=DARK_BG, zorder=5)
    arrow_red = dict(arrowstyle="-|>,head_length=0.7,head_width=0.4", lw=2.0, color=CRIMSON, zorder=5)

    # 1. Usuario -> Controlador
    ax.annotate("", xy=(3.25, 2.75), xytext=(2.15, 2.75), arrowprops=arrow_red)
    ax.text(2.7, 3.05, "1. Solicita\nacción", ha="center", va="center", fontsize=8.5, fontweight="bold", color=CRIMSON)

    # 2. Controlador -> Modelo
    ax.annotate("", xy=(7.05, 3.85), xytext=(5.85, 2.95), arrowprops=arrow_kw)
    ax.text(6.15, 3.72, "2. Actualiza /\nconsulta datos", ha="center", va="center", fontsize=8.5, color=DARK_BG)

    # 3. Modelo -> Controlador
    ax.annotate("", xy=(5.85, 2.65), xytext=(7.05, 3.45), arrowprops=dict(arrowstyle="-|>,head_length=0.7,head_width=0.4", lw=1.8, ls="--", color=SLATE, zorder=5))
    ax.text(6.75, 2.85, "3. Retorna\nresultado", ha="center", va="center", fontsize=8.2, color=SLATE)

    # 4. Controlador -> Vista
    ax.annotate("", xy=(7.05, 1.45), xytext=(5.85, 2.2), arrowprops=arrow_red)
    ax.text(6.2, 1.45, "4. Envía datos\na mostrar", ha="center", va="center", fontsize=8.5, fontweight="bold", color=CRIMSON)

    # 5. Vista -> Usuario (curva inferior)
    ax.annotate("", xy=(1.2, 1.8), xytext=(7.1, 0.95),
                arrowprops=dict(arrowstyle="-|>,head_length=0.7,head_width=0.4", lw=2.0,
                                connectionstyle="arc3,rad=-0.22", color=ACCENT_TEAL, zorder=5))
    ax.text(4.2, 0.32, "5. Presenta resultados y mensajes al usuario", ha="center", va="center",
            fontsize=9, fontweight="bold", color=ACCENT_TEAL)

    plt.tight_layout()
    plt.savefig(output_path, dpi=220, bbox_inches="tight")
    plt.close(fig)


def generate_act2_architecture(output_path):
    fig, ax = plt.subplots(figsize=(10, 5.4), dpi=220)
    fig.patch.set_facecolor(WHITE)
    ax.set_facecolor(WHITE)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.4)
    ax.axis("off")

    ax.text(5.0, 5.05, "Arquitectura MVC Escalada - Actividad 2 (Con Capa de Persistencia)",
            ha="center", va="center", fontsize=14.5, fontweight="bold", color=DARK_BG)

    # Main
    draw_box(ax, 0.3, 2.2, 1.7, 1.2, "Main.java", "Punto de entrada\nEnsambla MVC", DARK_BG, DARK_BG)

    # Controller
    draw_box(ax, 2.6, 1.9, 2.5, 1.8, "TaskController", "CRUD completo\nFiltros y búsqueda\nEstadísticas y flujo", CRIMSON, CRIMSON)

    # View
    draw_box(ax, 2.6, 0.25, 2.5, 1.1, "TaskView", "Menú interactivo, tabla,\nbarras y lectura segura", LIGHT_GRAY, CRIMSON, title_color=CRIMSON, sub_color=DARK_BG)

    # Model container
    model_bg = patches.FancyBboxPatch(
        (5.7, 0.25), 4.0, 4.3,
        boxstyle="round,pad=0.04,rounding_size=0.05",
        linewidth=2, edgecolor=SLATE, facecolor="#F8FAFC", linestyle="--", zorder=1
    )
    ax.add_patch(model_bg)
    ax.text(7.7, 4.35, "CAPA DE MODELO Y PERSISTENCIA", ha="center", va="center",
            fontsize=10, fontweight="bold", color=SLATE, zorder=2)

    # Task
    draw_box(ax, 6.0, 2.85, 1.75, 1.2, "Task.java", "id, name, desc\npriority, createdAt", SLATE, SLATE)
    # Priority
    draw_box(ax, 8.0, 2.85, 1.45, 1.2, "Priority", "Enum:\nALTA / MEDIA\nBAJA", ACCENT_BLUE, ACCENT_BLUE)
    # Repository
    draw_box(ax, 6.0, 1.4, 3.45, 1.05, "TaskRepository.java (SRP)", "Guarda y carga CSV en UTF-8\nManejo seguro de IOException", ACCENT_TEAL, ACCENT_TEAL)
    # File
    draw_box(ax, 6.65, 0.4, 2.15, 0.72, "tareas.csv", "Persistencia en disco", LIGHT_GRAY, ACCENT_TEAL, title_color=ACCENT_TEAL, sub_color=DARK_BG)

    arrow_kw = dict(arrowstyle="-|>,head_length=0.6,head_width=0.35", lw=1.9, color=DARK_BG, zorder=5)
    arrow_bi = dict(arrowstyle="<->,head_length=0.5,head_width=0.3", lw=1.9, color=CRIMSON, zorder=5)

    # Main -> Controller
    ax.annotate("", xy=(2.55, 2.8), xytext=(2.05, 2.8), arrowprops=arrow_kw)
    # Controller <-> View
    ax.annotate("", xy=(3.85, 1.88), xytext=(3.85, 1.38), arrowprops=arrow_bi)
    # Controller -> Task
    ax.annotate("", xy=(5.95, 3.45), xytext=(5.15, 3.1), arrowprops=arrow_kw)
    # Task -> Priority
    ax.annotate("", xy=(7.95, 3.45), xytext=(7.78, 3.45), arrowprops=arrow_kw)
    # Controller -> Repository
    ax.annotate("", xy=(5.95, 1.95), xytext=(5.15, 2.45), arrowprops=arrow_kw)
    # Repository <-> tareas.csv
    ax.annotate("", xy=(7.72, 1.38), xytext=(7.72, 1.14), arrowprops=dict(arrowstyle="<->,head_length=0.5,head_width=0.3", lw=1.9, color=ACCENT_TEAL, zorder=5))

    plt.tight_layout()
    plt.savefig(output_path, dpi=220, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    out_dir = os.path.dirname(os.path.abspath(__file__))
    generate_mvc_flow(os.path.join(out_dir, "diagrama_mvc_flujo.png"))
    generate_act2_architecture(os.path.join(out_dir, "diagrama_arquitectura_act2.png"))
    print("Diagramas generados exitosamente.")
