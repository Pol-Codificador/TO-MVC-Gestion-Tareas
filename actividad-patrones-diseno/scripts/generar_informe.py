"""
Generador del Informe Formal en Word (.docx) sobre Patrones de Diseño Comportamentales
(Observer, Strategy y Command) en Java.

Utiliza la plantilla oficial UNSA ('informe/plantilla_base.docx', idéntica a 'Plantilla Informe.docx'),
conservando intactos la portada institucional, banner, escudo, márgenes y tipografía base.
"""
import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
ACT_DIR = os.path.dirname(SCRIPTS_DIR)
REPO_ROOT = os.path.dirname(ACT_DIR)
TEMPLATE_PATH = os.path.join(REPO_ROOT, "informe", "plantilla_base.docx")
DIAG_DIR = os.path.join(SCRIPTS_DIR, "diagramas")
SALIDAS_DIR = os.path.join(SCRIPTS_DIR, "salidas")
SRC_DIR = os.path.join(ACT_DIR, "src")

UNSA_GUINDA_HEX = "7B0C16"
LIGHT_BG_HEX = "F6F6F8"
CODE_BG_HEX = "F3F4F6"
BORDER_HEX = "CBD5E1"

UNSA_GUINDA_RGB = RGBColor(0x7B, 0x0C, 0x16)
TEXT_DARK_RGB = RGBColor(0x20, 0x21, 0x24)
MUTED_RGB = RGBColor(0x5F, 0x63, 0x68)
WHITE_RGB = RGBColor(0xFF, 0xFF, 0xFF)


def read_text(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read().strip()
    return f"(Archivo no encontrado: {path})"


def set_cell_shading(cell, color_hex):
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading)


def set_cell_margins(cell, top=70, bottom=70, left=110, right=110):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement("w:tcMar")
    for m, val in [("top", top), ("bottom", bottom), ("left", left), ("right", right)]:
        node = OxmlElement(f"w:{m}")
        node.set(qn("w:w"), str(val))
        node.set(qn("w:type"), "dxa")
        tcMar.append(node)
    tcPr.append(tcMar)


def set_table_borders(table, border_color=BORDER_HEX):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="6" w:space="0" w:color="{border_color}"/>'
        f'<w:bottom w:val="single" w:sz="6" w:space="0" w:color="{border_color}"/>'
        f'<w:left w:val="single" w:sz="6" w:space="0" w:color="{border_color}"/>'
        f'<w:right w:val="single" w:sz="6" w:space="0" w:color="{border_color}"/>'
        f'<w:insideH w:val="single" w:sz="4" w:space="0" w:color="{border_color}"/>'
        f'<w:insideV w:val="single" w:sz="4" w:space="0" w:color="{border_color}"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)


def add_page_number_to_run(run):
    fldChar1 = parse_xml(r'<w:fldChar %s w:fldCharType="begin"/>' % nsdecls("w"))
    instrText = parse_xml(r'<w:instrText %s xml:space="preserve"> PAGE </w:instrText>' % nsdecls("w"))
    fldChar2 = parse_xml(r'<w:fldChar %s w:fldCharType="separate"/>' % nsdecls("w"))
    fldChar3 = parse_xml(r'<w:fldChar %s w:fldCharType="end"/>' % nsdecls("w"))
    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)
    run._r.append(fldChar3)


def add_section_heading(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    pPr = p._p.get_or_add_pPr()
    pBdr = parse_xml(
        f'<w:pBdr {nsdecls("w")}>'
        f'<w:bottom w:val="single" w:sz="12" w:space="3" w:color="{UNSA_GUINDA_HEX}"/>'
        f'</w:pBdr>'
    )
    pPr.append(pBdr)
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(13.5)
    r.font.bold = True
    r.font.color.rgb = UNSA_GUINDA_RGB
    return p


def add_subheading(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.color.rgb = TEXT_DARK_RGB
    return p


def add_body_p(doc, text, bold_prefix=None, space_after=6):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        rb = p.add_run(bold_prefix)
        rb.font.name = "Times New Roman"
        rb.font.size = Pt(11.5)
        rb.font.bold = True
        rb.font.color.rgb = TEXT_DARK_RGB
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(11.5)
    r.font.color.rgb = TEXT_DARK_RGB
    return p


def add_bullet(doc, bold_prefix, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.left_indent = Inches(0.32)
    p.paragraph_format.first_line_indent = Inches(-0.16)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15

    r_bul = p.add_run("•  ")
    r_bul.font.name = "Times New Roman"
    r_bul.font.size = Pt(11)
    r_bul.font.bold = True
    r_bul.font.color.rgb = UNSA_GUINDA_RGB

    if bold_prefix:
        rb = p.add_run(bold_prefix)
        rb.font.name = "Times New Roman"
        rb.font.size = Pt(11)
        rb.font.bold = True
        rb.font.color.rgb = TEXT_DARK_RGB

    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.font.color.rgb = TEXT_DARK_RGB
    return p


def add_figure(doc, img_path, caption_text, width_in=5.8):
    if not os.path.exists(img_path):
        return
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(4)
    p_img.paragraph_format.space_after = Pt(2)
    p_img.add_run().add_picture(img_path, width=Inches(width_in))

    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_after = Pt(8)
    rcap = p_cap.add_run(caption_text)
    rcap.font.name = "Times New Roman"
    rcap.font.size = Pt(9.5)
    rcap.font.italic = True
    rcap.font.color.rgb = MUTED_RGB


def add_code_block(doc, title, code_text, font_size=8.2):
    tbl = doc.add_table(rows=2, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl, BORDER_HEX)

    c0 = tbl.cell(0, 0)
    set_cell_shading(c0, UNSA_GUINDA_HEX)
    set_cell_margins(c0, top=50, bottom=50, left=105, right=105)
    p0 = c0.paragraphs[0]
    p0.paragraph_format.space_after = Pt(0)
    r0 = p0.add_run(title)
    r0.font.name = "Consolas"
    r0.font.size = Pt(9)
    r0.font.bold = True
    r0.font.color.rgb = WHITE_RGB

    c1 = tbl.cell(1, 0)
    set_cell_shading(c1, CODE_BG_HEX)
    set_cell_margins(c1, top=70, bottom=70, left=105, right=105)
    p1 = c1.paragraphs[0]
    p1.paragraph_format.space_after = Pt(0)
    p1.paragraph_format.line_spacing = 1.05
    r1 = p1.add_run(code_text)
    r1.font.name = "Consolas"
    r1.font.size = Pt(font_size)
    r1.font.color.rgb = TEXT_DARK_RGB

    sp = doc.add_paragraph()
    sp.paragraph_format.space_after = Pt(4)


def add_styled_table(doc, headers, rows):
    tbl = doc.add_table(rows=len(rows) + 1, cols=len(headers))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl, BORDER_HEX)

    for c_idx, h in enumerate(headers):
        cell = tbl.cell(0, c_idx)
        set_cell_shading(cell, UNSA_GUINDA_HEX)
        set_cell_margins(cell, top=70, bottom=70, left=95, right=95)
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(h)
        r.font.name = "Times New Roman"
        r.font.size = Pt(10.5)
        r.font.bold = True
        r.font.color.rgb = WHITE_RGB

    for r_idx, row_vals in enumerate(rows, start=1):
        bg = LIGHT_BG_HEX if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row_vals):
            cell = tbl.cell(r_idx, c_idx)
            set_cell_shading(cell, bg)
            set_cell_margins(cell, top=60, bottom=60, left=95, right=95)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(val)
            r.font.name = "Times New Roman"
            r.font.size = Pt(10)
            r.font.bold = (c_idx == 0)
            r.font.color.rgb = TEXT_DARK_RGB

    sp = doc.add_paragraph()
    sp.paragraph_format.space_after = Pt(4)


def build_report():
    if not os.path.exists(TEMPLATE_PATH):
        raise FileNotFoundError(f"No se encontró la plantilla en: {TEMPLATE_PATH}")

    doc = Document(TEMPLATE_PATH)

    # Actualizar carátula respetando el banner, escudo y tipografía de la plantilla
    for idx, p in enumerate(doc.paragraphs):
        if "ACTIVIDAD 5" in p.text:
            if p.runs:
                p.runs[0].text = "ACTIVIDAD 5: PATRONES DE DISEÑO COMPORTAMENTALES (OBSERVER, STRATEGY Y COMMAND)"
                p.runs[0].font.name = "Times New Roman"
                p.runs[0].font.size = Pt(13.5)
                p.runs[0].font.bold = True
                p.runs[0].font.color.rgb = UNSA_GUINDA_RGB
        elif p.text.strip() == "INTEGRANTES:":
            if idx + 1 < len(doc.paragraphs):
                p_next = doc.paragraphs[idx + 1]
                p_next.alignment = WD_ALIGN_PARAGRAPH.LEFT
                r_int = p_next.add_run("    •  [Completar Apellidos y Nombres — CUI]")
                r_int.font.name = "Times New Roman"
                r_int.font.size = Pt(13)
                r_int.font.color.rgb = TEXT_DARK_RGB

    # Encabezado y pie de página desde la página 2
    section = doc.sections[0]
    section.different_first_page_header_footer = True

    hdr = section.header
    hp = hdr.paragraphs[0]
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    hr = hp.add_run("UNSA — Tecnología de Objetos (TO)  |  Patrones Comportamentales: Observer, Strategy y Command")
    hr.font.name = "Times New Roman"
    hr.font.size = Pt(9.5)
    hr.font.italic = True
    hr.font.color.rgb = MUTED_RGB

    ftr = section.footer
    fp = ftr.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fr1 = fp.add_run("Escuela Profesional de Ingeniería de Sistemas — Informe de Práctica   |   Página ")
    fr1.font.name = "Times New Roman"
    fr1.font.size = Pt(9.5)
    fr1.font.color.rgb = MUTED_RGB
    fr_num = fp.add_run()
    fr_num.font.name = "Times New Roman"
    fr_num.font.size = Pt(9.5)
    fr_num.font.bold = True
    fr_num.font.color.rgb = UNSA_GUINDA_RGB
    add_page_number_to_run(fr_num)

    doc.add_page_break()

    # =========================================================================
    # 1. INTRODUCCIÓN A LOS PATRONES COMPORTAMENTALES Y OBJETIVOS
    # =========================================================================
    add_section_heading(doc, "1. Introducción a los Patrones de Diseño Comportamentales y Objetivos")
    add_body_p(doc, (
        "En la ingeniería de software orientada a objetos, la calidad de un sistema no solo depende de cómo se estructuran "
        "sus clases, sino de cómo colaboran los objetos entre sí en tiempo de ejecución. Los patrones de diseño comportamentales "
        "(definidos en el catálogo clásico del Gang of Four - GoF) ofrecen soluciones probadas y reutilizables para gestionar "
        "algoritmos, flujos de comunicación y distribución de responsabilidades entre objetos, evitando dependencias rígidas."
    ))
    add_body_p(doc, (
        "En la presente actividad del curso de Tecnología de Objetos se implementaron, compilaron y verificaron en Java "
        "(OpenJDK 21.0.13.1 LTS) tres ejercicios prácticos independientes dentro de la carpeta exclusiva actividad-patrones-diseno/, "
        "demostrando la aplicación directa y limpia de los patrones Observer, Strategy y Command."
    ))

    add_subheading(doc, "1.1 Objetivos de la Actividad")
    add_bullet(doc, "Patrón Observer: ", "Construir un sistema de notificaciones uno-a-muchos que permita suscribir, desuscribir y notificar automáticamente a múltiples usuarios sin acoplar el emisor a clases concretas.")
    add_bullet(doc, "Patrón Strategy: ", "Diseñar una calculadora de precios capaz de intercambiar distintas reglas de promoción en tiempo de ejecución sin recurrir a condicionales rígidos.")
    add_bullet(doc, "Patrón Command: ", "Encapsular cinco acciones de un televisor dentro de objetos comando independientes para que un control remoto genérico pueda invocarlas de manera uniforme.")

    # =========================================================================
    # 2. EJERCICIO 1: PATRÓN OBSERVER
    # =========================================================================
    add_section_heading(doc, "2. Ejercicio 1: Patrón Observer — Sistema de Notificaciones")
    add_body_p(doc, (
        "El patrón Observer establece una relación de suscripción uno-a-muchos entre un Sujeto (Observable) y múltiples "
        "Observadores. Cuando el sujeto emite un evento, todos los observadores registrados son notificados automáticamente "
        "a través de una interfaz común, permitiendo agregar o retirar suscriptores en cualquier momento."
    ))

    add_styled_table(doc, ["Rol del Patrón", "Archivo / Clase", "Responsabilidad en el Ejercicio"], [
        ["Interfaz Observer", "Observer.java", "Declara el contrato actualizar(String mensaje) que todo suscriptor debe implementar."],
        ["Observador Concreto", "Usuario.java", "Almacena el nombre del usuario e imprime la notificación recibida cuando se invoca actualizar()."],
        ["Sujeto (Observable)", "SistemaNotificaciones.java", "Mantiene la lista List<Observer> e implementa registrar(), eliminar() y notificar()."],
        ["Cliente", "Main.java", "Registra usuarios (Ana, Carlos, Lucía), emite alertas, desuscribe a Carlos, suma a Diego y valida los resultados."]
    ])

    add_figure(doc, os.path.join(DIAG_DIR, "diagrama_observer.png"),
               "Figura 1. Diagrama de relaciones y flujo de notificación del patrón Observer.")

    add_subheading(doc, "2.1 Código Fuente Completo (src/observer/)")
    for fname in ["Observer.java", "Usuario.java", "SistemaNotificaciones.java", "Main.java"]:
        add_code_block(doc, f"actividad-patrones-diseno/src/observer/{fname}",
                       read_text(os.path.join(SRC_DIR, "observer", fname)))

    add_subheading(doc, "2.2 Resultado Real de Ejecución (Observer)")
    add_body_p(doc, (
        "La compilación con javac -Xlint:all -encoding UTF-8 finalizó con 0 errores y 0 advertencias. La salida real "
        "confirma que al desuscribir a Carlos deja de recibir los mensajes posteriores y que Diego recibe el último aviso:"
    ))
    add_code_block(doc, "Salida Real de Consola — observer.Main",
                   read_text(os.path.join(SALIDAS_DIR, "salida_observer.txt")), font_size=8.3)

    # =========================================================================
    # 3. EJERCICIO 2: PATRÓN STRATEGY
    # =========================================================================
    add_section_heading(doc, "3. Ejercicio 2: Patrón Strategy — Promociones de Productos")
    add_body_p(doc, (
        "El patrón Strategy encapsula una familia de algoritmos intercambiables detrás de una interfaz común. En lugar de "
        "concentrar múltiples bloques if/else dentro de la calculadora de precios, cada tipo de promoción vive en su propia "
        "clase, cumpliendo el principio Abierto/Cerrado (SOLID)."
    ))

    add_styled_table(doc, ["Rol del Patrón", "Archivo / Clase", "Responsabilidad en el Ejercicio"], [
        ["Interfaz Strategy", "EstrategiaPromocion.java", "Define aplicarPromocion(double precioUnitario, int cantidad) y getDescripcion()."],
        ["Estrategia Concreta 1", "SinDescuento.java", "Calcula el precio regular sin rebajas (precioUnitario * cantidad)."],
        ["Estrategia Concreta 2", "DescuentoPorcentaje.java", "Aplica una rebaja porcentual validada entre 0% y 100% (ejemplo: 20%)."],
        ["Estrategia Concreta 3", "DescuentoMontoFijo.java", "Resta un monto fijo al subtotal garantizando un total mínimo de S/ 0.00."],
        ["Estrategia Concreta 4", "PromocionDosPorUno.java", "Cobra solo 1 de cada 2 unidades ((cantidad / 2) + (cantidad % 2))."],
        ["Contexto", "CalculadoraPrecios.java", "Mantiene la estrategia activa y ofrece setEstrategia() para cambiarla en ejecución."],
        ["Cliente", "Main.java", "Evalúa las 4 estrategias sobre 4 Audífonos Bluetooth de S/ 120.00 (subtotal S/ 480.00)."]
    ])

    add_figure(doc, os.path.join(DIAG_DIR, "diagrama_strategy.png"),
               "Figura 2. Estructura del patrón Strategy con intercambio dinámico de promociones.")

    add_subheading(doc, "3.1 Código Fuente Relevante (src/strategy/)")
    for fname in ["EstrategiaPromocion.java", "CalculadoraPrecios.java", "DescuentoPorcentaje.java",
                  "DescuentoMontoFijo.java", "PromocionDosPorUno.java", "Main.java"]:
        add_code_block(doc, f"actividad-patrones-diseno/src/strategy/{fname}",
                       read_text(os.path.join(SRC_DIR, "strategy", fname)), font_size=8.0)

    add_subheading(doc, "3.2 Resultado Real de Ejecución (Strategy)")
    add_body_p(doc, (
        "En la ejecución real se observa cómo la misma instancia de CalculadoraPrecios produce totales distintos "
        "(S/ 480.00, S/ 384.00, S/ 405.00 y S/ 240.00) simplemente intercambiando la estrategia mediante setEstrategia():"
    ))
    add_code_block(doc, "Salida Real de Consola — strategy.Main",
                   read_text(os.path.join(SALIDAS_DIR, "salida_strategy.txt")), font_size=8.3)

    # =========================================================================
    # 4. EJERCICIO 3: PATRÓN COMMAND
    # =========================================================================
    add_section_heading(doc, "4. Ejercicio 3: Patrón Command — Control Remoto de Televisor")
    add_body_p(doc, (
        "El patrón Command convierte cada solicitud de acción en un objeto autónomo que implementa un método único execute(). "
        "De esta forma, el invocador (ControlRemoto) se desacopla por completo del receptor (Televisor), ya que el botón "
        "del control únicamente ejecuta el comando asignado sin conocer qué operación física realiza."
    ))

    add_styled_table(doc, ["Rol del Patrón", "Archivo / Clase", "Responsabilidad en el Ejercicio"], [
        ["Interfaz Command", "Command.java", "Declara el método único execute() para encapsular cualquier acción."],
        ["Receptor", "Televisor.java", "Implementa las 5 acciones reales: encender(), apagar(), subirVolumen(), bajarVolumen() y cambiarCanal()."],
        ["Comandos Concretos (5)", "*Command.java", "EncenderTelevisorCommand, ApagarTelevisorCommand, SubirVolumenCommand, BajarVolumenCommand y CambiarCanalCommand."],
        ["Invocador", "ControlRemoto.java", "Guarda un Command mediante setCommand() y lo dispara en presionarBoton()."],
        ["Cliente", "Main.java", "Crea el televisor, configura los 5 comandos en el control remoto y los ejecuta en orden."]
    ])

    add_figure(doc, os.path.join(DIAG_DIR, "diagrama_command.png"),
               "Figura 3. Desacoplamiento Invocador-Comando-Receptor en el patrón Command (5 funcionalidades).")

    add_subheading(doc, "4.1 Código Fuente Relevante (src/command/)")
    for fname in ["Command.java", "Televisor.java", "ControlRemoto.java",
                  "EncenderTelevisorCommand.java", "CambiarCanalCommand.java", "Main.java"]:
        add_code_block(doc, f"actividad-patrones-diseno/src/command/{fname}",
                       read_text(os.path.join(SRC_DIR, "command", fname)), font_size=8.0)

    add_subheading(doc, "4.2 Resultado Real de Ejecución (Command)")
    add_body_p(doc, (
        "La salida real verifica la ejecución ordenada de las 5 funcionalidades solicitadas sobre el receptor Televisor "
        "a través del invocador ControlRemoto:"
    ))
    add_code_block(doc, "Salida Real de Consola — command.Main",
                   read_text(os.path.join(SALIDAS_DIR, "salida_command.txt")), font_size=8.3)

    # =========================================================================
    # 5. CUADRO COMPARATIVO DE LOS PATRONES IMPLEMENTADOS
    # =========================================================================
    add_section_heading(doc, "5. Cuadro Comparativo de los Patrones Comportamentales")
    add_styled_table(doc, ["Criterio", "Observer", "Strategy", "Command"], [
        ["Intención principal", "Notificar automáticamente cambios o eventos a múltiples suscriptores.", "Intercambiar algoritmos o reglas de cálculo en tiempo de ejecución.", "Encapsular peticiones como objetos para desacoplar quien pide de quien ejecuta."],
        ["Relación dominante", "Uno a muchos (Sujeto -> Observadores).", "Uno a uno intercambiable (Contexto -> Estrategia).", "Invocador -> Comando -> Receptor."],
        ["Problema que evita", "Acoplamiento entre emisor y receptores; consultas repetitivas (polling).", "Condicionales extensos (if/else o switch) en la lógica de cálculo.", "Invocador acoplado a métodos concretos del receptor."],
        ["Facilidad de extensión", "Añadir nuevas clases Observer sin modificar el sujeto.", "Añadir nuevas EstrategiaPromocion sin modificar CalculadoraPrecios.", "Añadir nuevos botones/comandos sin modificar ControlRemoto."],
        ["Caso implementado", "Sistema de notificaciones para usuarios (Ana, Carlos, Lucía, Diego).", "Calculadora de precios con 4 promociones (regular, %, fijo, 2x1).", "Control remoto de televisor con 5 acciones independientes."]
    ])

    # =========================================================================
    # 6. CONCLUSIONES
    # =========================================================================
    add_section_heading(doc, "6. Conclusiones")
    add_bullet(doc, "Reducción efectiva del acoplamiento: ", "En los tres ejercicios, programar contra interfaces (Observer, EstrategiaPromocion y Command) permitió que las clases coordinadoras trabajen sin depender de implementaciones concretas.")
    add_bullet(doc, "Flexibilidad en tiempo de ejecución: ", "Observer permite suscribir y retirar usuarios dinámicamente; Strategy cambia reglas de descuento al vuelo mediante setEstrategia(); y Command permite reasignar acciones al mismo botón del control remoto.")
    add_bullet(doc, "Código limpio y extensible: ", "Cada clase cumple una responsabilidad única y clara, facilitando agregar nuevas promociones, tipos de observadores o comandos del televisor sin alterar el código existente.")
    add_bullet(doc, "Verificación completa en Java 21: ", "Los 20 archivos fuente compilaron con cero advertencias (-Xlint:all) y produjeron salidas exactas que validan todos los requerimientos funcionales solicitados.")

    out_path = os.path.join(ACT_DIR, "Informe_Patrones_Diseno.docx")
    doc.save(out_path)
    print("Informe generado exitosamente:", out_path)


if __name__ == "__main__":
    build_report()
