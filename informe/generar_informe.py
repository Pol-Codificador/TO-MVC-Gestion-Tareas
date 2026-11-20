"""
Generador de Informe Técnico Académico (.docx) basado en la plantilla oficial UNSA
Curso: Tecnología de Objetos (TO)
Docente: Mg. Diego Alonso Iquira Becerra

Carga directamente 'informe/plantilla_base.docx' para conservar intactos la carátula,
el banner institucional UNSA, el escudo, los márgenes (2.54 cm), tamaño A4 y tipografía
Times New Roman (#202124), y agrega el contenido completo del informe a partir de la página 2.
"""
import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INF_DIR = os.path.dirname(os.path.abspath(__file__))
PRES_DIR = os.path.join(BASE_DIR, "presentacion")
TEMPLATE_PATH = os.path.join(INF_DIR, "plantilla_base.docx")

# Paleta alineada a la plantilla oficial UNSA (banner guinda/carmesí + dorado + #202124)
UNSA_GUINDA_HEX = "7B0C16"
DARK_HEX = "202124"
LIGHT_BG_HEX = "F6F6F8"
CODE_BG_HEX = "F3F4F6"
BORDER_HEX = "CBD5E1"

UNSA_GUINDA_RGB = RGBColor(0x7B, 0x0C, 0x16)
TEXT_DARK_RGB = RGBColor(0x20, 0x21, 0x24)
MUTED_RGB = RGBColor(0x5F, 0x63, 0x68)
WHITE_RGB = RGBColor(0xFF, 0xFF, 0xFF)


def read_file_text(rel_path):
    full = os.path.join(BASE_DIR, rel_path)
    if os.path.exists(full):
        with open(full, "r", encoding="utf-8", errors="replace") as f:
            return f.read().strip()
    return f"(Archivo no encontrado: {rel_path})"


def set_cell_shading(cell, color_hex):
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading)


def set_cell_margins(cell, top=75, bottom=75, left=120, right=120):
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
    fldChar1 = parse_xml(r'<w:fldChar %s w:fldCharType="begin"/>' % nsdecls('w'))
    instrText = parse_xml(r'<w:instrText %s xml:space="preserve"> PAGE </w:instrText>' % nsdecls('w'))
    fldChar2 = parse_xml(r'<w:fldChar %s w:fldCharType="separate"/>' % nsdecls('w'))
    fldChar3 = parse_xml(r'<w:fldChar %s w:fldCharType="end"/>' % nsdecls('w'))
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


def add_code_block(doc, title, code_text, font_size=8.2):
    tbl = doc.add_table(rows=2, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl, BORDER_HEX)

    # Cabecera del bloque
    c0 = tbl.cell(0, 0)
    set_cell_shading(c0, UNSA_GUINDA_HEX)
    set_cell_margins(c0, top=55, bottom=55, left=110, right=110)
    p0 = c0.paragraphs[0]
    p0.paragraph_format.space_after = Pt(0)
    r0 = p0.add_run(title)
    r0.font.name = "Consolas"
    r0.font.size = Pt(9)
    r0.font.bold = True
    r0.font.color.rgb = WHITE_RGB

    # Contenido de código
    c1 = tbl.cell(1, 0)
    set_cell_shading(c1, CODE_BG_HEX)
    set_cell_margins(c1, top=75, bottom=75, left=110, right=110)
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
        set_cell_margins(cell, top=75, bottom=75, left=100, right=100)
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
            set_cell_margins(cell, top=65, bottom=65, left=100, right=100)
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


def build_report_from_template():
    if not os.path.exists(TEMPLATE_PATH):
        raise FileNotFoundError(f"No se encontró la plantilla base en: {TEMPLATE_PATH}")

    # 1. Cargar la plantilla oficial exacta
    doc = Document(TEMPLATE_PATH)

    # 2. Actualizar únicamente los campos de la carátula manteniendo intactos
    #    el banner UNSA, el escudo, los márgenes y la tipografía Times New Roman 15pt
    for idx, p in enumerate(doc.paragraphs):
        if "ACTIVIDAD 5" in p.text:
            # Conservar formato del primer run
            if p.runs:
                p.runs[0].text = "ACTIVIDAD 5: PATRÓN ARQUITECTÓNICO MODELO-VISTA-CONTROLADOR (MVC)"
                p.runs[0].font.name = "Times New Roman"
                p.runs[0].font.size = Pt(14)
                p.runs[0].font.bold = True
                p.runs[0].font.color.rgb = UNSA_GUINDA_RGB
        elif p.text.strip() == "INTEGRANTES:":
            # Insertar placeholder claro en el párrafo siguiente (P25) sin mover el resto
            if idx + 1 < len(doc.paragraphs):
                p_next = doc.paragraphs[idx + 1]
                p_next.alignment = WD_ALIGN_PARAGRAPH.LEFT
                r_int = p_next.add_run("    •  [Completar Apellidos y Nombres — CUI]")
                r_int.font.name = "Times New Roman"
                r_int.font.size = Pt(13)
                r_int.font.color.rgb = TEXT_DARK_RGB

    # 3. Configurar encabezado y pie de página SOLO para las páginas 2 en adelante
    #    (la página 1 conserva la carátula oficial limpia sin encabezados extra)
    section = doc.sections[0]
    section.different_first_page_header_footer = True

    hdr = section.header
    hp = hdr.paragraphs[0]
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    hr = hp.add_run("UNSA — Tecnología de Objetos (TO)  |  Actividad 5: Patrón Arquitectónico MVC")
    hr.font.name = "Times New Roman"
    hr.font.size = Pt(9.5)
    hr.font.italic = True
    hr.font.color.rgb = MUTED_RGB

    ftr = section.footer
    fp = ftr.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fr1 = fp.add_run("Escuela Profesional de Ingeniería de Sistemas — Informe de Laboratorio   |   Página ")
    fr1.font.name = "Times New Roman"
    fr1.font.size = Pt(9.5)
    fr1.font.color.rgb = MUTED_RGB
    fr_num = fp.add_run()
    fr_num.font.name = "Times New Roman"
    fr_num.font.size = Pt(9.5)
    fr_num.font.bold = True
    fr_num.font.color.rgb = UNSA_GUINDA_RGB
    add_page_number_to_run(fr_num)

    # Salto de página después de la carátula oficial
    doc.add_page_break()

    # =========================================================================
    # 1. INTRODUCCIÓN Y OBJETIVOS
    # =========================================================================
    add_section_heading(doc, "1. Introducción y Objetivos")
    add_body_p(doc, (
        "En el desarrollo de aplicaciones orientadas a objetos, mantener una separación clara entre los datos del dominio, "
        "la lógica de control y la presentación al usuario es indispensable para evitar software rígido y difícil de mantener. "
        "El patrón arquitectónico Modelo-Vista-Controlador (MVC) aborda directamente este desafío al dividir el sistema en tres "
        "capas desacopladas con responsabilidades bien definidas."
    ))
    add_body_p(doc, (
        "En la presente práctica de laboratorio (Actividad 5) del curso de Tecnología de Objetos, se diseña, implementa, compila "
        "y verifica un sistema de gestión de tareas en Java (OpenJDK 21.0.13.1 LTS) en dos etapas progresivas: la Actividad 1 "
        "implementa la versión base pura de MVC en memoria, y la Actividad 2 escala dicha arquitectura incorporando operaciones "
        "CRUD completas, enumeraciones tipificadas, persistencia real en archivo CSV UTF-8 mediante una capa de repositorio "
        "(TaskRepository), filtros, búsqueda por palabra clave, estadísticas y menú interactivo tolerante a fallos."
    ))

    add_subheading(doc, "1.1 Objetivo General")
    add_body_p(doc, (
        "Aplicar el patrón arquitectónico Modelo-Vista-Controlador (MVC) en Java para construir y escalar un gestor de tareas "
        "modular, comprobando sus beneficios en mantenibilidad, encapsulamiento y persistencia de datos."
    ))

    add_subheading(doc, "1.2 Objetivos Específicos")
    add_bullet(doc, "Diferenciar ", "los patrones de diseño de los patrones arquitectónicos y comprender el flujo de comunicación de MVC.")
    add_bullet(doc, "Desarrollar la Actividad 1 ", "implementando las clases Task (Modelo), TaskView (Vista), TaskController (Controlador) y Main con validación de índices.")
    add_bullet(doc, "Escalar el sistema en la Actividad 2 ", "agregando actualización, eliminación, persistencia en archivo CSV UTF-8, prioridades, filtros, búsqueda, estadísticas y lectura segura en consola.")
    add_bullet(doc, "Verificar la compilación y ejecución real ", "de ambas actividades sin errores ni advertencias, documentando las salidas reales de consola y el archivo persistido.")

    # =========================================================================
    # 2. MARCO TEÓRICO
    # =========================================================================
    add_section_heading(doc, "2. Marco Teórico")
    add_subheading(doc, "2.1 Patrones de Diseño vs. Patrones Arquitectónicos")
    add_body_p(doc, (
        "Los patrones de diseño ofrecen soluciones reutilizables a problemas recurrentes a nivel de clases y objetos individuales "
        "(por ejemplo, Singleton, Factory o Strategy). Por su parte, los patrones arquitectónicos definen la estructura macro del "
        "sistema completo, estableciendo cómo se organizan los subsistemas principales y qué reglas rigen su interacción. "
        "MVC es un patrón arquitectónico orientado a sistemas interactivos."
    ))

    add_subheading(doc, "2.2 Componentes y Flujo de Trabajo de MVC")
    add_bullet(doc, "Modelo (Model): ", "Administra los datos, el estado y las reglas de negocio (incluyendo el acceso a persistencia). No depende de ninguna interfaz de usuario.")
    add_bullet(doc, "Vista (View): ", "Se limita a presentar información al usuario y capturar sus entradas. No contiene lógica de negocio ni modifica directamente al Modelo.")
    add_bullet(doc, "Controlador (Controller): ", "Coordina el flujo entre la Vista y el Modelo: recibe las acciones del usuario, valida parámetros, invoca cambios en el Modelo y solicita a la Vista mostrar resultados.")

    img_mvc = os.path.join(PRES_DIR, "diagrama_mvc_flujo.png")
    if os.path.exists(img_mvc):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture(img_mvc, width=Inches(5.8))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(8)
        rcap = p_cap.add_run("Figura 1. Flujo arquitectónico de comunicación del patrón Modelo-Vista-Controlador (MVC).")
        rcap.font.name = "Times New Roman"
        rcap.font.size = Pt(9.5)
        rcap.font.italic = True
        rcap.font.color.rgb = MUTED_RGB

    add_subheading(doc, "2.3 Beneficios del Patrón MVC")
    add_bullet(doc, "Bajo acoplamiento y alta cohesión: ", "Los cambios en la interfaz (ej. pasar de consola a JavaFX) no alteran la lógica del Modelo.")
    add_bullet(doc, "Escalabilidad ordenada: ", "Permite agregar nuevas funcionalidades y capas auxiliares (como repositorios) sin degradar la estructura.")
    add_bullet(doc, "Facilidad de pruebas y trabajo colaborativo: ", "Cada componente puede probarse y desarrollarse de manera independiente.")

    # =========================================================================
    # 3. DESARROLLO DE LA ACTIVIDAD 1
    # =========================================================================
    add_section_heading(doc, "3. Desarrollo de la Actividad 1: Implementación Base MVC")
    add_body_p(doc, (
        "La Actividad 1 se implementó en la carpeta actividad 1/ con cuatro clases Java que reflejan de manera directa "
        "y didáctica las tres capas de MVC más el punto de entrada Main."
    ))

    add_styled_table(doc, ["Archivo", "Capa MVC", "Responsabilidad Principal"], [
        ["Task.java", "Modelo", "Encapsula name (String) y completed (boolean). Constructor inicializa completed = false. Métodos: getName(), isCompleted(), complete()."],
        ["TaskView.java", "Vista", "Presenta las tareas con índice, nombre y estado (printTasks) e imprime mensajes informativos o de error (printMessage)."],
        ["TaskController.java", "Controlador", "Administra List<Task> y TaskView. Implementa addTask(), completeTask(index) con validación de límites y displayTasks()."],
        ["Main.java", "Aplicación", "Ensambla Vista y Controlador, añade 3 tareas, lista, completa el índice 1, prueba el índice inválido 10 y vuelve a listar."]
    ])

    add_subheading(doc, "3.1 Código Fuente Completo (Actividad 1)")
    for fname in ["Task.java", "TaskView.java", "TaskController.java", "Main.java"]:
        add_code_block(doc, f"actividad 1/{fname}", read_file_text(os.path.join("actividad 1", fname)))

    add_subheading(doc, "3.2 Evidencia de Compilación y Ejecución Real (Actividad 1)")
    add_body_p(doc, (
        "Se compiló con javac -Xlint:all -encoding UTF-8 *.java en OpenJDK 21.0.13.1 obteniendo 0 errores y 0 advertencias. "
        "La ejecución real demuestra el cambio de estado de la tarea [1] y el rechazo controlado del índice inválido (10):"
    ))
    add_code_block(doc, "Salida Real de Consola — Actividad 1", read_file_text(os.path.join("actividad 1", "salida_actividad1.txt")), font_size=8.4)

    # =========================================================================
    # 4. DESARROLLO DE LA ACTIVIDAD 2
    # =========================================================================
    add_section_heading(doc, "4. Desarrollo de la Actividad 2: Versión Mejorada y Escalada MVC")
    add_body_p(doc, (
        "Partiendo de la base de la Actividad 1, la Actividad 2 (carpeta actividad 2/) incorpora persistencia en disco, "
        "operaciones CRUD completas, modelo enriquecido, filtros, búsqueda, estadísticas y menú interactivo con validación "
        "segura de entradas."
    ))

    add_subheading(doc, "4.1 Arquitectura Escalada y Justificación de Diseño")
    img_a2 = os.path.join(PRES_DIR, "diagrama_arquitectura_act2.png")
    if os.path.exists(img_a2):
        p_img2 = doc.add_paragraph()
        p_img2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img2.add_run().add_picture(img_a2, width=Inches(5.8))
        p_cap2 = doc.add_paragraph()
        p_cap2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap2.paragraph_format.space_after = Pt(8)
        rcap2 = p_cap2.add_run("Figura 2. Arquitectura MVC escalada de la Actividad 2 con Priority y TaskRepository (SRP).")
        rcap2.font.name = "Times New Roman"
        rcap2.font.size = Pt(9.5)
        rcap2.font.italic = True
        rcap2.font.color.rgb = MUTED_RGB

    add_bullet(doc, "Priority.java (Enum): ", "Tipifica las prioridades válidas (ALTA, MEDIA, BAJA) y convierte entradas numéricas o textuales con fromInput(), evitando cadenas inválidas.")
    add_bullet(doc, "Task.java enriquecido: ", "Añade id autoincremental, description, priority y createdAt (LocalDateTime), además de setters validados y toggleCompleted().")
    add_bullet(doc, "TaskRepository.java (Capa de Persistencia - SRP): ", "Desacopla la lectura y escritura del archivo tareas.csv en UTF-8 con manejo explícito de IOException, cierre seguro mediante try-with-resources y saneamiento de delimitadores (;).")
    add_bullet(doc, "TaskView.java mejorado: ", "Ofrece menú de 12 opciones, listado tabular alineado, panel de estadísticas con barra visual ASCII y lectura segura de enteros (readInt usando nextLine + Integer.parseInt) que previene InputMismatchException.")
    add_bullet(doc, "TaskController.java ampliado: ", "Gestiona creación, listado, actualización parcial (manteniendo valores si se deja vacío), alternancia de estado, eliminación validada, filtros por estado/prioridad, búsqueda por palabra clave, estadísticas, guardado/carga y recálculo automático de nextId.")

    add_subheading(doc, "4.2 Código Fuente Completo (Actividad 2)")
    for fname in ["Priority.java", "Task.java", "TaskRepository.java", "TaskView.java", "TaskController.java", "Main.java"]:
        add_code_block(doc, f"actividad 2/{fname}", read_file_text(os.path.join("actividad 2", fname)), font_size=7.6)

    add_subheading(doc, "4.3 Evidencia de Pruebas Reales y Persistencia en tareas.csv")
    add_body_p(doc, (
        "Tras compilar sin advertencias (javac -Xlint:all -encoding UTF-8 *.java), se ejecutó una prueba automatizada completa "
        "por entrada estándar (stdin) verificando: adición de 4 tareas, listado, cambio de estado, actualización parcial, filtros "
        "(pendientes y prioridad alta), búsqueda ('CSV'), estadísticas, eliminación por índice, manejo de texto inválido ('abc'), "
        "guardado en tareas.csv, limpieza de memoria RAM y recarga íntegra desde disco."
    ))
    add_code_block(doc, "Archivo de Persistencia Generado: actividad 2/tareas.csv", read_file_text(os.path.join("actividad 2", "tareas.csv")), font_size=8.4)

    raw_a2 = read_file_text(os.path.join("actividad 2", "salida_actividad2.txt"))
    filtered_lines = [
        ln for ln in raw_a2.splitlines()
        if not ln.startswith("  ") or any(x in ln for x in ["Total de tareas", "Completadas", "Pendientes", "Avance general", "Por prioridad", "-----"])
    ]
    compact_a2 = "\n".join([
        ln for ln in filtered_lines
        if ln.strip() and not ln.startswith("--------------------------- MENÚ") and not ln.startswith("----------------------------------------------------------------------")
    ])
    add_code_block(doc, "Extracto de Salida Real de Prueba Automatizada — Actividad 2", compact_a2[:4200], font_size=7.6)

    # =========================================================================
    # 5. TABLA COMPARATIVA ACTIVIDAD 1 VS. ACTIVIDAD 2
    # =========================================================================
    add_section_heading(doc, "5. Tabla Comparativa: Actividad 1 vs. Actividad 2")
    add_styled_table(doc, ["Criterio", "Actividad 1 (Versión Base)", "Actividad 2 (Versión Escalada)"], [
        ["Clases del Proyecto", "4 clases (Task, TaskView, TaskController, Main)", "6 clases (+Priority enum y TaskRepository)"],
        ["Atributos del Modelo", "name, completed", "id, name, description, priority, completed, createdAt"],
        ["Operaciones CRUD", "Crear, Listar y Completar", "Crear, Listar, Actualizar parcial, Alternar estado y Eliminar"],
        ["Persistencia en Archivo", "No implementada (solo RAM)", "Persistencia CSV UTF-8 (tareas.csv) con manejo de IOException"],
        ["Consultas y Estadísticas", "Listado simple", "Filtros (estado/prioridad), búsqueda por palabra clave y métricas"],
        ["Interacción y Robustez", "Flujo fijo en Main", "Menú interactivo seguro (sin caídas por InputMismatchException)"],
        ["Principios Aplicados", "Encapsulamiento y MVC base", "MVC + SRP (repositorio desacoplado) + seguridad de tipos con Enum"]
    ])

    # =========================================================================
    # 6. CONCLUSIONES Y RECOMENDACIONES
    # =========================================================================
    add_section_heading(doc, "6. Conclusiones y Recomendaciones")
    add_subheading(doc, "6.1 Conclusiones")
    add_bullet(doc, "Escalabilidad demostrada de MVC: ", "La transición de la Actividad 1 a la Actividad 2 se realizó extendiendo limpiamente cada capa sin reescribir la arquitectura base.")
    add_bullet(doc, "Valor del Principio de Responsabilidad Única (SRP): ", "Separar la persistencia en TaskRepository mantuvo limpio a TaskController y centralizó la codificación UTF-8 y el control de IOException.")
    add_bullet(doc, "Tolerancia a fallos en consola: ", "Validar límites de índices y leer enteros mediante nextLine() + Integer.parseInt() eliminó excepciones por entradas inválidas del usuario.")
    add_bullet(doc, "Validación real completa: ", "Ambas actividades compilaron con cero advertencias en OpenJDK 21 y pasaron pruebas de ejecución reales comprobando la persistencia íntegra en tareas.csv.")

    add_subheading(doc, "6.2 Recomendaciones")
    add_bullet(doc, "Abstraer la persistencia con una interfaz: ", "Introducir ITaskRepository permitiría migrar de CSV a JSON o base de datos relacional (SQLite/PostgreSQL) sin modificar TaskController.")
    add_bullet(doc, "Incorporar pruebas unitarias (JUnit 5): ", "Automatizar pruebas sobre Task, TaskRepository y TaskController para detectar regresiones en futuras versiones.")
    add_bullet(doc, "Explorar una Vista gráfica: ", "Reutilizar el Modelo y el Repositorio actuales con una nueva Vista en JavaFX o Swing para evidenciar la independencia de la interfaz.")

    out_path = os.path.join(INF_DIR, "Informe_Laboratorio_MVC_Tareas.docx")
    doc.save(out_path)
    print(f"Informe generado exitosamente sobre la plantilla oficial UNSA: {out_path}")


if __name__ == "__main__":
    build_report_from_template()
