/**
 * Enumeración Priority (Modelo) - Actividad 2: Patrón MVC Avanzado
 * Define los niveles de prioridad válidos para una tarea, garantizando
 * seguridad de tipos y evitando cadenas arbitrarias inválidas.
 */
public enum Priority {
    ALTA("Alta"),
    MEDIA("Media"),
    BAJA("Baja");
    private final String label;

    Priority(String label) {
        this.label = label;
    }

    /**
     * Devuelve la etiqueta legible de la prioridad.
     *
     * @return Nombre formateado de la prioridad.
     */
    public String getLabel() {
        return label;
    }

    /**
     * Convierte una cadena de texto o número ("1", "2", "3", "ALTA", etc.) en una constante Priority.
     *
     * @param value Valor ingresado por el usuario o leído desde archivo.
     * @return La prioridad correspondiente, o MEDIA por defecto si no coincide.
     */
    public static Priority fromInput(String value) {
        if (value == null) {
            return MEDIA;
        }
        String normalized = value.trim().toUpperCase();
        switch (normalized) {
            case "1":
            case "ALTA":
                return ALTA;
            case "2":
            case "MEDIA":
                return MEDIA;
            case "3":
            case "BAJA":
                return BAJA;
            default:
                return MEDIA;
        }
    }
}
