import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

/**
 * Modelo (Model) - Actividad 2: Patrón MVC Avanzado
 * Representa una tarea enriquecida con identificador único, nombre, descripción,
 * prioridad, estado de completado y fecha/hora de creación.
 */
public class Task {
    public static final DateTimeFormatter DATE_FORMATTER = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");

    private int id;
    private String name;
    private String description;
    private Priority priority;
    private boolean completed;
    private LocalDateTime createdAt;

    /**
     * Constructor para crear una nueva tarea desde el sistema.
     *
     * @param id          Identificador único de la tarea.
     * @param name        Nombre o título de la tarea.
     * @param description Descripción detallada de la tarea.
     * @param priority    Nivel de prioridad (ALTA, MEDIA, BAJA).
     */
    public Task(int id, String name, String description, Priority priority) {
        this(id, name, description, priority, false, LocalDateTime.now());
    }

    /**
     * Constructor completo utilizado principalmente al reconstruir tareas desde el archivo de persistencia.
     *
     * @param id          Identificador único.
     * @param name        Nombre de la tarea.
     * @param description Descripción de la tarea.
     * @param priority    Prioridad de la tarea.
     * @param completed   Estado de completado.
     * @param createdAt   Fecha y hora de creación.
     */
    public Task(int id, String name, String description, Priority priority, boolean completed, LocalDateTime createdAt) {
        this.id = id;
        this.name = name;
        this.description = (description == null || description.trim().isEmpty()) ? "Sin descripción" : description.trim();
        this.priority = (priority == null) ? Priority.MEDIA : priority;
        this.completed = completed;
        this.createdAt = (createdAt == null) ? LocalDateTime.now() : createdAt;
    }

    public int getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        if (name != null && !name.trim().isEmpty()) {
            this.name = name.trim();
        }
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        if (description != null && !description.trim().isEmpty()) {
            this.description = description.trim();
        }
    }

    public Priority getPriority() {
        return priority;
    }

    public void setPriority(Priority priority) {
        if (priority != null) {
            this.priority = priority;
        }
    }

    public boolean isCompleted() {
        return completed;
    }

    public void complete() {
        this.completed = true;
    }

    /**
     * Alterna el estado de la tarea entre Completada y Pendiente.
     */
    public void toggleCompleted() {
        this.completed = !this.completed;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    /**
     * Devuelve la fecha de creación formateada como texto legible.
     *
     * @return Fecha en formato yyyy-MM-dd HH:mm:ss.
     */
    public String getFormattedCreatedAt() {
        return createdAt.format(DATE_FORMATTER);
    }
}
