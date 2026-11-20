"""
Generador de Presentación PowerPoint (.pptx) - Laboratorio MVC
Curso: Tecnología de Objetos (TO)
Docente: Mg. Diego Alonso Iquira Becerra

Produce: Presentacion_MVC_Tareas.pptx (15 diapositivas widescreen 16:9)
con diseño corporativo/académico (carmesí, carbón, blanco), diagramas visuales,
bloques de código con fuente monoespaciada y Notas del Orador en cada diapositiva.
"""
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# Paleta de colores corporativa/académica
CRIMSON = RGBColor(0x9B, 0x1B, 0x30)
DARK_CHARCOAL = RGBColor(0x1F, 0x24, 0x2D)
SLATE = RGBColor(0x33, 0x41, 0x55)
CODE_BG = RGBColor(0x1E, 0x29, 0x3B)
CODE_TEXT = RGBColor(0xF1, 0xF5, 0xF9)
CARD_BG = RGBColor(0xF4, 0xF6, 0xF9)
BORDER_GRAY = RGBColor(0xCB, 0xD5, 0xE1)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
MUTED_TEXT = RGBColor(0x64, 0x74, 0x8B)
TEAL = RGBColor(0x0F, 0x76, 0x6E)
SOFT_RED = RGBColor(0xFD, 0xED, 0xF0)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRES_DIR = os.path.dirname(os.path.abspath(__file__))


def read_text_safe(path, fallback=""):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read().strip()
    return fallback


def add_notes(slide, text):
    notes_slide = slide.notes_slide
    tf = notes_slide.notes_text_frame
    tf.text = text


def add_header_and_footer(slide, title_text, subtitle_text, slide_num, total_slides=15):
    # Barra superior carmesí
    top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.12))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = CRIMSON
    top_bar.line.fill.background()

    # Título
    tb = slide.shapes.add_textbox(Inches(0.6), Inches(0.25), Inches(12.1), Inches(0.55))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.name = "Segoe UI"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = DARK_CHARCOAL

    # Subtítulo
    if subtitle_text:
        stb = slide.shapes.add_textbox(Inches(0.6), Inches(0.80), Inches(12.1), Inches(0.32))
        stf = stb.text_frame
        stf.word_wrap = True
        stf.margin_left = stf.margin_top = stf.margin_right = stf.margin_bottom = 0
        sp = stf.paragraphs[0]
        sp.text = subtitle_text
        sp.font.name = "Segoe UI"
        sp.font.size = Pt(12.5)
        sp.font.color.rgb = CRIMSON

    # Línea divisoria
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(1.16), Inches(12.133), Inches(0.02))
    line.fill.solid()
    line.fill.fore_color.rgb = BORDER_GRAY
    line.line.fill.background()

    # Pie de página
    ftb = slide.shapes.add_textbox(Inches(0.6), Inches(7.08), Inches(9.5), Inches(0.28))
    ftf = ftb.text_frame
    fp = ftf.paragraphs[0]
    fp.text = "Tecnología de Objetos (TO)  |  Patrón Arquitectónico MVC en Java  |  Mg. Diego Alonso Iquira Becerra"
    fp.font.name = "Segoe UI"
    fp.font.size = Pt(9.5)
    fp.font.color.rgb = MUTED_TEXT

    ntb = slide.shapes.add_textbox(Inches(11.3), Inches(7.08), Inches(1.433), Inches(0.28))
    ntf = ntb.text_frame
    np = ntf.paragraphs[0]
    np.text = f"{slide_num} / {total_slides}"
    np.alignment = PP_ALIGN.RIGHT
    np.font.name = "Segoe UI"
    np.font.size = Pt(9.5)
    np.font.bold = True
    np.font.color.rgb = CRIMSON


def add_card(slide, x, y, w, h, title=None, bullets=None, bg_color=CARD_BG, border_color=BORDER_GRAY, title_color=CRIMSON, font_size=12.5):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    shape.adjustments[0] = 0.04
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    shape.line.color.rgb = border_color
    shape.line.width = Pt(1.2)

    tf = shape.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.2)
    tf.margin_right = Inches(0.2)
    tf.margin_top = Inches(0.15)
    tf.margin_bottom = Inches(0.12)
    tf.vertical_anchor = MSO_ANCHOR.TOP

    first = True
    if title:
        p = tf.paragraphs[0]
        p.text = title
        p.font.name = "Segoe UI"
        p.font.size = Pt(14.5)
        p.font.bold = True
        p.font.color.rgb = title_color
        p.space_after = Pt(6)
        first = False

    if bullets:
        for b in bullets:
            p = tf.paragraphs[0] if first else tf.add_paragraph()
            first = False
            p.text = f"•  {b}" if not b.startswith("•") and not b.startswith("✔") and not b.startswith("✖") else b
            p.font.name = "Segoe UI"
            p.font.size = Pt(font_size)
            p.font.color.rgb = DARK_CHARCOAL
            p.space_after = Pt(5)
    return shape


def add_code_box(slide, x, y, w, h, title, code_text, font_size=10.0):
    # Contenedor oscuro
    box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    box.adjustments[0] = 0.03
    box.fill.solid()
    box.fill.fore_color.rgb = CODE_BG
    box.line.color.rgb = SLATE
    box.line.width = Pt(1)

    # Barra superior del bloque de código
    hdr = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(0.32))
    hdr.fill.solid()
    hdr.fill.fore_color.rgb = CRIMSON
    hdr.line.fill.background()
    htf = hdr.text_frame
    htf.margin_left = Inches(0.15)
    htf.margin_top = Inches(0.03)
    hp = htf.paragraphs[0]
    hp.text = title
    hp.font.name = "Consolas"
    hp.font.size = Pt(10.5)
    hp.font.bold = True
    hp.font.color.rgb = WHITE

    # Área de código
    tb = slide.shapes.add_textbox(Inches(x + 0.14), Inches(y + 0.38), Inches(w - 0.28), Inches(h - 0.44))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for idx, line in enumerate(code_text.splitlines()):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.text = line
        p.font.name = "Consolas"
        p.font.size = Pt(font_size)
        p.font.color.rgb = CODE_TEXT
        p.space_after = Pt(1)


def build_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Leer salidas reales de ejecución
    act1_out = read_text_safe(os.path.join(BASE_DIR, "actividad 1", "salida_actividad1.txt"), "(Ejecutar Actividad 1 para ver salida)")
    act2_out = read_text_safe(os.path.join(BASE_DIR, "actividad 2", "salida_actividad2.txt"), "(Ejecutar Actividad 2 para ver salida)")
    csv_out = read_text_safe(os.path.join(BASE_DIR, "actividad 2", "tareas.csv"), "(tareas.csv)")

    # =========================================================================
    # SLIDE 1: PORTADA
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = DARK_CHARCOAL
    bg.line.fill.background()

    # Franja lateral carmesí
    side = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.45), Inches(7.5))
    side.fill.solid()
    side.fill.fore_color.rgb = CRIMSON
    side.line.fill.background()

    # Etiqueta curso
    badge = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.1), Inches(1.1), Inches(4.5), Inches(0.48))
    badge.fill.solid()
    badge.fill.fore_color.rgb = CRIMSON
    badge.line.fill.background()
    bp = badge.text_frame.paragraphs[0]
    bp.text = "PRÁCTICA DE LABORATORIO  •  TECNOLOGÍA DE OBJETOS"
    bp.alignment = PP_ALIGN.CENTER
    bp.font.name = "Segoe UI"
    bp.font.size = Pt(11)
    bp.font.bold = True
    bp.font.color.rgb = WHITE

    # Título principal
    tb = s1.shapes.add_textbox(Inches(1.1), Inches(1.85), Inches(11.2), Inches(1.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Patrón Arquitectónico\nModelo - Vista - Controlador (MVC)"
    p.font.name = "Segoe UI"
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = WHITE

    p2 = tf.add_paragraph()
    p2.text = "Implementación en Java: Gestor de Tareas Base (Actividad 1) y Sistema Escalado con Persistencia (Actividad 2)"
    p2.font.name = "Segoe UI"
    p2.font.size = Pt(16.5)
    p2.font.color.rgb = BORDER_GRAY
    p2.space_before = Pt(12)

    # Caja de metadatos
    meta = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.1), Inches(4.75), Inches(11.1), Inches(1.95))
    meta.adjustments[0] = 0.05
    meta.fill.solid()
    meta.fill.fore_color.rgb = SLATE
    meta.line.color.rgb = CRIMSON
    meta.line.width = Pt(1.5)
    mtf = meta.text_frame
    mtf.margin_left = Inches(0.3)
    mtf.margin_top = Inches(0.2)
    info_lines = [
        ("Docente: ", "Mg. Diego Alonso Iquira Becerra"),
        ("Curso: ", "Tecnología de Objetos (TO)"),
        ("Integrantes: ", "[Apellidos y Nombres del Estudiante / Grupo]"),
        ("Fecha: ", "Noviembre 2026")
    ]
    for i, (k, v) in enumerate(info_lines):
        mp = mtf.paragraphs[0] if i == 0 else mtf.add_paragraph()
        r1 = mp.add_run()
        r1.text = k
        r1.font.name = "Segoe UI"
        r1.font.size = Pt(14)
        r1.font.bold = True
        r1.font.color.rgb = WHITE
        r2 = mp.add_run()
        r2.text = v
        r2.font.name = "Segoe UI"
        r2.font.size = Pt(14)
        r2.font.color.rgb = BORDER_GRAY
        mp.space_after = Pt(5)

    add_notes(s1, (
        "QUÉ DECIR EN ESTA DIAPOSITIVA:\n"
        "Buenos días/tardes profesor y compañeros. Hoy presentaremos nuestra práctica de laboratorio del curso de "
        "Tecnología de Objetos sobre el Patrón Arquitectónico Modelo-Vista-Controlador (MVC) implementado en Java.\n"
        "Veremos primero qué es MVC con una analogía sencilla, luego revisaremos la Actividad 1 (versión base) y "
        "finalmente la Actividad 2 (versión mejorada con edición, eliminación, filtros, estadísticas y guardado en archivo)."
    ))

    # =========================================================================
    # SLIDE 2: ¿QUÉ SON LOS PATRONES Y QUÉ ES MVC?
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header_and_footer(s2, "¿Qué son los Patrones y qué es MVC?", "Conceptos fundamentales explicados de forma simple", 2)

    add_card(s2, 0.6, 1.4, 5.9, 2.55, "Patrón Arquitectónico vs. Patrón de Diseño", [
        "Patrón de Diseño: solución puntual a nivel de clases/objetos (ej. Singleton, Factory).",
        "Patrón Arquitectónico: define la estructura global del sistema y cómo se separan sus capas.",
        "MVC (Modelo-Vista-Controlador) separa los datos, la interfaz de usuario y la lógica de coordinación."
    ])

    add_card(s2, 0.6, 4.15, 5.9, 2.7, "¿Por qué separar el código en 3 capas?", [
        "Mantenibilidad: cambiar cómo se muestra un dato (Vista) no rompe la lógica del Modelo.",
        "Reutilización: el mismo Modelo puede usarse en consola, escritorio o web.",
        "Trabajo en equipo: un programador diseña la Vista mientras otro desarrolla el Modelo."
    ])

    add_card(s2, 6.8, 1.4, 5.93, 5.45, "Analogía de la vida real: Un Restaurante", [
        "CLIENTE (Usuario): decide qué plato quiere pedir y lo recibe servido en su mesa.",
        "MESERO (Controlador): recibe el pedido del cliente, lo lleva a la cocina y trae el resultado. No cocina ni lava platos.",
        "COCINA (Modelo): guarda los ingredientes (datos) y prepara la comida según las recetas (reglas de negocio).",
        "PLATO PRESENTADO / MENÚ (Vista): es lo único que ve el cliente; muestra la información de forma agradable y ordenada.",
        "Conclusión: si el restaurante cambia el diseño del menú (Vista), la cocina (Modelo) sigue funcionando exactamente igual."
    ], bg_color=SOFT_RED, border_color=CRIMSON)

    add_notes(s2, (
        "QUÉ DECIR EN ESTA DIAPOSITIVA:\n"
        "Antes de ver código, entendamos qué es MVC. Un patrón arquitectónico es como el plano de un edificio: "
        "organiza las grandes partes del software. MVC divide un programa en 3 piezas: Modelo, Vista y Controlador.\n"
        "La mejor forma de recordarlo es con un restaurante: tú eres el Usuario, el Mesero es el Controlador que "
        "lleva y trae pedidos, la Cocina es el Modelo donde están los datos y la preparación, y el Plato servido o la Carta "
        "es la Vista. Gracias a esta separación, si cambiamos la interfaz (consola a ventana), no tenemos que reescribir los datos."
    ))

    # =========================================================================
    # SLIDE 3: ARQUITECTURA MVC VISUAL
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header_and_footer(s3, "Arquitectura MVC: Flujo de Comunicación", "Cómo interactúan el Usuario, Controlador, Modelo y Vista paso a paso", 3)

    img_mvc = os.path.join(PRES_DIR, "diagrama_mvc_flujo.png")
    if os.path.exists(img_mvc):
        s3.shapes.add_picture(img_mvc, Inches(0.6), Inches(1.35), width=Inches(8.2))

    add_card(s3, 9.0, 1.35, 3.73, 5.45, "Paso a paso del flujo", [
        "1. El Usuario ejecuta una acción (ej. añadir o completar tarea).",
        "2. El Controlador valida la entrada y llama al Modelo.",
        "3. El Modelo actualiza su estado interno o devuelve datos.",
        "4. El Controlador pasa los datos actualizados a la Vista.",
        "5. La Vista formatea y muestra el resultado en pantalla."
    ], font_size=12)

    add_notes(s3, (
        "QUÉ DECIR EN ESTA DIAPOSITIVA:\n"
        "En este diagrama vemos el ciclo completo de MVC. Noten algo clave: la Vista y el Modelo no se mezclan. "
        "Todo pasa por el Controlador. Por ejemplo, cuando el usuario quiere completar una tarea, el Controlador verifica "
        "que el índice exista, le pide al Modelo que cambie su estado a completada, y luego le indica a la Vista que imprima "
        "el mensaje de confirmación."
    ))

    # =========================================================================
    # SLIDE 4: ACTIVIDAD 1 - OBJETIVO Y ESTRUCTURA
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header_and_footer(s4, "Actividad 1: Objetivo y Estructura del Proyecto Base", "Implementación mínima y limpia del patrón MVC en Java", 4)

    add_card(s4, 0.6, 1.4, 12.13, 1.15, "Objetivo de la Actividad 1", [
        "Construir un gestor de tareas en consola que demuestre la separación estricta entre Modelo, Vista y Controlador, permitiendo añadir tareas, listarlas y marcarlas como completadas con validación de índices."
    ], bg_color=SOFT_RED, border_color=CRIMSON)

    cards_a1 = [
        ("1. Task.java\n(Modelo)", [
            "Atributos privados: name (String) y completed (boolean).",
            "Constructor inicia completed en false.",
            "Métodos: getName(), isCompleted(), complete()."
        ]),
        ("2. TaskView.java\n(Vista)", [
            "Solo imprime información en consola.",
            "printTasks(List<Task>): muestra índice, nombre y estado.",
            "printMessage(String): muestra avisos o errores."
        ]),
        ("3. TaskController.java\n(Controlador)", [
            "Administra la lista de tareas y la referencia a TaskView.",
            "addTask(): crea tarea y notifica.",
            "completeTask(index): valida índice y actualiza."
        ]),
        ("4. Main.java\n(Aplicación)", [
            "Punto de entrada del programa.",
            "Instancia Vista y Controlador.",
            "Ejecuta una secuencia de prueba completa."
        ])
    ]
    for i, (t, bl) in enumerate(cards_a1):
        add_card(s4, 0.6 + i * 3.08, 2.8, 2.9, 4.05, t, bl, font_size=11.8)

    add_notes(s4, (
        "QUÉ DECIR EN ESTA DIAPOSITIVA:\n"
        "La Actividad 1 consta de solo 4 archivos Java en la carpeta 'actividad 1/'. Cada archivo tiene una única "
        "responsabilidad: Task guarda los datos de una tarea, TaskView solo imprime en pantalla, TaskController coordina "
        "las acciones y valida errores, y Main simplemente arranca el programa para demostrar su funcionamiento."
    ))

    # =========================================================================
    # SLIDE 5: ACTIVIDAD 1 - MODELO (Task.java)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header_and_footer(s5, "Actividad 1 — Modelo (Task.java)", "Encapsulamiento de datos y comportamiento de una tarea", 5)

    code_task1 = """public class Task {
    private String name;
    private boolean completed;

    public Task(String name) {
        this.name = name;
        this.completed = false;
    }

    public String getName() {
        return name;
    }

    public boolean isCompleted() {
        return completed;
    }

    public void complete() {
        this.completed = true;
    }
}"""
    add_code_box(s5, 0.6, 1.4, 6.4, 5.4, "actividad 1/Task.java", code_task1, font_size=11)

    add_card(s5, 7.25, 1.4, 5.48, 5.4, "Explicación bloque por bloque", [
        "Atributos privados (Encapsulamiento): nadie fuera de la clase puede alterar name o completed directamente.",
        "Constructor Task(String name): toda tarea nace automáticamente como 'Pendiente' (completed = false).",
        "Getters (getName / isCompleted): permiten leer el estado de la tarea de forma segura.",
        "Método complete(): cambia el estado a true. Es una regla de negocio propia del Modelo.",
        "Independencia total: Task.java no tiene ningún System.out.println; no sabe ni le importa cómo se muestra."
    ])

    add_notes(s5, (
        "QUÉ DECIR EN ESTA DIAPOSITIVA:\n"
        "Aquí vemos el Modelo: la clase Task.java. Es muy limpia porque solo guarda dos datos privados: el nombre y si está "
        "completada o no. Al crearla, siempre empieza en falso (pendiente). Fíjense que aquí NO hay impresiones en consola; "
        "eso garantiza que el Modelo sea 100% independiente de la interfaz."
    ))

    # =========================================================================
    # SLIDE 6: ACTIVIDAD 1 - VISTA (TaskView.java)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header_and_footer(s6, "Actividad 1 — Vista (TaskView.java)", "Presentación pura al usuario sin lógica de negocio", 6)

    code_view1 = """import java.util.List;

public class TaskView {
    public void printTasks(List<Task> tasks) {
        System.out.println("\\n=== LISTA DE TAREAS ===");
        if (tasks == null || tasks.isEmpty()) {
            System.out.println("No hay tareas registradas.");
        } else {
            for (int i = 0; i < tasks.size(); i++) {
                Task task = tasks.get(i);
                String status = task.isCompleted()
                                ? "Completada" : "Pendiente";
                System.out.printf("[%d] %s - Estado: %s%n",
                                  i, task.getName(), status);
            }
        }
    }

    public void printMessage(String message) {
        System.out.println(">> " + message);
    }
}"""
    add_code_box(s6, 0.6, 1.4, 6.7, 5.4, "actividad 1/TaskView.java", code_view1, font_size=10.5)

    add_card(s6, 7.55, 1.4, 5.18, 5.4, "¿Qué hace y por qué es así?", [
        "printTasks(List<Task>): recorre la lista, traduce el booleano true/false a texto legible ('Completada' o 'Pendiente') y muestra el índice.",
        "printMessage(String): centraliza cualquier aviso de éxito o error.",
        "Sin lógica de negocio: la Vista nunca agrega ni completa tareas; solo recibe datos listos para mostrar.",
        "Beneficio práctico: si mañana quisiéramos usar una ventana gráfica (JavaFX/Swing), solo reemplazaríamos esta clase."
    ])

    add_notes(s6, (
        "QUÉ DECIR EN ESTA DIAPOSITIVA:\n"
        "TaskView es nuestra Vista. Su único trabajo es formatear y mostrar texto en consola. Convierte el valor booleano "
        "true o false en las palabras 'Completada' o 'Pendiente' para que sea amigable al usuario. No modifica la lista de "
        "tareas porque eso le corresponde al Controlador y al Modelo."
    ))

    # =========================================================================
    # SLIDE 7: ACTIVIDAD 1 - CONTROLADOR (TaskController.java)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header_and_footer(s7, "Actividad 1 — Controlador (TaskController.java)", "El puente que coordina el Modelo y la Vista", 7)

    code_ctrl1 = """public class TaskController {
    private List<Task> tasks;
    private TaskView view;

    public TaskController(TaskView view) {
        this.view = view;
        this.tasks = new ArrayList<>();
    }

    public void addTask(String taskName) {
        if (taskName == null || taskName.trim().isEmpty()) {
            view.printMessage("Error: Nombre vacío.");
            return;
        }
        tasks.add(new Task(taskName.trim()));
        view.printMessage("Tarea añadida: " + taskName);
    }

    public void completeTask(int index) {
        if (index >= 0 && index < tasks.size()) {
            tasks.get(index).complete();
            view.printMessage("Tarea [" + index + "] completada.");
        } else {
            view.printMessage("Error: Índice inválido.");
        }
    }

    public void displayTasks() { view.printTasks(tasks); }
}"""
    add_code_box(s7, 0.6, 1.4, 6.9, 5.4, "actividad 1/TaskController.java", code_ctrl1, font_size=9.8)

    add_card(s7, 7.75, 1.4, 4.98, 5.4, "Responsabilidades del Controlador", [
        "Mantiene la colección List<Task> y la referencia a TaskView.",
        "addTask(): valida que el nombre no esté vacío, instancia un nuevo Task y avisa a la Vista.",
        "completeTask(int index): verifica los límites (0 <= index < size) para evitar IndexOutOfBoundsException.",
        "displayTasks(): delega la impresión completa a view.printTasks(tasks).",
        "Nunca usa System.out directamente: toda salida pasa por la Vista."
    ])

    add_notes(s7, (
        "QUÉ DECIR EN ESTA DIAPOSITIVA:\n"
        "El Controlador es el cerebro coordinador. Recibe las órdenes desde Main, valida que los datos sean correctos —por "
        "ejemplo, que el índice no sea negativo ni mayor al tamaño de la lista— actualiza el Modelo y le ordena a la Vista "
        "mostrar la confirmación o el error."
    ))

    # =========================================================================
    # SLIDE 8: ACTIVIDAD 1 - MAIN Y EJECUCIÓN REAL
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header_and_footer(s8, "Actividad 1 — Main.java y Ejecución Real", "Ensamblaje de componentes y salida verificada en consola", 8)

    code_main1 = """public class Main {
    public static void main(String[] args) {
        TaskView view = new TaskView();
        TaskController controller = new TaskController(view);

        controller.addTask("Estudiar el patrón arquitectónico MVC");
        controller.addTask("Implementar el laboratorio de TO");
        controller.addTask("Preparar la exposición y el informe");

        controller.displayTasks();
        controller.completeTask(1);   // Índice válido
        controller.completeTask(10);  // Prueba de validación
        controller.displayTasks();
    }
}"""
    add_code_box(s8, 0.6, 1.4, 5.8, 5.4, "actividad 1/Main.java", code_main1, font_size=10)
    add_code_box(s8, 6.6, 1.4, 6.13, 5.4, "Salida Real de Consola (javac + java Main)", act1_out, font_size=8.6)

    add_notes(s8, (
        "QUÉ DECIR EN ESTA DIAPOSITIVA:\n"
        "A la izquierda vemos Main.java, que crea la Vista y el Controlador y ejecuta un escenario de prueba: agrega 3 tareas, "
        "las muestra, completa la tarea 1, prueba un índice inválido (10) y vuelve a listarlas.\n"
        "A la derecha tenemos la salida real compilada y ejecutada en terminal, comprobando que la tarea [1] cambió de "
        "Pendiente a Completada y que el índice 10 fue rechazado de forma controlada sin cerrar el programa."
    ))

    # =========================================================================
    # SLIDE 9: TRANSICIÓN A ACTIVIDAD 2
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header_and_footer(s9, "Transición a Actividad 2: ¿Por qué mejorar el sistema?", "De un prototipo en memoria a una aplicación robusta y persistente", 9)

    add_card(s9, 0.6, 1.5, 5.9, 5.2, "Limitaciones de la Actividad 1", [
        "✖  Datos volátiles: al cerrar el programa se pierden todas las tareas.",
        "✖  Sin edición ni borrado: no se puede corregir un nombre ni eliminar una tarea.",
        "✖  Modelo muy básico: solo guarda nombre y estado booleano.",
        "✖  Sin interactividad: las operaciones están fijas (hardcoded) en Main.",
        "✖  Sin búsqueda ni métricas: difícil de usar si crecen las tareas."
    ], bg_color=SOFT_RED, border_color=CRIMSON)

    add_card(s9, 6.83, 1.5, 5.9, 5.2, "Mejoras Implementadas en la Actividad 2", [
        "✔  Persistencia real en archivo CSV UTF-8 (guardar y cargar desde disco).",
        "✔  CRUD completo: crear, listar, actualizar, alternar estado y eliminar.",
        "✔  Modelo enriquecido: ID único, descripción, prioridad (Enum) y fecha/hora.",
        "✔  Nueva capa TaskRepository (SRP) para desacoplar la E/S de archivos.",
        "✔  Menú interactivo seguro + filtros, búsqueda por palabra clave y estadísticas."
    ], bg_color=CARD_BG, border_color=TEAL, title_color=TEAL)

    add_notes(s9, (
        "QUÉ DECIR EN ESTA DIAPOSITIVA:\n"
        "La Actividad 1 cumplió con demostrar MVC, pero tenía limitaciones reales: si cerrabas la consola perdías todo, "
        "no podías editar ni borrar tareas, y el usuario no podía escribir sus propias tareas. Por eso, en la Actividad 2 "
        "escalamos la misma arquitectura MVC agregando persistencia en archivos, CRUD completo, prioridades, filtros y menú interactivo."
    ))

    # =========================================================================
    # SLIDE 10: ACTIVIDAD 2 - NUEVA ARQUITECTURA
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header_and_footer(s10, "Actividad 2: Nueva Arquitectura MVC Escalada", "Incorporación de Priority y TaskRepository respetando SRP", 10)

    img_a2 = os.path.join(PRES_DIR, "diagrama_arquitectura_act2.png")
    if os.path.exists(img_a2):
        s10.shapes.add_picture(img_a2, Inches(0.6), Inches(1.35), width=Inches(8.1))

    add_card(s10, 8.9, 1.35, 3.83, 5.45, "Nuevos componentes clave", [
        "Priority.java (Enum): tipifica prioridades (ALTA, MEDIA, BAJA) evitando textos erróneos.",
        "Task.java ampliado: añade id, description, priority y createdAt (LocalDateTime).",
        "TaskRepository.java: capa de persistencia dentro del Modelo que maneja archivos CSV.",
        "¿Por qué un Repositorio? Para aplicar SRP (Principio de Responsabilidad Única) y no sobrecargar al Controlador."
    ], font_size=11.8)

    add_notes(s10, (
        "QUÉ DECIR EN ESTA DIAPOSITIVA:\n"
        "Vean cómo creció la arquitectura sin romper MVC. Seguimos teniendo Modelo, Vista y Controlador, pero dentro de "
        "la capa de Modelo agregamos Priority (un Enum) y TaskRepository, que se encarga únicamente de guardar y leer "
        "el archivo tareas.csv. Así el Controlador no se ensucia con código de lectura de discos."
    ))

    # =========================================================================
    # SLIDE 11: ACTIVIDAD 2 - CRUD (ACTUALIZAR Y ELIMINAR)
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header_and_footer(s11, "Actividad 2 — Operaciones CRUD: Actualizar y Eliminar", "Modificación selectiva y borrado seguro con validación de índices", 11)

    code_crud = """public void updateTask(int index, String newName,
                       String newDesc, String newPrio,
                       boolean toggleState) {
    if (!isValidIndex(index)) {
        view.printError("Índice inválido (" + index + ").");
        return;
    }
    Task task = tasks.get(index);
    if (!newName.isEmpty()) task.setName(newName);
    if (!newDesc.isEmpty()) task.setDescription(newDesc);
    if (!newPrio.isEmpty())
        task.setPriority(Priority.fromInput(newPrio));
    if (toggleState) task.toggleCompleted();
    view.printMessage("Tarea [" + index + "] actualizada.");
}

public void deleteTask(int index) {
    if (!isValidIndex(index)) {
        view.printError("Índice inválido (" + index + ").");
        return;
    }
    Task removed = tasks.remove(index);
    view.printMessage("Eliminada: " + removed.getName());
}"""
    add_code_box(s11, 0.6, 1.4, 7.1, 5.4, "actividad 2/TaskController.java (Fragmento CRUD)", code_crud, font_size=9.8)

    add_card(s11, 7.95, 1.4, 4.78, 5.4, "¿Cómo garantizamos seguridad?", [
        "Validación centralizada: isValidIndex(index) comprueba 0 <= index < tasks.size() antes de tocar la lista.",
        "Edición parcial inteligente: si el usuario deja un campo vacío y presiona Enter, se conserva el valor anterior.",
        "Alternar estado (toggleCompleted): permite pasar de Pendiente a Completada y viceversa si hubo un error.",
        "Confirmación explícita: al eliminar, se informa qué ID y nombre fueron borrados."
    ])

    add_notes(s11, (
        "QUÉ DECIR EN ESTA DIAPOSITIVA:\n"
        "Aquí mostramos dos funcionalidades clave de la Actividad 2: actualizar y eliminar. En updateTask, si el usuario "
        "solo quiere cambiar la prioridad y deja el nombre vacío, el sistema conserva el nombre original. Y tanto al "
        "actualizar como al eliminar, primero validamos el índice para que el programa nunca falle por un número fuera de rango."
    ))

    # =========================================================================
    # SLIDE 12: ACTIVIDAD 2 - PERSISTENCIA DE DATOS
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_header_and_footer(s12, "Actividad 2 — Persistencia de Datos en Archivo (CSV)", "Guardado y recuperación confiable mediante TaskRepository.java", 12)

    code_repo = """public void saveTasks(List<Task> tasks) throws IOException {
    try (BufferedWriter writer = new BufferedWriter(
         new OutputStreamWriter(new FileOutputStream(filePath),
                                StandardCharsets.UTF_8))) {
        writer.write(HEADER);
        writer.newLine();
        for (Task t : tasks) {
            writer.write(String.join(";",
                String.valueOf(t.getId()), sanitize(t.getName()),
                sanitize(t.getDescription()), t.getPriority().name(),
                String.valueOf(t.isCompleted()),
                t.getFormattedCreatedAt()));
            writer.newLine();
        }
    }
}"""
    add_code_box(s12, 0.6, 1.4, 7.2, 3.65, "actividad 2/TaskRepository.java (Guardar CSV UTF-8)", code_repo, font_size=9.6)
    add_code_box(s12, 0.6, 5.2, 7.2, 1.65, "Archivo real generado: actividad 2/tareas.csv", csv_out, font_size=8.6)

    add_card(s12, 8.0, 1.4, 4.73, 5.45, "Claves de la Persistencia", [
        "Try-with-resources: cierra automáticamente el archivo aunque ocurra un error.",
        "Codificación UTF-8: preserva tildes y la letra ñ correctamente en Windows.",
        "Saneamiento (sanitize): reemplaza ';' y saltos de línea para no corromper columnas CSV.",
        "Carga robusta (loadTasks): verifica si el archivo existe o está vacío, reconstruye cada Task y recalcula el siguiente ID disponible.",
        "Manejo de IOException: el Controlador captura el error y lo muestra limpiamente en la Vista."
    ], font_size=11.8)

    add_notes(s12, (
        "QUÉ DECIR EN ESTA DIAPOSITIVA:\n"
        "Para guardar las tareas de forma permanente creamos TaskRepository.java. Usamos un archivo tareas.csv separado por "
        "punto y coma y en formato UTF-8 para soportar tildes. Abajo a la izquierda pueden ver el archivo CSV real generado "
        "por nuestras pruebas. Cuando el programa se reinicia, loadTasks lee este archivo y reconstruye cada objeto Task."
    ))

    # =========================================================================
    # SLIDE 13: ACTIVIDAD 2 - FUNCIONALIDADES EXTRA
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    add_header_and_footer(s13, "Actividad 2 — Funcionalidades Extra y Usabilidad", "Filtros, búsqueda, prioridades, estadísticas y entradas seguras", 13)

    add_card(s13, 0.6, 1.4, 5.9, 2.55, "1. Filtros y Búsqueda Inteligente", [
        "Filtro por estado: ver solo Pendientes o solo Completadas.",
        "Filtro por prioridad: Alta, Media o Baja.",
        "Búsqueda por palabra clave: busca coincidencias (sin distinguir mayúsculas) tanto en el nombre como en la descripción."
    ])

    add_card(s13, 6.83, 1.4, 5.9, 2.55, "2. Estadísticas y Barra de Progreso", [
        "Calcula total de tareas, completadas, pendientes y porcentaje de avance.",
        "Muestra desglose por prioridad (Alta / Media / Baja).",
        "Renderiza una barra visual ASCII en consola: [##########----------] 50.0%."
    ])

    add_card(s13, 0.6, 4.2, 12.13, 2.65, "3. Menú Interactivo Seguro (Prevención de Caídas)", [
        "En Java, Scanner.nextInt() suele fallar con InputMismatchException si el usuario escribe texto en lugar de un número.",
        "Solución en TaskView.readInt(): lee siempre la línea completa con nextLine() y convierte con Integer.parseInt() dentro de try-catch.",
        "Resultado: si el usuario escribe 'abc' en vez de un número, la aplicación muestra un mensaje claro de error y sigue funcionando sin cerrarse."
    ], bg_color=SOFT_RED, border_color=CRIMSON)

    add_notes(s13, (
        "QUÉ DECIR EN ESTA DIAPOSITIVA:\n"
        "Además de lo obligatorio, añadimos funciones muy útiles en cualquier gestor real: filtros por estado o prioridad, "
        "búsqueda por palabra clave y un panel de estadísticas con barra de progreso. También resolvimos un error muy común "
        "en consola en Java: leer enteros con nextLine() y try-catch para que escribir letras por accidente nunca tumbe el programa."
    ))

    # =========================================================================
    # SLIDE 14: EVIDENCIA REAL ACT 2 Y COMPARATIVA
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    add_header_and_footer(s14, "Evidencia de Ejecución (Act. 2) y Comparativa", "Prueba automatizada de punta a punta y evolución arquitectónica", 14)

    # Extraer líneas clave de la salida de Actividad 2 para que quepa nítidamente
    lines_a2 = [ln for ln in act2_out.splitlines() if ln.strip()]
    key_lines = []
    for ln in lines_a2:
        if any(k in ln for k in [">>", "[ERROR]", "===", "IDX", "0 ", "1 ", "2 ", "Total de tareas", "Avance general", "Por prioridad"]):
            key_lines.append(ln)
    snippet_a2 = "\n".join(key_lines[:24])
    add_code_box(s14, 0.6, 1.35, 6.7, 5.45, "Extracto Real: Prueba Automatizada Actividad 2", snippet_a2, font_size=8.1)

    # Tabla comparativa
    rows, cols = 7, 3
    tbl_shape = s14.shapes.add_table(rows, cols, Inches(7.5), Inches(1.35), Inches(5.23), Inches(5.45))
    tbl = tbl_shape.table
    tbl.columns[0].width = Inches(1.75)
    tbl.columns[1].width = Inches(1.58)
    tbl.columns[2].width = Inches(1.90)

    headers = ["Criterio", "Actividad 1", "Actividad 2"]
    data = [
        ["Clases", "4 clases", "6 clases (+Enum/Repo)"],
        ["Operaciones", "Crear, Listar, Completar", "CRUD completo + Toggle"],
        ["Atributos", "name, completed", "+id, desc, priority, fecha"],
        ["Persistencia", "Solo memoria RAM", "Archivo CSV UTF-8"],
        ["Consultas", "Listado general", "Filtros, búsqueda, stats"],
        ["Interacción", "Flujo fijo en Main", "Menú seguro interactivo"]
    ]
    for c, h in enumerate(headers):
        cell = tbl.cell(0, c)
        cell.fill.solid()
        cell.fill.fore_color.rgb = CRIMSON
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.name = "Segoe UI"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = WHITE

    for r, row_data in enumerate(data, start=1):
        for c, val in enumerate(row_data):
            cell = tbl.cell(r, c)
            cell.fill.solid()
            cell.fill.fore_color.rgb = CARD_BG if r % 2 == 1 else WHITE
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.name = "Segoe UI"
            p.font.size = Pt(10.2)
            p.font.bold = (c == 0)
            p.font.color.rgb = DARK_CHARCOAL

    add_notes(s14, (
        "QUÉ DECIR EN ESTA DIAPOSITIVA:\n"
        "A la izquierda vemos el extracto real de la prueba automatizada de la Actividad 2, donde verificamos añadir tareas, "
        "actualizarlas, filtrarlas, buscarlas, ver estadísticas, guardar en tareas.csv, limpiar la memoria RAM y volver a "
        "cargarlas intactas desde el disco. A la derecha, la tabla resume el salto de calidad entre la Actividad 1 y la Actividad 2."
    ))

    # =========================================================================
    # SLIDE 15: CONCLUSIONES
    # =========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    add_header_and_footer(s15, "Conclusiones y Beneficios Comprobados de MVC", "Lecciones aprendidas en el laboratorio de Tecnología de Objetos", 15)

    add_card(s15, 0.6, 1.45, 5.9, 4.65, "Beneficios Comprobados en el Código", [
        "Escalabilidad real: pasar de la Actividad 1 a la Actividad 2 no requirió rehacer la arquitectura; solo extendimos cada capa.",
        "Bajo acoplamiento y alta cohesión: cada clase tiene una sola razón para cambiar (SRP).",
        "Código más seguro y testeable: las validaciones están concentradas en el Controlador y la lectura segura en la Vista.",
        "Persistencia desacoplada: cambiar de CSV a JSON o base de datos SQL solo requeriría modificar TaskRepository."
    ])

    add_card(s15, 6.83, 1.45, 5.9, 4.65, "Recomendaciones para Proyectos Futuros", [
        "Aplicar MVC desde el inicio incluso en aplicaciones pequeñas de consola.",
        "Usar interfaces (ej. ITaskRepository) para facilitar pruebas unitarias con JUnit.",
        "Separar siempre las excepciones técnicas (IOException) de los mensajes mostrados al usuario final.",
        "Mantener el Modelo libre de dependencias de interfaz gráfica o consola."
    ], bg_color=SOFT_RED, border_color=CRIMSON)

    thanks = s15.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(6.25), Inches(12.13), Inches(0.65))
    thanks.fill.solid()
    thanks.fill.fore_color.rgb = DARK_CHARCOAL
    thanks.line.fill.background()
    tp = thanks.text_frame.paragraphs[0]
    tp.text = "¡Muchas gracias por su atención!  •  ¿Preguntas o comentarios?"
    tp.alignment = PP_ALIGN.CENTER
    tp.font.name = "Segoe UI"
    tp.font.size = Pt(15)
    tp.font.bold = True
    tp.font.color.rgb = WHITE

    add_notes(s15, (
        "QUÉ DECIR EN ESTA DIAPOSITIVA:\n"
        "Para concluir, esta práctica nos demostró con código real por qué MVC es uno de los patrones más usados en la "
        "industria: nos permitió pasar de un programa pequeño a uno completo con persistencia, filtros y estadísticas de "
        "forma ordenada y sin código espagueti. Si mañana quisiéramos guardar en una base de datos o crear una app de "
        "escritorio, la estructura ya está preparada. Muchas gracias, quedamos atentos a sus preguntas."
    ))

    output_pptx = os.path.join(PRES_DIR, "Presentacion_MVC_Tareas.pptx")
    prs.save(output_pptx)
    print(f"Presentación generada exitosamente: {output_pptx}")


if __name__ == "__main__":
    build_presentation()
