import java.util.List;
import java.util.Scanner;

/**
 * Vista (View) - Actividad 2: Patrón MVC Avanzado
 * Encargada de toda la interacción visual con el usuario en consola:
 * menú principal, listado tabular, estadísticas, mensajes y captura segura de entradas.
 */
public class TaskView {
    private final Scanner scanner;

    public TaskView() {
        this.scanner = new Scanner(System.in);
    }

    /**
     * Muestra el encabezado principal del sistema.
     */
    public void printBanner() {
        System.out.println("=========================================================================");
        System.out.println("     SISTEMA AVANZADO DE GESTIÓN DE TAREAS (ACTIVIDAD 2 - PATRÓN MVC)    ");
        System.out.println("=========================================================================");
    }

    /**
     * Muestra el menú interactivo de opciones disponibles.
     */
    public void printMenu() {
        System.out.println("\n--------------------------- MENÚ PRINCIPAL ---------------------------");
        System.out.println("  1. Añadir nueva tarea");
        System.out.println("  2. Listar todas las tareas");
        System.out.println("  3. Actualizar una tarea (nombre, descripción, prioridad o estado)");
        System.out.println("  4. Marcar / alternar estado de tarea (Completada / Pendiente)");
        System.out.println("  5. Eliminar una tarea");
        System.out.println("  6. Filtrar tareas (por estado o prioridad)");
        System.out.println("  7. Buscar tareas por palabra clave");
        System.out.println("  8. Ver resumen y estadísticas");
        System.out.println("  9. Guardar tareas en archivo (CSV)");
        System.out.println(" 10. Cargar tareas desde archivo (CSV)");
        System.out.println(" 11. Limpiar lista en memoria (para probar recarga)");
        System.out.println("  0. Salir");
        System.out.println("----------------------------------------------------------------------");
    }

    /**
     * Imprime una lista de tareas con formato tabular claro y alineado.
     *
     * @param title Título de la sección (ej. "LISTA COMPLETA", "RESULTADOS DE BÚSQUEDA").
     * @param tasks Lista de tareas a mostrar.
     */
    public void printTasks(String title, List<Task> tasks) {
        System.out.println("\n=== " + title + " ===");
        if (tasks == null || tasks.isEmpty()) {
            System.out.println("No se encontraron tareas para mostrar.");
            return;
        }

        System.out.printf("%-4s | %-4s | %-26s | %-9s | %-11s | %-19s%n",
                "IDX", "ID", "NOMBRE", "PRIORIDAD", "ESTADO", "CREADA EL");
        System.out.println("-----+------+----------------------------+-----------+-------------+--------------------");

        for (int i = 0; i < tasks.size(); i++) {
            Task t = tasks.get(i);
            String status = t.isCompleted() ? "Completada" : "Pendiente";
            System.out.printf("%-4d | %-4d | %-26s | %-9s | %-11s | %-19s%n",
                    i,
                    t.getId(),
                    truncate(t.getName(), 26),
                    t.getPriority().getLabel(),
                    status,
                    t.getFormattedCreatedAt());
            System.out.printf("     |      | Desc: %s%n", t.getDescription());
        }
        System.out.println("---------------------------------------------------------------------------------------");
    }

    /**
     * Muestra el panel de estadísticas y una barra visual de progreso.
     */
    public void printStatistics(int total, int completed, int pending,
                                int highCount, int mediumCount, int lowCount) {
        double percentage = (total == 0) ? 0.0 : (completed * 100.0 / total);
        int filledBars = (int) Math.round(percentage / 5.0); // 20 bloques = 100%
        StringBuilder bar = new StringBuilder("[");
        for (int i = 0; i < 20; i++) {
            bar.append(i < filledBars ? "#" : "-");
        }
        bar.append("]");

        System.out.println("\n================== RESUMEN Y ESTADÍSTICAS ==================");
        System.out.printf("  Total de tareas     : %d%n", total);
        System.out.printf("  Completadas         : %d%n", completed);
        System.out.printf("  Pendientes          : %d%n", pending);
        System.out.printf("  Avance general      : %s %.1f%%%n", bar.toString(), percentage);
        System.out.println("  ----------------------------------------------------------");
        System.out.printf("  Por prioridad       : Alta=%d | Media=%d | Baja=%d%n",
                highCount, mediumCount, lowCount);
        System.out.println("============================================================");
    }

    /**
     * Imprime un mensaje informativo al usuario.
     */
    public void printMessage(String message) {
        System.out.println(">> " + message);
    }

    /**
     * Imprime un mensaje de error formateado.
     */
    public void printError(String error) {
        System.out.println("[ERROR] " + error);
    }

    /**
     * Lee una línea de texto desde la entrada estándar de manera segura.
     *
     * @param prompt Mensaje de solicitud mostrado al usuario.
     * @return Cadena leída, o cadena vacía si ya no hay más entradas disponibles.
     */
    public String readLine(String prompt) {
        System.out.print(prompt);
        if (!scanner.hasNextLine()) {
            return "";
        }
        return scanner.nextLine().trim();
    }

    /**
     * Lee un número entero validando que la entrada no provoque InputMismatchException.
     *
     * @param prompt Mensaje de solicitud.
     * @return El número entero válido, o -1 si la entrada es inválida o finalizó el flujo.
     */
    public int readInt(String prompt) {
        System.out.print(prompt);
        if (!scanner.hasNextLine()) {
            return -1;
        }
        String input = scanner.nextLine().trim();
        try {
            return Integer.parseInt(input);
        } catch (NumberFormatException e) {
            printError("Entrada inválida (\"" + input + "\"). Debe ingresar un número entero.");
            return -1;
        }
    }

    /**
     * Indica si aún hay líneas disponibles en el flujo de entrada (útil para ejecución interactiva y automatizada).
     */
    public boolean hasInput() {
        return scanner.hasNextLine();
    }

    /**
     * Recorta textos largos para mantener la alineación de la tabla en consola.
     */
    private String truncate(String text, int maxLen) {
        if (text == null) {
            return "";
        }
        if (text.length() <= maxLen) {
            return text;
        }
        return text.substring(0, maxLen - 3) + "...";
    }
}
