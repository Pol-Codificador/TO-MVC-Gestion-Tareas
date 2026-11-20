/**
 * Modelo (Model) - Actividad 1: Patrón MVC
 * Representa una tarea individual dentro del sistema de gestión de tareas.
 * Encapsula los datos (nombre y estado de completado) y las reglas básicas de su estado.
 */
public class Task {
    private String name;
    private boolean completed;

    /**
     * Constructor que inicializa una tarea con su nombre y estado inicial pendiente (false).
     *
     * @param name Nombre descriptivo de la tarea.
     */
    public Task(String name) {
        this.name = name;
        this.completed = false;
    }

    /**
     * Devuelve el nombre de la tarea.
     *
     * @return Nombre de la tarea.
     */
    public String getName() {
        return name;
    }

    /**
     * Indica si la tarea ha sido completada.
     *
     * @return true si está completada, false si está pendiente.
     */
    public boolean isCompleted() {
        return completed;
    }

    /**
     * Marca la tarea como completada.
     */
    public void complete() {
        this.completed = true;
    }
}
