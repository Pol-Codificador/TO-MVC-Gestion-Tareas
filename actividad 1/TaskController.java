import java.util.ArrayList;
import java.util.List;

/**
 * Controlador (Controller) - Actividad 1: Patrón MVC
 * Actúa como intermediario entre el Modelo (Task) y la Vista (TaskView).
 * Recibe las solicitudes de operación, actualiza el modelo y ordena a la vista mostrar resultados.
 */
public class TaskController {
    private List<Task> tasks;
    private TaskView view;

    /**
     * Constructor que inicializa la vista y la lista interna de tareas.
     *
     * @param view Instancia de la vista encargada de mostrar salidas al usuario.
     */
    public TaskController(TaskView view) {
        this.view = view;
        this.tasks = new ArrayList<>();
    }

    /**
     * Crea y añade una nueva tarea a la lista, notificando el resultado a la vista.
     *
     * @param taskName Nombre de la nueva tarea.
     */
    public void addTask(String taskName) {
        if (taskName == null || taskName.trim().isEmpty()) {
            view.printMessage("Error: El nombre de la tarea no puede estar vacío.");
            return;
        }
        tasks.add(new Task(taskName.trim()));
        view.printMessage("Tarea añadida correctamente: \"" + taskName.trim() + "\"");
    }

    /**
     * Marca una tarea como completada según su índice en la lista.
     * Si el índice está fuera de rango, informa el error mediante la vista.
     *
     * @param index Índice basado en cero de la tarea a completar.
     */
    public void completeTask(int index) {
        if (index >= 0 && index < tasks.size()) {
            Task task = tasks.get(index);
            task.complete();
            view.printMessage("Tarea [" + index + "] marcada como completada: \"" + task.getName() + "\"");
        } else {
            view.printMessage("Error: Índice inválido (" + index + "). Debe estar entre 0 y " + (tasks.size() - 1) + ".");
        }
    }

    /**
     * Solicita a la vista mostrar el listado actual de tareas.
     */
    public void displayTasks() {
        view.printTasks(tasks);
    }
}
