/**
 * Aplicación Principal (Main) - Actividad 1: Patrón MVC
 * Punto de entrada del programa que ensambla la Vista y el Controlador
 * y demuestra el flujo de operaciones CRUD básicas bajo el patrón MVC.
 */
public class Main {
    public static void main(String[] args) {
        System.out.println("=== GESTOR DE TAREAS (ACTIVIDAD 1 - PATRÓN MVC) ===\n");

        // 1. Instanciar la Vista y el Controlador
        TaskView view = new TaskView();
        TaskController controller = new TaskController(view);

        // 2. Añadir tareas mediante el Controlador
        controller.addTask("Estudiar el patrón arquitectónico MVC");
        controller.addTask("Implementar el laboratorio de Tecnología de Objetos");
        controller.addTask("Preparar la exposición y el informe técnico");

        // 3. Mostrar la lista inicial de tareas
        controller.displayTasks();

        // 4. Completar una tarea válida usando su índice
        controller.completeTask(1);

        // 5. Probar un índice inválido para demostrar la validación del Controlador
        controller.completeTask(10);

        // 6. Mostrar nuevamente la lista actualizada de tareas
        controller.displayTasks();
    }
}
