import java.util.List;

/**
 * Vista (View) - Actividad 1: Patrón MVC
 * Se encarga exclusivamente de la presentación de la información al usuario en consola.
 * No contiene lógica de negocio ni modifica directamente los datos del modelo.
 */
public class TaskView {

    /**
     * Muestra en consola todas las tareas con su índice, nombre y estado.
     *
     * @param tasks Lista de tareas a mostrar.
     */
    public void printTasks(List<Task> tasks) {
        System.out.println("\n================ LISTA DE TAREAS ================");
        if (tasks == null || tasks.isEmpty()) {
            System.out.println("No hay tareas registradas actualmente.");
        } else {
            for (int i = 0; i < tasks.size(); i++) {
                Task task = tasks.get(i);
                String status = task.isCompleted() ? "Completada" : "Pendiente";
                System.out.printf("[%d] %s - Estado: %s%n", i, task.getName(), status);
            }
        }
        System.out.println("=================================================\n");
    }

    /**
     * Imprime un mensaje informativo o de error en la consola.
     *
     * @param message Texto del mensaje a mostrar.
     */
    public void printMessage(String message) {
        System.out.println(">> " + message);
    }
}
