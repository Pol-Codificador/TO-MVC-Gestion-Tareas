package command;

/**
 * Comando concreto 3: sube el volumen del televisor.
 */
public class SubirVolumenCommand implements Command {
    private final Televisor televisor;

    public SubirVolumenCommand(Televisor televisor) {
        this.televisor = televisor;
    }

    @Override
    public void execute() {
        televisor.subirVolumen();
    }
}
