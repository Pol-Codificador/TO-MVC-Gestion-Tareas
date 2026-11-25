package command;

/**
 * Receptor: contiene la lógica real de las cinco funcionalidades del televisor.
 */
public class Televisor {
    private boolean encendido = false;
    private int volumen = 15;
    private int canal = 1;

    public void encender() {
        encendido = true;
        System.out.println("  [TV] Televisor encendido (Canal " + canal + ", Volumen " + volumen + ").");
    }

    public void apagar() {
        encendido = false;
        System.out.println("  [TV] Televisor apagado.");
    }

    public void subirVolumen() {
        if (!encendido) {
            System.out.println("  [TV] No se puede subir el volumen: el televisor está apagado.");
            return;
        }
        if (volumen < 100) {
            volumen = Math.min(100, volumen + 5);
        }
        System.out.println("  [TV] Volumen aumentado a " + volumen + ".");
    }

    public void bajarVolumen() {
        if (!encendido) {
            System.out.println("  [TV] No se puede bajar el volumen: el televisor está apagado.");
            return;
        }
        if (volumen > 0) {
            volumen = Math.max(0, volumen - 5);
        }
        System.out.println("  [TV] Volumen disminuido a " + volumen + ".");
    }

    public void cambiarCanal(int nuevoCanal) {
        if (!encendido) {
            System.out.println("  [TV] No se puede cambiar de canal: el televisor está apagado.");
            return;
        }
        if (nuevoCanal <= 0) {
            System.out.println("  [TV] Canal inválido: " + nuevoCanal + ".");
            return;
        }
        canal = nuevoCanal;
        System.out.println("  [TV] Canal cambiado al " + canal + ".");
    }
}
