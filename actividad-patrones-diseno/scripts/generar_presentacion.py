"""
Generador de Presentación PowerPoint (.pptx) sobre Patrones de Diseño Comportamentales:
Observer, Strategy y Command en Java.

Produce: actividad-patrones-diseno/Presentacion_Patrones_Diseno.pptx (14 diapositivas 16:9)
con lenguaje claro y analogías cotidianas para todo público, diagramas visuales,
explicación paso a paso del código, resultados reales y Notas del Orador.
"""
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
ACT_DIR = os.path.dirname(SCRIPTS_DIR)
DIAG_DIR = os.path.join(SCRIPTS_DIR, "diagramas")
SALIDAS_DIR = os.path.join(SCRIPTS_DIR, "salidas")

# Paleta profesional limpia y contrastada
NAVY = RGBColor(0x1E, 0x29, 0x3B)
SLATE = RGBColor(0x33, 0x41, 0x55)
GUINDA = RGBColor(0x8B, 0x1E, 0x2D)
BLUE = RGBColor(0x1D, 0x4E, 0xD8)
TEAL = RGBColor(0x0F, 0x76, 0x6E)
AMBER = RGBColor(0xB4, 0x53, 0x09)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
CARD_BG = RGBColor(0xF8, 0xFA, 0xFC)
SOFT_BLUE = RGBColor(0xEF, 0xF6, 0xFF)
SOFT_TEAL = RGBColor(0xF0, 0xFD, 0xFA)
SOFT_AMBER = RGBColor(0xFF, 0xFB, 0xEB)
SOFT_RED = RGBColor(0xFE, 0xF2, 0xF2)
BORDER = RGBColor(0xCB, 0xD5, 0xE1)
MUTED = RGBColor(0x64, 0x74, 0x8B)
CODE_BG = RGBColor(0x0F, 0x17, 0x2A)
CODE_TEXT = RGBColor(0xF1, 0xF5, 0xF9)

TOTAL_SLIDES = 14


def read_text(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read().strip()
    return ""


def add_notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text


def add_chrome(slide, title, subtitle, slide_num, accent=GUINDA):
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.11))
    bar.fill.solid()
    bar.fill.fore_color.rgb = accent
    bar.line.fill.background()

    tb = slide.shapes.add_textbox(Inches(0.6), Inches(0.22), Inches(12.1), Inches(0.55))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = title
    p.font.name = "Segoe UI"
    p.font.size = Pt(23)
    p.font.bold = True
    p.font.color.rgb = NAVY

    stb = slide.shapes.add_textbox(Inches(0.6), Inches(0.76), Inches(12.1), Inches(0.32))
    stf = stb.text_frame
    stf.word_wrap = True
    stf.margin_left = stf.margin_right = stf.margin_top = stf.margin_bottom = 0
    sp = stf.paragraphs[0]
    sp.text = subtitle
    sp.font.name = "Segoe UI"
    sp.font.size = Pt(12.5)
    sp.font.color.rgb = accent

    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(1.13), Inches(12.133), Inches(0.02))
    line.fill.solid()
    line.fill.fore_color.rgb = BORDER
    line.line.fill.background()

    ftb = slide.shapes.add_textbox(Inches(0.6), Inches(7.10), Inches(10.0), Inches(0.28))
    fp = ftb.text_frame.paragraphs[0]
    fp.text = "Tecnología de Objetos (UNSA)  |  Patrones Comportamentales: Observer, Strategy y Command"
    fp.font.name = "Segoe UI"
    fp.font.size = Pt(9.5)
    fp.font.color.rgb = MUTED

    ntb = slide.shapes.add_textbox(Inches(11.4), Inches(7.10), Inches(1.333), Inches(0.28))
    np = ntb.text_frame.paragraphs[0]
    np.text = f"{slide_num} / {TOTAL_SLIDES}"
    np.alignment = PP_ALIGN.RIGHT
    np.font.name = "Segoe UI"
    np.font.size = Pt(9.5)
    np.font.bold = True
    np.font.color.rgb = accent


def add_card(slide, x, y, w, h, title, items, bg=CARD_BG, border=BORDER, title_color=NAVY, font_size=12.5):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    shape.adjustments[0] = 0.04
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg
    shape.line.color.rgb = border
    shape.line.width = Pt(1.4)

    tf = shape.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.TOP
    tf.margin_left = Inches(0.20)
    tf.margin_right = Inches(0.20)
    tf.margin_top = Inches(0.15)
    tf.margin_bottom = Inches(0.12)

    first = True
    if title:
        p = tf.paragraphs[0]
        p.text = title
        p.font.name = "Segoe UI"
        p.font.size = Pt(14.5)
        p.font.bold = True
        p.font.color.rgb = title_color
        p.space_after = Pt(7)
        first = False

    for item in items:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.text = item if item.startswith(("•", "1.", "2.", "3.", "4.", "5.", "✔")) else f"•  {item}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(font_size)
        p.font.color.rgb = NAVY
        p.space_after = Pt(6)
    return shape


def add_code_box(slide, x, y, w, h, title, code_text, accent=GUINDA, font_size=9.5):
    box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    box.adjustments[0] = 0.03
    box.fill.solid()
    box.fill.fore_color.rgb = CODE_BG
    box.line.color.rgb = SLATE
    box.line.width = Pt(1)

    hdr = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(0.32))
    hdr.fill.solid()
    hdr.fill.fore_color.rgb = accent
    hdr.line.fill.background()
    hp = hdr.text_frame.paragraphs[0]
    hp.text = f"  {title}"
    hp.font.name = "Consolas"
    hp.font.size = Pt(10.0)
    hp.font.bold = True
    hp.font.color.rgb = WHITE

    tb = slide.shapes.add_textbox(Inches(x + 0.14), Inches(y + 0.37), Inches(w - 0.28), Inches(h - 0.43))
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
    blank = prs.slide_layouts[6]

    out_obs = read_text(os.path.join(SALIDAS_DIR, "salida_observer.txt"))
    out_str = read_text(os.path.join(SALIDAS_DIR, "salida_strategy.txt"))
    out_cmd = read_text(os.path.join(SALIDAS_DIR, "salida_command.txt"))

    # =========================================================================
    # SLIDE 1: PORTADA
    # =========================================================================
    s1 = prs.slides.add_slide(blank)
    bg = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = NAVY
    bg.line.fill.background()

    side = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.45), Inches(7.5))
    side.fill.solid()
    side.fill.fore_color.rgb = GUINDA
    side.line.fill.background()

    badge = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.1), Inches(1.05), Inches(5.3), Inches(0.46))
    badge.fill.solid()
    badge.fill.fore_color.rgb = GUINDA
    badge.line.fill.background()
    bp = badge.text_frame.paragraphs[0]
    bp.text = "UNSA  •  TECNOLOGÍA DE OBJETOS  •  ACTIVIDAD 5"
    bp.alignment = PP_ALIGN.CENTER
    bp.font.name = "Segoe UI"
    bp.font.size = Pt(11.5)
    bp.font.bold = True
    bp.font.color.rgb = WHITE

    tb = s1.shapes.add_textbox(Inches(1.1), Inches(1.8), Inches(11.2), Inches(2.2))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Patrones de Diseño Comportamentales\nen Java"
    p.font.name = "Segoe UI"
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = WHITE

    p2 = tf.add_paragraph()
    p2.text = "Observer (Notificaciones)  •  Strategy (Promociones)  •  Command (Control Remoto de TV)"
    p2.font.name = "Segoe UI"
    p2.font.size = Pt(17)
    p2.font.color.rgb = BORDER
    p2.space_before = Pt(14)

    meta = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.1), Inches(4.75), Inches(11.1), Inches(1.9))
    meta.adjustments[0] = 0.05
    meta.fill.solid()
    meta.fill.fore_color.rgb = SLATE
    meta.line.color.rgb = GUINDA
    meta.line.width = Pt(1.5)
    mtf = meta.text_frame
    mtf.margin_left = Inches(0.3)
    mtf.margin_top = Inches(0.22)
    for idx, (k, v) in enumerate([
        ("Universidad: ", "Universidad Nacional de San Agustín de Arequipa (UNSA)"),
        ("Docente: ", "Mg. Diego Alonso Iquira Becerra"),
        ("Integrantes: ", "[Completar Apellidos y Nombres]"),
        ("Fecha: ", "Noviembre - 2026"),
    ]):
        mp = mtf.paragraphs[0] if idx == 0 else mtf.add_paragraph()
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
        r2.font.color.rgb = BORDER
        mp.space_after = Pt(5)

    add_notes(s1, "Presentación introductoria: presentaremos tres patrones comportamentales en Java explicados con analogías cotidianas y código real ejecutado.")

    # =========================================================================
    # SLIDE 2: ¿QUÉ SON LOS PATRONES COMPORTAMENTALES?
    # =========================================================================
    s2 = prs.slides.add_slide(blank)
    add_chrome(s2, "¿Qué son los Patrones de Diseño Comportamentales?",
               "Reglas claras para que distintas piezas de un programa colaboren sin enredarse", 2)

    add_card(s2, 0.6, 1.38, 12.13, 1.45, "Explicación sencilla (sin tecnicismos)", [
        "Imagina una empresa bien organizada: cada persona sabe qué tarea cumple y cómo pedir ayuda a otra área sin interrumpir todo.",
        "En programación, un patrón comportamental es una receta probada para repartir tareas y mensajes entre objetos, evitando código desordenado o difícil de cambiar."
    ], bg=SOFT_RED, border=GUINDA, title_color=GUINDA, font_size=13)

    add_card(s2, 0.6, 3.1, 3.85, 3.7, "1. Patrón Observer", [
        "Idea clave: 'Avísame cuando pase algo nuevo'.",
        "Analogía: Suscribirse a un canal de YouTube.",
        "En el ejercicio: Un sistema de notificaciones avisa a múltiples usuarios al instante."
    ], bg=SOFT_BLUE, border=BLUE, title_color=BLUE, font_size=12.5)

    add_card(s2, 4.74, 3.1, 3.85, 3.7, "2. Patrón Strategy", [
        "Idea clave: 'Elige la mejor forma de calcular algo según el momento'.",
        "Analogía: Elegir ruta en GPS (auto, bus o caminando).",
        "En el ejercicio: Una calculadora cambia entre 4 promociones al instante."
    ], bg=SOFT_TEAL, border=TEAL, title_color=TEAL, font_size=12.5)

    add_card(s2, 8.88, 3.1, 3.85, 3.7, "3. Patrón Command", [
        "Idea clave: 'Empaqueta una orden para que cualquiera la ejecute'.",
        "Analogía: La comanda escrita que llega a la cocina.",
        "En el ejercicio: Un control remoto ejecuta 5 acciones distintas en un televisor."
    ], bg=SOFT_AMBER, border=AMBER, title_color=AMBER, font_size=12.5)

    add_notes(s2, "Antes de entrar al código, explicamos con analogías simples qué resuelve cada uno de los tres patrones comportamentales.")

    # =========================================================================
    # SLIDE 3: OBSERVER - IDEA Y ANALOGÍA REAL
    # =========================================================================
    s3 = prs.slides.add_slide(blank)
    add_chrome(s3, "Patrón Observer: Idea y Analogía de la Vida Real",
               "Cómo funciona un sistema de suscripciones explicado paso a paso", 3, accent=BLUE)

    add_card(s3, 0.6, 1.4, 5.9, 5.4, "Analogía: Canal de Noticias o YouTube", [
        "1. Te suscribes: Le das clic a 'Suscribirse' en tu canal favorito (registrar).",
        "2. Llega una novedad: Cuando el canal sube un video, te llega la alerta automáticamente sin que tengas que entrar cada 5 minutos a revisar (notificar).",
        "3. Te das de baja: Si un día ya no te interesa, cancelas la suscripción (eliminar) y dejas de recibir avisos.",
        "✔ Resultado: El canal no necesita conocer tu vida privada; solo mantiene una lista de suscriptores activos."
    ], bg=SOFT_BLUE, border=BLUE, title_color=BLUE, font_size=13)

    add_card(s3, 6.8, 1.4, 5.93, 2.55, "¿Qué problema resuelve en software?", [
        "Evita que los usuarios pregunten repetidamente '¿hay algo nuevo?' (desperdicio de recursos).",
        "Permite agregar o quitar usuarios en cualquier momento sin modificar el sistema central."
    ], font_size=12.5)

    add_card(s3, 6.8, 4.18, 5.93, 2.62, "Los 3 actores del ejercicio en Java", [
        "SistemaNotificaciones (Emisor): guarda la lista de inscritos y envía los mensajes.",
        "Observer (Contrato): regla común que obliga a tener el método actualizar().",
        "Usuario (Receptor): Ana, Carlos, Lucía y Diego reciben el mensaje en pantalla."
    ], font_size=12.5)

    add_notes(s3, "Analogía clara de YouTube/noticias: el usuario no pregunta cada segundo si hay novedades; el sistema le avisa solo mientras esté suscrito.")

    # =========================================================================
    # SLIDE 4: OBSERVER - DIAGRAMA Y COMPONENTES
    # =========================================================================
    s4 = prs.slides.add_slide(blank)
    add_chrome(s4, "Patrón Observer: Arquitectura del Ejercicio",
               "Relación entre SistemaNotificaciones, la interfaz Observer y los Usuarios", 4, accent=BLUE)

    img_obs = os.path.join(DIAG_DIR, "diagrama_observer.png")
    if os.path.exists(img_obs):
        s4.shapes.add_picture(img_obs, Inches(0.55), Inches(1.38), width=Inches(8.2))

    add_card(s4, 8.95, 1.38, 3.78, 5.4, "¿Qué hace cada pieza?", [
        "1. registrar(usuario): añade al usuario a la lista de alertas.",
        "2. notificar(texto): recorre la lista y llama a actualizar(texto) en cada usuario.",
        "3. eliminar(usuario): saca al usuario de la lista para que no reciba futuros avisos.",
        "4. Usuario: implementa actualizar() mostrando su nombre y el mensaje recibido."
    ], bg=CARD_BG, border=BLUE, title_color=BLUE, font_size=12.2)

    add_notes(s4, "Explicamos el diagrama visual de Observer: SistemaNotificaciones solo conoce la interfaz Observer, por eso puede avisar a cualquier cantidad de usuarios.")

    # =========================================================================
    # SLIDE 5: OBSERVER - CÓDIGO SIMPLE Y RESULTADO REAL
    # =========================================================================
    s5 = prs.slides.add_slide(blank)
    add_chrome(s5, "Patrón Observer: Código Clave y Resultado Real",
               "Demostración ejecutada en Java con suscripción y desuscripción", 5, accent=BLUE)

    code_obs = """// Sujeto que gestiona suscriptores
public class SistemaNotificaciones {
    private final List<Observer> observadores = new ArrayList<>();

    public void registrar(Observer obs) { observadores.add(obs); }
    public void eliminar(Observer obs)  { observadores.remove(obs); }

    public void notificar(String mensaje) {
        for (Observer obs : observadores) {
            obs.actualizar(mensaje); // Avisa a cada suscrito
        }
    }
}

// Uso en Main:
sistema.registrar(ana); sistema.registrar(carlos); sistema.registrar(lucia);
sistema.notificar("Nueva actualización v2.0 disponible.");
sistema.eliminar(carlos); // Carlos deja de recibir futuras alertas
sistema.notificar("Mantenimiento programado hoy a las 22:00.");"""

    add_code_box(s5, 0.6, 1.38, 5.85, 5.42, "SistemaNotificaciones.java + Main.java", code_obs, accent=BLUE, font_size=8.6)
    add_code_box(s5, 6.65, 1.38, 6.08, 5.42, "Salida Real de Consola (observer.Main)", out_obs, accent=NAVY, font_size=7.6)

    add_notes(s5, "En la salida real de la derecha comprobamos que Carlos recibe el primer aviso, luego es eliminado y ya no recibe el segundo aviso.")

    # =========================================================================
    # SLIDE 6: STRATEGY - IDEA Y ANALOGÍA REAL
    # =========================================================================
    s6 = prs.slides.add_slide(blank)
    add_chrome(s6, "Patrón Strategy: Idea y Analogía de la Vida Real",
               "Cómo cambiar la regla de cálculo sin modificar la calculadora", 6, accent=TEAL)

    add_card(s6, 0.6, 1.4, 5.9, 5.4, "Analogía: Tu aplicación de mapas (GPS)", [
        "El objetivo siempre es el mismo: llegar del punto A al punto B.",
        "Pero puedes elegir la estrategia de viaje según necesites:",
        "• En auto (más rápido por autopista).",
        "• En autobús (rutas de transporte público).",
        "• A pie (calles peatonales).",
        "✔ El mapa (contexto) es el mismo; solo cambias la regla de ruta con un toque."
    ], bg=SOFT_TEAL, border=TEAL, title_color=TEAL, font_size=13)

    add_card(s6, 6.8, 1.4, 5.93, 2.55, "¿Qué problema resuelve en software?", [
        "Evita llenar una clase con decenas de 'si es descuento A haz esto, si es B haz aquello...'.",
        "Cada promoción vive aislada en su propia clase limpia y fácil de probar."
    ], font_size=12.5)

    add_card(s6, 6.8, 4.18, 5.93, 2.62, "Piezas del ejercicio en Java", [
        "CalculadoraPrecios (Contexto): pide calcular el total usando la regla activa.",
        "EstrategiaPromocion (Contrato): todas las promos responden a aplicarPromocion().",
        "4 Estrategias reales: Sin descuento, 20%, S/ 75.00 fijos y 2x1."
    ], font_size=12.5)

    add_notes(s6, "Con la analogía del GPS queda clarísimo: mismo objetivo (calcular total), distintas estrategias intercambiables en vivo.")

    # =========================================================================
    # SLIDE 7: STRATEGY - DIAGRAMA Y LAS 4 PROMOCIONES
    # =========================================================================
    s7 = prs.slides.add_slide(blank)
    add_chrome(s7, "Patrón Strategy: Diagrama y las 4 Promociones",
               "Cómo CalculadoraPrecios delega el cálculo a cada estrategia concreta", 7, accent=TEAL)

    img_str = os.path.join(DIAG_DIR, "diagrama_strategy.png")
    if os.path.exists(img_str):
        s7.shapes.add_picture(img_str, Inches(0.55), Inches(1.38), width=Inches(8.2))

    add_card(s7, 8.95, 1.38, 3.78, 5.4, "Las 4 promociones implementadas", [
        "1. SinDescuento: cobra el 100% del precio normal.",
        "2. DescuentoPorcentaje: descuenta un % (ej. 20% menos).",
        "3. DescuentoMontoFijo: resta un bono fijo (ej. -S/ 75.00).",
        "4. PromocionDosPorUno: por cada 2 productos, solo cobra 1.",
        "✔ setEstrategia() cambia de promo al instante."
    ], bg=CARD_BG, border=TEAL, title_color=TEAL, font_size=12.0)

    add_notes(s7, "Aquí mostramos las 4 clases de promoción implementadas y cómo todas comparten exactamente la misma interfaz EstrategiaPromocion.")

    # =========================================================================
    # SLIDE 8: STRATEGY - CAMBIO EN VIVO Y RESULTADOS REALES
    # =========================================================================
    s8 = prs.slides.add_slide(blank)
    add_chrome(s8, "Patrón Strategy: Cambio en Ejecución y Resultados",
               "Prueba real sobre 4 Audífonos Bluetooth de S/ 120.00 (Subtotal: S/ 480.00)", 8, accent=TEAL)

    code_str = """// Contexto que cambia de estrategia en tiempo real
public class CalculadoraPrecios {
    private EstrategiaPromocion estrategia;

    public void setEstrategia(EstrategiaPromocion estrategia) {
        this.estrategia = estrategia;
    }

    public double calcularTotal(double precio, int cantidad) {
        return estrategia.aplicarPromocion(precio, cantidad);
    }
}

// En Main.java:
CalculadoraPrecios calc = new CalculadoraPrecios(new SinDescuento());
calc.setEstrategia(new DescuentoPorcentaje(20));
calc.setEstrategia(new DescuentoMontoFijo(75.00));
calc.setEstrategia(new PromocionDosPorUno());"""

    add_code_box(s8, 0.6, 1.38, 6.1, 5.42, "CalculadoraPrecios.java + Main.java", code_str, accent=TEAL, font_size=9.4)
    add_code_box(s8, 6.9, 1.38, 5.83, 5.42, "Salida Real de Consola (strategy.Main)", out_str, accent=NAVY, font_size=8.5)

    add_notes(s8, "Sobre el mismo producto (4 audífonos = S/ 480), la calculadora pasa de pagar 480 a 384 (20%), 405 (-S/75) y 240 (2x1).")

    # =========================================================================
    # SLIDE 9: COMMAND - IDEA Y ANALOGÍA REAL
    # =========================================================================
    s9 = prs.slides.add_slide(blank)
    add_chrome(s9, "Patrón Command: Idea y Analogía de la Vida Real",
               "Convertir una petición en un objeto orden independiente", 9, accent=AMBER)

    add_card(s9, 0.6, 1.4, 5.9, 5.4, "Analogía: La Comanda de un Restaurante", [
        "1. Tú (Cliente) pides un plato al mesero.",
        "2. El mesero anota la orden en un papel llamado 'comanda' (objeto Command) y la deja en el mostrador.",
        "3. El botón o timbre de cocina (Invocador) solo avisa: '¡ejecuten la siguiente comanda!'.",
        "4. El chef (Receptor / Televisor) lee la orden y realiza el trabajo real.",
        "✔ El botón no sabe cocinar ni cómo funciona el televisor por dentro; solo dispara la orden."
    ], bg=SOFT_AMBER, border=AMBER, title_color=AMBER, font_size=12.8)

    add_card(s9, 6.8, 1.4, 5.93, 2.55, "¿Qué problema resuelve en software?", [
        "Separa por completo el botón que dispara la acción (ControlRemoto) del aparato que la ejecuta (Televisor).",
        "Permite reasignar funciones, registrar historial o crear botones universales."
    ], font_size=12.5)

    add_card(s9, 6.8, 4.18, 5.93, 2.62, "Piezas del ejercicio en Java", [
        "ControlRemoto (Invocador): solo tiene setCommand() y presionarBoton().",
        "Command (Contrato): método único execute().",
        "Televisor (Receptor): ejecuta las 5 acciones reales."
    ], font_size=12.5)

    add_notes(s9, "Con la comanda de restaurante se entiende por qué ControlRemoto no necesita saber absolutamente nada de electrónica de TV.")

    # =========================================================================
    # SLIDE 10: COMMAND - DIAGRAMA Y LAS 5 FUNCIONALIDADES
    # =========================================================================
    s10 = prs.slides.add_slide(blank)
    add_chrome(s10, "Patrón Command: Diagrama y las 5 Funcionalidades",
               "Cinco comandos concretos conectados entre el Control Remoto y el Televisor", 10, accent=AMBER)

    img_cmd = os.path.join(DIAG_DIR, "diagrama_command.png")
    if os.path.exists(img_cmd):
        s10.shapes.add_picture(img_cmd, Inches(0.55), Inches(1.38), width=Inches(8.3))

    add_card(s10, 9.05, 1.38, 3.68, 5.4, "Las 5 acciones del TV", [
        "1. Encender TV: activa el televisor (Canal 1, Vol 15).",
        "2. Subir volumen: aumenta +5 (máximo 100).",
        "3. Cambiar canal: sintoniza el canal elegido (ej. canal 7).",
        "4. Bajar volumen: reduce -5 (mínimo 0).",
        "5. Apagar TV: apaga el equipo de forma segura."
    ], bg=CARD_BG, border=AMBER, title_color=AMBER, font_size=12.0)

    add_notes(s10, "Cada botón u orden es una clase pequeña que implementa Command y delega en el método correspondiente de Televisor.")

    # =========================================================================
    # SLIDE 11: COMMAND - CÓDIGO SIMPLE Y RESULTADO REAL
    # =========================================================================
    s11 = prs.slides.add_slide(blank)
    add_chrome(s11, "Patrón Command: Código Simple y Resultado Real",
               "Configuración y ejecución verificada de las 5 acciones del televisor", 11, accent=AMBER)

    code_cmd = """// Invocador desacoplado del Televisor
public class ControlRemoto {
    private Command comando;
    public void setCommand(Command comando) { this.comando = comando; }
    public void presionarBoton() {
        if (comando != null) comando.execute();
    }
}

// Ejemplo de Comando Concreto (con parámetro):
public class CambiarCanalCommand implements Command {
    private final Televisor televisor;
    private final int nuevoCanal;
    public CambiarCanalCommand(Televisor tv, int canal) {
        this.televisor = tv; this.nuevoCanal = canal;
    }
    public void execute() { televisor.cambiarCanal(nuevoCanal); }
}"""

    add_code_box(s11, 0.6, 1.38, 6.25, 5.42, "ControlRemoto.java + CambiarCanalCommand.java", code_cmd, accent=AMBER, font_size=9.2)
    add_code_box(s11, 7.05, 1.38, 5.68, 5.42, "Salida Real de Consola (command.Main)", out_cmd, accent=NAVY, font_size=8.8)

    add_notes(s11, "A la derecha se observa la salida real en consola ejecutando en orden las 5 acciones: encender, subir a 20, canal 7, bajar a 15 y apagar.")

    # =========================================================================
    # SLIDE 12: TABLA COMPARATIVA CLARA
    # =========================================================================
    s12 = prs.slides.add_slide(blank)
    add_chrome(s12, "Comparativa Clara de los Tres Patrones",
               "Resumen visual para identificar cuándo usar Observer, Strategy o Command", 12)

    tbl_shape = s12.shapes.add_table(5, 4, Inches(0.6), Inches(1.45), Inches(12.13), Inches(5.25))
    tbl = tbl_shape.table
    tbl.columns[0].width = Inches(2.23)
    tbl.columns[1].width = Inches(3.30)
    tbl.columns[2].width = Inches(3.30)
    tbl.columns[3].width = Inches(3.30)

    headers = ["Aspecto", "Observer", "Strategy", "Command"]
    rows_data = [
        ["Analogía cotidiana", "Suscribirse a un canal de noticias o YouTube.", "Elegir medio de ruta en el GPS (auto, bus, a pie).", "Comanda escrita en un restaurante / botón remoto."],
        ["¿Para qué sirve?", "Avisar automáticamente a muchos interesados cuando ocurre algo.", "Cambiar la fórmula o regla de negocio sin tocar la calculadora.", "Encapsular acciones como objetos independientes."],
        ["Piezas principales", "SistemaNotificaciones, Observer y Usuario.", "CalculadoraPrecios, EstrategiaPromocion y 4 promos.", "ControlRemoto, Command, 5 comandos y Televisor."],
        ["Ventaja principal", "Agregar o quitar usuarios en cualquier momento.", "Agregar nuevas promociones sin llenar el código de if/else.", "El control no depende de los detalles internos del TV."]
    ]
    header_colors = [NAVY, BLUE, TEAL, AMBER]
    for c_idx, h in enumerate(headers):
        cell = tbl.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = header_colors[c_idx]
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.name = "Segoe UI"
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = WHITE

    for r_idx, r_vals in enumerate(rows_data, start=1):
        for c_idx, val in enumerate(r_vals):
            cell = tbl.cell(r_idx, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = CARD_BG if r_idx % 2 == 1 else WHITE
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.name = "Segoe UI"
            p.font.size = Pt(11.5)
            p.font.bold = (c_idx == 0)
            p.font.color.rgb = NAVY

    add_notes(s12, "Esta tabla resume en un vistazo la diferencia práctica entre los tres patrones usando sus analogías, piezas y beneficios.")

    # =========================================================================
    # SLIDE 13: RESUMEN DE IMPLEMENTACIÓN Y VERIFICACIÓN
    # =========================================================================
    s13 = prs.slides.add_slide(blank)
    add_chrome(s13, "Organización del Proyecto y Verificación Técnica",
               "Todo organizado exclusivamente dentro de actividad-patrones-diseno/", 13)

    add_card(s13, 0.6, 1.45, 5.85, 5.2, "Estructura limpia de carpetas", [
        "src/observer/ -> 4 archivos Java (Observer, Usuario, SistemaNotificaciones, Main).",
        "src/strategy/ -> 7 archivos Java (EstrategiaPromocion, 4 promociones, CalculadoraPrecios, Main).",
        "src/command/ -> 9 archivos Java (Command, Televisor, 5 comandos, ControlRemoto, Main).",
        "Documentación: EXPLICACION_CODIGO.md, Informe_Patrones_Diseno.docx y Presentacion_Patrones_Diseno.pptx."
    ], font_size=12.2)

    add_card(s13, 6.85, 1.45, 5.88, 5.2, "Verificación real realizada", [
        "✔ Compilación estricta con OpenJDK 21 (javac -Xlint:all -encoding UTF-8).",
        "✔ Resultado de compilación: 0 errores y 0 advertencias en los 20 archivos.",
        "✔ Ejecución verificada de observer.Main, strategy.Main y command.Main.",
        "✔ Código directo, sin clases innecesarias ni lógica duplicada."
    ], bg=SOFT_TEAL, border=TEAL, title_color=TEAL, font_size=12.5)

    add_notes(s13, "Mostramos cómo quedó organizada la carpeta exclusiva actividad-patrones-diseno/ y confirmamos la compilación sin errores ni advertencias en Java 21.")

    # =========================================================================
    # SLIDE 14: CONCLUSIONES
    # =========================================================================
    s14 = prs.slides.add_slide(blank)
    add_chrome(s14, "Conclusiones",
               "Aprendizajes clave de la aplicación de Observer, Strategy y Command", 14)

    conclusions = [
        ("1. Código más flexible y fácil de mantener",
         "Programar usando interfaces permite cambiar reglas o agregar nuevos usuarios, promociones o botones sin reescribir el código que ya funciona.",
         SOFT_BLUE, BLUE),
        ("2. Menos dependencias rígidas (Bajo acoplamiento)",
         "Cada clase se concentra en una tarea concreta: emitir avisos, calcular una rebaja o controlar el televisor.",
         SOFT_TEAL, TEAL),
        ("3. Comportamientos intercambiables al instante",
         "Tanto Strategy como Observer y Command demuestran que el comportamiento de un programa puede cambiar dinámicamente en tiempo de ejecución.",
         SOFT_AMBER, AMBER),
        ("4. Soluciones aplicables a proyectos reales",
         "Estos tres patrones son la base de sistemas reales como notificaciones en apps móviles, carritos de compra con cupones y controles de dispositivos.",
         SOFT_RED, GUINDA),
    ]
    positions = [(0.6, 1.45), (6.8, 1.45), (0.6, 4.25), (6.8, 4.25)]
    for (x, y), (t, desc, bgc, bdc) in zip(positions, conclusions):
        add_card(s14, x, y, 5.93, 2.5, t, [desc], bg=bgc, border=bdc, title_color=bdc, font_size=12.5)

    add_notes(s14, "Cierre de la presentación resumiendo los cuatro beneficios comprobados de aplicar patrones comportamentales en Java.")

    out_path = os.path.join(ACT_DIR, "Presentacion_Patrones_Diseno.pptx")
    prs.save(out_path)
    print("Presentación generada exitosamente:", out_path)


if __name__ == "__main__":
    build_presentation()
