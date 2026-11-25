package command;

/**
 * Comando concreto 1: enciende el televisor.
 */
public class EncenderTelevisorCommand implements Command {
    private final Televisor televisor;

    public EncenderTelevisorCommand(Televisor televisor) {
        this.televisor = televisor;
    }

    @Override
    public void execute() {
        televisor.encender();
    }
}
