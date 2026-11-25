package command;

/**
 * Comando concreto 4: baja el volumen del televisor.
 */
public class BajarVolumenCommand implements Command {
    private final Televisor televisor;

    public BajarVolumenCommand(Televisor televisor) {
        this.televisor = televisor;
    }

    @Override
    public void execute() {
        televisor.bajarVolumen();
    }
}
