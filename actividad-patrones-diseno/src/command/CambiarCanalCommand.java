package command;

/**
 * Comando concreto 5: cambia el televisor a un canal específico.
 */
public class CambiarCanalCommand implements Command {
    private final Televisor televisor;
    private final int nuevoCanal;

    public CambiarCanalCommand(Televisor televisor, int nuevoCanal) {
        this.televisor = televisor;
        this.nuevoCanal = nuevoCanal;
    }

    @Override
    public void execute() {
        televisor.cambiarCanal(nuevoCanal);
    }
}
