package observer;

/**
 * Cliente de demostración para el patrón Observer.
 */
public class Main {
    public static void main(String[] args) {
        System.out.println("=== PATRÓN OBSERVER: SISTEMA DE NOTIFICACIONES ===");

        SistemaNotificaciones sistema = new SistemaNotificaciones();

        Usuario ana = new Usuario("Ana");
        Usuario carlos = new Usuario("Carlos");
        Usuario lucia = new Usuario("Lucía");

        sistema.registrar(ana);
        sistema.registrar(carlos);
        sistema.registrar(lucia);

        sistema.notificar("Nueva actualización v2.0 disponible.");

        System.out.println();
        sistema.eliminar(carlos);

        sistema.notificar("Mantenimiento programado hoy a las 22:00.");

        System.out.println();
        Usuario diego = new Usuario("Diego");
        sistema.registrar(diego);

        sistema.notificar("Promoción exclusiva de fin de semana activada.");
    }
}
