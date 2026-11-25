package command;

/**
 * Invocador: ejecuta el comando asignado al presionar el botón, sin conocer
 * los detalles internos del televisor.
 */
public class ControlRemoto {
    private Command comando;

    public void setCommand(Command comando) {
        this.comando = comando;
    }

    public void presionarBoton() {
        if (comando == null) {
            System.out.println("  [CONTROL] No hay ningún comando asignado al botón.");
            return;
        }
        comando.execute();
    }
}
