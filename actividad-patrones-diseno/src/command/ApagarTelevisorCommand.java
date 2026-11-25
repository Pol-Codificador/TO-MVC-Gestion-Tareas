package command;

/**
 * Comando concreto 2: apaga el televisor.
 */
public class ApagarTelevisorCommand implements Command {
    private final Televisor televisor;

    public ApagarTelevisorCommand(Televisor televisor) {
        this.televisor = televisor;
    }

    @Override
    public void execute() {
        televisor.apagar();
    }
}
