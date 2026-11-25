package observer;

/**
 * Observador concreto: representa a un usuario suscrito al sistema de notificaciones.
 */
public class Usuario implements Observer {
    private final String nombre;

    public Usuario(String nombre) {
        this.nombre = nombre;
    }

    public String getNombre() {
        return nombre;
    }

    @Override
    public void actualizar(String mensaje) {
        System.out.println("  [Notificación para " + nombre + "] -> " + mensaje);
    }

    @Override
    public String toString() {
        return nombre;
    }
}
