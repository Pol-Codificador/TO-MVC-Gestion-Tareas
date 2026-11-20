# Gestor de Tareas con Patrón Arquitectónico MVC en Java

Repositorio correspondiente a las prácticas de laboratorio del curso **Tecnología de Objetos (TO)**, enfocado en el diseño e implementación del **Patrón Arquitectónico Modelo–Vista–Controlador (MVC)** en Java.

---

## Estructura del Repositorio

```text
ACTIVIDADES TO/
├── actividad 1/                          # Implementación base del patrón MVC en Java
│   ├── Task.java                         # Modelo (entidad de tarea)
│   ├── TaskView.java                     # Vista de consola
│   ├── TaskController.java               # Controlador con operaciones básicas
│   ├── Main.java                         # Punto de entrada y flujo de demostración
│   └── salida_actividad1.txt             # Evidencia de salida en consola
│
├── actividad 2/                          # Versión avanzada: MVC + Persistencia (Repository)
│   ├── Priority.java                     # Enumeración de prioridades (ALTA, MEDIA, BAJA)
│   ├── Task.java                         # Modelo enriquecido (ID, descripción, prioridad, estado)
│   ├── TaskView.java                     # Vista interactiva de consola (menú, tablas, estadísticas)
│   ├── TaskRepository.java               # Capa de persistencia en archivo CSV
│   ├── TaskController.java               # Controlador con CRUD completo, filtros, búsqueda y persistencia
│   ├── Main.java                         # Punto de entrada del menú interactivo
│   ├── tareas.csv                        # Archivo de almacenamiento persistente de ejemplo
│   └── salida_actividad2.txt             # Evidencia de salida en consola
│
├── presentacion/                         # Material de exposición
│   ├── Presentacion_MVC_Tareas.pptx      # Diapositivas de la presentación
│   ├── diagrama_mvc_flujo.png            # Diagrama de flujo MVC
│   ├── diagrama_arquitectura_act2.png    # Diagrama de arquitectura de la Actividad 2
│   ├── generar_diagramas.py              # Script en Python para generar los diagramas
│   └── generar_presentacion.py           # Script en Python para generar la presentación
│
├── informe/                              # Documentación técnica del laboratorio
│   ├── Informe_Laboratorio_MVC_Tareas.docx  # Informe final del laboratorio
│   ├── plantilla_base.docx               # Plantilla base utilizada
│   └── generar_informe.py                # Script en Python para generar el informe
│
├── .gitignore
└── README.md
```

---

## Resumen de Actividades

### Actividad 1: Implementación Base del Patrón MVC
Implementación introductoria del patrón arquitectónico **Modelo–Vista–Controlador** en Java puro:
- **Modelo (`Task`)**: Representa una tarea con nombre y estado de completitud.
- **Vista (`TaskView`)**: Se encarga exclusivamente de mostrar en consola la lista de tareas y mensajes de retroalimentación.
- **Controlador (`TaskController`)**: Gestiona la colección de tareas en memoria, permite añadir tareas, marcarlas como completadas validando índices y coordinar la actualización de la vista.
- **Aplicación (`Main`)**: Ensambla los componentes y demuestra el flujo básico de alta, listado, completado y manejo de índice inválido.

### Actividad 2: Mejoras Avanzadas (MVC + Capa de Persistencia)
Evolución de la Actividad 1 hacia una aplicación interactiva más completa y desacoplada:
- **Modelo enriquecido (`Task` y `Priority`)**: Incorpora identificador único (`id`), descripción, nivel de prioridad (`ALTA`, `MEDIA`, `BAJA`) y alternancia de estado.
- **Menú interactivo completo**: Operaciones **CRUD** completas (crear, listar, editar, alternar estado y eliminar tareas) desde consola.
- **Filtros, búsqueda y estadísticas**: Filtrado por estado o prioridad, búsqueda por palabra clave en nombre o descripción, y resumen estadístico de tareas.
- **Persistencia en archivo (`TaskRepository`)**: Separación de responsabilidades mediante una capa de repositorio para guardar y cargar tareas en formato CSV (`tareas.csv`), además de limpiar la memoria sin alterar el archivo en disco.

---

## Compilación y Ejecución

Requisitos previos: tener instalado **JDK (Java Development Kit)** y disponible en el `PATH` (`javac` y `java`).

### Actividad 1

Desde la raíz del repositorio:

```bash
cd "actividad 1"
javac -encoding UTF-8 *.java
java Main
```

### Actividad 2

Desde la raíz del repositorio:

```bash
cd "actividad 2"
javac -encoding UTF-8 *.java
java Main
```

> **Nota:** En PowerShell de Windows, los comandos anteriores funcionan exactamente igual. Al ejecutar la Actividad 2, se cargará automáticamente el archivo `tareas.csv` si existe en la carpeta `actividad 2`.
