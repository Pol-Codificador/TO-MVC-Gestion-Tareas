package strategy;

import java.util.Locale;

/**
 * Estrategia concreta: aplica un descuento porcentual al subtotal.
 */
public class DescuentoPorcentaje implements EstrategiaPromocion {
    private final double porcentaje;

    public DescuentoPorcentaje(double porcentaje) {
        if (porcentaje < 0 || porcentaje > 100) {
            throw new IllegalArgumentException("El porcentaje debe estar entre 0 y 100.");
        }
        this.porcentaje = porcentaje;
    }

    @Override
    public double aplicarPromocion(double precioUnitario, int cantidad) {
        double subtotal = precioUnitario * cantidad;
        return subtotal * (1.0 - porcentaje / 100.0);
    }

    @Override
    public String getDescripcion() {
        return String.format(Locale.US, "Descuento porcentual (%.0f%%)", porcentaje);
    }
}
