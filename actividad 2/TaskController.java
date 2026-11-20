import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

/**
 * Controlador (Controller) - Actividad 2: Patrón MVC Avanzado
 * Coordina la interacción entre la Vista (TaskView), el Modelo (Task) y
 * la Capa de Persistencia (TaskRepository). Gestiona todas las operaciones CRUD,
 * filtrado, búsqueda, estadísticas y persistencia en archivo.
 */
public class TaskController {
    private List<Task> tasks;
    private final TaskView view;
    private final TaskRepository repository;
    private int nextId;

    /**
     * Constructor del controlador.
     *
     * @param view       Vista de consola.
     * @param repository Repositorio de persistencia en archivo.
     */
    public TaskController(TaskView view, TaskRepository repository) {
        this.view = view;
        this.repository = repository;
        this.tasks = new ArrayList<>();
        this.nextId = 1;
    }

    /**
     * Inicia el ciclo principal de la aplicación: carga tareas previas si existen
     * y ejecuta el menú interactivo hasta que el usuario elija salir.
     */
    public void run() {
        view.printBanner();
        loadTasksFromFile(true);

        boolean running = true;
        while (running) {
            view.printMenu();
            if (!view.hasInput()) {
                view.printMessage("Fin del flujo de entrada. Cerrando aplicación...");
                break;
            }
            int option = view.readInt("Seleccione una opción: ");
            switch (option) {
                case 1:
                    handleAddTask();
                    break;
                case 2:
                    displayTasks();
                    break;
                case 3:
                    handleUpdateTask();
                    break;
                case 4:
                    handleToggleComplete();
                    break;
                case 5:
                    handleDeleteTask();
                    break;
                case 6:
                    handleFilterTasks();
                    break;
                case 7:
                    handleSearchTasks();
                    break;
                case 8:
                    displayStatistics();
                    break;
                case 9:
                    saveTasksToFile();
                    break;
                case 10:
                    loadTasksFromFile(false);
                    break;
                case 11:
                    clearMemoryTasks();
                    break;
                case 0:
                    view.printMessage("Gracias por usar el Gestor de Tareas MVC. ¡Hasta pronto!");
                    running = false;
                    break;
                default:
                    view.printError("Opción no reconocida. Seleccione un número del 0 al 11.");
                    break;
            }
        }
    }

    // ==================== OPERACIONES CRUD ====================

    private void handleAddTask() {
        String name = view.readLine("Nombre de la tarea: ");
        if (name.isEmpty()) {
            view.printError("El nombre de la tarea no puede estar vacío.");
            return;
        }
        String description = view.readLine("Descripción (opcional): ");
        String prioInput = view.readLine("Prioridad [1=Alta, 2=Media, 3=Baja] (por defecto Media): ");
        Priority priority = Priority.fromInput(prioInput);

        addTask(name, description, priority);
    }

    public void addTask(String name, String description, Priority priority) {
        Task task = new Task(nextId++, name, description, priority);
        tasks.add(task);
        view.printMessage("Tarea añadida correctamente (ID=" + task.getId() + ", Prioridad=" + task.getPriority().getLabel() + ").");
    }

    public void displayTasks() {
        view.printTasks("LISTA COMPLETA DE TAREAS", tasks);
    }

    private void handleUpdateTask() {
        if (tasks.isEmpty()) {
            view.printMessage("No hay tareas registradas para actualizar.");
            return;
        }
        displayTasks();
        int index = view.readInt("Ingrese el índice (IDX) de la tarea a actualizar: ");
        if (!isValidIndex(index)) {
            view.printError("Índice fuera de rango (" + index + ").");
            return;
        }

        Task task = tasks.get(index);
        view.printMessage("Editando tarea [" + index + "] \"" + task.getName() + "\". Deje vacío para mantener el valor actual.");

        String newName = view.readLine("Nuevo nombre [" + task.getName() + "]: ");
        String newDesc = view.readLine("Nueva descripción [" + task.getDescription() + "]: ");
        String newPrio = view.readLine("Nueva prioridad [1=Alta, 2=Media, 3=Baja] [" + task.getPriority().getLabel() + "]: ");
        String toggleState = view.readLine("¿Alternar estado actual (" + (task.isCompleted() ? "Completada" : "Pendiente") + ")? [s/n]: ");

        updateTask(index, newName, newDesc, newPrio, toggleState.equalsIgnoreCase("s"));
    }

    public void updateTask(int index, String newName, String newDesc, String newPrioInput, boolean toggleState) {
        if (!isValidIndex(index)) {
            view.printError("Índice inválido (" + index + ").");
            return;
        }
        Task task = tasks.get(index);
        if (newName != null && !newName.isEmpty()) {
            task.setName(newName);
        }
        if (newDesc != null && !newDesc.isEmpty()) {
            task.setDescription(newDesc);
        }
        if (newPrioInput != null && !newPrioInput.isEmpty()) {
            task.setPriority(Priority.fromInput(newPrioInput));
        }
        if (toggleState) {
            task.toggleCompleted();
        }
        view.printMessage("Tarea [" + index + "] actualizada correctamente.");
    }

    private void handleToggleComplete() {
        if (tasks.isEmpty()) {
            view.printMessage("No hay tareas disponibles.");
            return;
        }
        displayTasks();
        int index = view.readInt("Ingrese el índice (IDX) de la tarea para cambiar su estado: ");
        toggleTaskStatus(index);
    }

    public void toggleTaskStatus(int index) {
        if (!isValidIndex(index)) {
            view.printError("Índice inválido (" + index + "). Debe estar entre 0 y " + (tasks.size() - 1) + ".");
            return;
        }
        Task task = tasks.get(index);
        task.toggleCompleted();
        String newState = task.isCompleted() ? "Completada" : "Pendiente";
        view.printMessage("Tarea [" + index + "] \"" + task.getName() + "\" ahora está: " + newState + ".");
    }

    private void handleDeleteTask() {
        if (tasks.isEmpty()) {
            view.printMessage("No hay tareas para eliminar.");
            return;
        }
        displayTasks();
        int index = view.readInt("Ingrese el índice (IDX) de la tarea a eliminar: ");
        deleteTask(index);
    }

    public void deleteTask(int index) {
        if (!isValidIndex(index)) {
            view.printError("Índice inválido (" + index + "). No se eliminó ninguna tarea.");
            return;
        }
        Task removed = tasks.remove(index);
        view.printMessage("Tarea eliminada correctamente: [ID=" + removed.getId() + "] \"" + removed.getName() + "\".");
    }

    // ==================== FILTROS, BÚSQUEDA Y ESTADÍSTICAS ====================

    private void handleFilterTasks() {
        System.out.println("\n--- FILTRAR TAREAS ---");
        System.out.println("  1. Solo Pendientes");
        System.out.println("  2. Solo Completadas");
        System.out.println("  3. Prioridad Alta");
        System.out.println("  4. Prioridad Media");
        System.out.println("  5. Prioridad Baja");
        int filterOption = view.readInt("Seleccione criterio de filtro: ");

        List<Task> filtered = new ArrayList<>();
        String title;

        switch (filterOption) {
            case 1:
                title = "TAREAS PENDIENTES";
                for (Task t : tasks) {
                    if (!t.isCompleted()) filtered.add(t);
                }
                break;
            case 2:
                title = "TAREAS COMPLETADAS";
                for (Task t : tasks) {
                    if (t.isCompleted()) filtered.add(t);
                }
                break;
            case 3:
                title = "TAREAS DE PRIORIDAD ALTA";
                for (Task t : tasks) {
                    if (t.getPriority() == Priority.ALTA) filtered.add(t);
                }
                break;
            case 4:
                title = "TAREAS DE PRIORIDAD MEDIA";
                for (Task t : tasks) {
                    if (t.getPriority() == Priority.MEDIA) filtered.add(t);
                }
                break;
            case 5:
                title = "TAREAS DE PRIORIDAD BAJA";
                for (Task t : tasks) {
                    if (t.getPriority() == Priority.BAJA) filtered.add(t);
                }
                break;
            default:
                view.printError("Criterio de filtro no válido.");
                return;
        }
        view.printTasks(title, filtered);
    }

    private void handleSearchTasks() {
        String keyword = view.readLine("Ingrese palabra clave para buscar (en nombre o descripción): ");
        if (keyword.isEmpty()) {
            view.printError("Debe ingresar una palabra clave.");
            return;
        }
        String lowerKey = keyword.toLowerCase();
        List<Task> results = new ArrayList<>();
        for (Task t : tasks) {
            if (t.getName().toLowerCase().contains(lowerKey) ||
                t.getDescription().toLowerCase().contains(lowerKey)) {
                results.add(t);
            }
        }
        view.printTasks("RESULTADOS DE BÚSQUEDA: \"" + keyword + "\"", results);
    }

    public void displayStatistics() {
        int total = tasks.size();
        int completed = 0;
        int high = 0;
        int medium = 0;
        int low = 0;

        for (Task t : tasks) {
            if (t.isCompleted()) {
                completed++;
            }
            switch (t.getPriority()) {
                case ALTA:
                    high++;
                    break;
                case MEDIA:
                    medium++;
                    break;
                case BAJA:
                    low++;
                    break;
            }
        }
        int pending = total - completed;
        view.printStatistics(total, completed, pending, high, medium, low);
    }

    // ==================== PERSISTENCIA EN ARCHIVO ====================

    public void saveTasksToFile() {
        try {
            repository.saveTasks(tasks);
            view.printMessage("Se guardaron " + tasks.size() + " tarea(s) exitosamente en \"" + repository.getFilePath() + "\".");
        } catch (IOException e) {
            view.printError("No se pudo guardar el archivo de tareas: " + e.getMessage());
        }
    }

    public void loadTasksFromFile(boolean silentIfMissing) {
        if (!repository.storageFileExists()) {
            if (!silentIfMissing) {
                view.printMessage("El archivo \"" + repository.getFilePath() + "\" aún no existe. No se cargaron tareas.");
            } else {
                view.printMessage("Iniciando sin archivo previo (\"" + repository.getFilePath() + "\" se creará al guardar).");
            }
            return;
        }

        try {
            List<Task> loaded = repository.loadTasks();
            this.tasks = loaded;
            recalculateNextId();
            view.printMessage("Se cargaron " + tasks.size() + " tarea(s) desde \"" + repository.getFilePath() + "\".");
        } catch (IOException e) {
            view.printError("Error al leer el archivo de tareas: " + e.getMessage());
        }
    }

    public void clearMemoryTasks() {
        tasks.clear();
        nextId = 1;
        view.printMessage("Lista de tareas en memoria limpiada (0 tareas en RAM; el archivo en disco no fue modificado).");
    }

    // ==================== UTILIDADES PRIVADAS ====================

    private boolean isValidIndex(int index) {
        return index >= 0 && index < tasks.size();
    }

    private void recalculateNextId() {
        int maxId = 0;
        for (Task t : tasks) {
            if (t.getId() > maxId) {
                maxId = t.getId();
            }
        }
        this.nextId = maxId + 1;
    }
}
