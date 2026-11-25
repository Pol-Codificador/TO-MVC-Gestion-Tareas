package observer;

/**
 * Interfaz Observer: define el contrato que deben implementar todos los
 * suscriptores para recibir notificaciones emitidas por el sujeto.
 */
public interface Observer {
    void actualizar(String mensaje);
}
