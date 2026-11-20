/**
 * Aplicación Principal (Main) - Actividad 2: Patrón MVC Avanzado
 * Ensambla la Vista, la Capa de Persistencia (TaskRepository) y el Controlador,
 * e inicia el menú interactivo en consola.
 */
public class Main {
    private static final String DEFAULT_STORAGE_FILE = "tareas.csv";

    public static void main(String[] args) {
        TaskView view = new TaskView();
        TaskRepository repository = new TaskRepository(DEFAULT_STORAGE_FILE);
        TaskController controller = new TaskController(view, repository);

        controller.run();
    }
}
