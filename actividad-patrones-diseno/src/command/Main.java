package command;

/**
 * Cliente de demostración para el patrón Command: configura y ejecuta las
 * cinco funcionalidades del control remoto del televisor.
 */
public class Main {
    public static void main(String[] args) {
        System.out.println("=== PATRÓN COMMAND: CONTROL REMOTO DE TELEVISOR ===");

        Televisor tv = new Televisor();
        ControlRemoto control = new ControlRemoto();

        Command encender = new EncenderTelevisorCommand(tv);
        Command subirVolumen = new SubirVolumenCommand(tv);
        Command cambiarCanal7 = new CambiarCanalCommand(tv, 7);
        Command bajarVolumen = new BajarVolumenCommand(tv);
        Command apagar = new ApagarTelevisorCommand(tv);

        System.out.println("\n1. Acción: Encender televisor");
        control.setCommand(encender);
        control.presionarBoton();

        System.out.println("\n2. Acción: Subir volumen");
        control.setCommand(subirVolumen);
        control.presionarBoton();

        System.out.println("\n3. Acción: Cambiar al canal 7");
        control.setCommand(cambiarCanal7);
        control.presionarBoton();

        System.out.println("\n4. Acción: Bajar volumen");
        control.setCommand(bajarVolumen);
        control.presionarBoton();

        System.out.println("\n5. Acción: Apagar televisor");
        control.setCommand(apagar);
        control.presionarBoton();
    }
}
