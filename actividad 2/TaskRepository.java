import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.nio.charset.StandardCharsets;
import java.time.LocalDateTime;
import java.time.format.DateTimeParseException;
import java.util.ArrayList;
import java.util.List;

/**
 * Capa de Persistencia (Parte del Modelo) - Actividad 2: Patrón MVC Avanzado
 * Aplica el Principio de Responsabilidad Única (SRP) separando la lectura y escritura
 * en disco del Controlador. Utiliza formato CSV separado por punto y coma (;) en UTF-8.
 */
public class TaskRepository {
    private static final String DELIMITER = ";";
    private static final String HEADER = "id;name;description;priority;completed;createdAt";

    private final String filePath;

    /**
     * Constructor que define la ruta del archivo de persistencia.
     *
     * @param filePath Ruta del archivo CSV donde se almacenarán las tareas.
     */
    public TaskRepository(String filePath) {
        this.filePath = filePath;
    }

    public String getFilePath() {
        return filePath;
    }

    /**
     * Guarda la lista completa de tareas en el archivo CSV.
     *
     * @param tasks Lista de tareas a persistir.
     * @throws IOException Si ocurre un error de escritura en disco.
     */
    public void saveTasks(List<Task> tasks) throws IOException {
        try (BufferedWriter writer = new BufferedWriter(
                new OutputStreamWriter(new FileOutputStream(filePath), StandardCharsets.UTF_8))) {
            writer.write(HEADER);
            writer.newLine();
            for (Task task : tasks) {
                String line = String.join(DELIMITER,
                        String.valueOf(task.getId()),
                        sanitize(task.getName()),
                        sanitize(task.getDescription()),
                        task.getPriority().name(),
                        String.valueOf(task.isCompleted()),
                        task.getFormattedCreatedAt()
                );
                writer.write(line);
                writer.newLine();
            }
        }
    }

    /**
     * Carga las tareas almacenadas en el archivo CSV y reconstruye los objetos Task.
     * Si el archivo no existe o está vacío, devuelve una lista vacía sin lanzar errores críticos.
     *
     * @return Lista de tareas reconstruidas desde el archivo.
     * @throws IOException Si ocurre un error de lectura en disco.
     */
    public List<Task> loadTasks() throws IOException {
        List<Task> loadedTasks = new ArrayList<>();
        File file = new File(filePath);

        if (!file.exists() || file.length() == 0) {
            return loadedTasks;
        }

        try (BufferedReader reader = new BufferedReader(
                new InputStreamReader(new FileInputStream(file), StandardCharsets.UTF_8))) {
            String line;
            boolean isFirstLine = true;

            while ((line = reader.readLine()) != null) {
                if (isFirstLine) {
                    isFirstLine = false;
                    // Omitir cabecera si coincide
                    if (line.trim().equalsIgnoreCase(HEADER)) {
                        continue;
                    }
                }
                if (line.trim().isEmpty()) {
                    continue;
                }

                String[] parts = line.split(DELIMITER, -1);
                if (parts.length >= 6) {
                    try {
                        int id = Integer.parseInt(parts[0].trim());
                        String name = restore(parts[1]);
                        String description = restore(parts[2]);
                        Priority priority = Priority.fromInput(parts[3]);
                        boolean completed = Boolean.parseBoolean(parts[4].trim());
                        LocalDateTime createdAt = parseDateTime(parts[5].trim());

                        loadedTasks.add(new Task(id, name, description, priority, completed, createdAt));
                    } catch (NumberFormatException ignored) {
                        // Se omite una línea corrupta para no interrumpir la carga de las demás tareas
                    }
                }
            }
        }
        return loadedTasks;
    }

    /**
     * Verifica si el archivo de persistencia existe actualmente en el disco.
     *
     * @return true si el archivo existe.
     */
    public boolean storageFileExists() {
        return new File(filePath).exists();
    }

    /**
     * Limpia caracteres que podrían romper el formato CSV (saltos de línea y punto y coma).
     */
    private String sanitize(String text) {
        if (text == null) {
            return "";
        }
        return text.replace("\r", " ")
                   .replace("\n", " ")
                   .replace(DELIMITER, ",")
                   .trim();
    }

    /**
     * Restaura el texto leído desde el CSV.
     */
    private String restore(String text) {
        return text == null ? "" : text.trim();
    }

    /**
     * Parsea la fecha almacenada; si falla, asigna la fecha actual como respaldo seguro.
     */
    private LocalDateTime parseDateTime(String dateStr) {
        try {
            return LocalDateTime.parse(dateStr, Task.DATE_FORMATTER);
        } catch (DateTimeParseException e) {
            return LocalDateTime.now();
        }
    }
}
