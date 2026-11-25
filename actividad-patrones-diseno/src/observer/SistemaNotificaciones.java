package observer;

import java.util.ArrayList;
import java.util.List;

/**
 * Sujeto (Observable): administra la lista de observadores y les notifica
 * automáticamente cada vez que ocurre un nuevo evento o mensaje.
 */
public class SistemaNotificaciones {
    private final List<Observer> observadores = new ArrayList<>();

    public void registrar(Observer observador) {
        if (observador == null || observadores.contains(observador)) {
            return;
        }
        observadores.add(observador);
        System.out.println("+ Suscrito: " + observador);
    }

    public void eliminar(Observer observador) {
        if (observadores.remove(observador)) {
            System.out.println("- Desuscrito: " + observador);
        }
    }

    public void notificar(String mensaje) {
        System.out.println("\n[SISTEMA] Emitiendo notificación: \"" + mensaje + "\"");
        for (Observer observador : observadores) {
            observador.actualizar(mensaje);
        }
    }
}
