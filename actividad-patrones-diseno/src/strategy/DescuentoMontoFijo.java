package strategy;

import java.util.Locale;

/**
 * Estrategia concreta: resta un monto fijo al subtotal, sin bajar de cero.
 */
public class DescuentoMontoFijo implements EstrategiaPromocion {
    private final double montoDescuento;

    public DescuentoMontoFijo(double montoDescuento) {
        if (montoDescuento < 0) {
            throw new IllegalArgumentException("El monto de descuento no puede ser negativo.");
        }
        this.montoDescuento = montoDescuento;
    }

    @Override
    public double aplicarPromocion(double precioUnitario, int cantidad) {
        double subtotal = precioUnitario * cantidad;
        return Math.max(0.0, subtotal - montoDescuento);
    }

    @Override
    public String getDescripcion() {
        return String.format(Locale.US, "Descuento de monto fijo (S/ %.2f)", montoDescuento);
    }
}
