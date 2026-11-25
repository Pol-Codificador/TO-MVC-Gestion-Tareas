package strategy;

/**
 * Estrategia concreta: no aplica ningún descuento sobre el precio regular.
 */
public class SinDescuento implements EstrategiaPromocion {
    @Override
    public double aplicarPromocion(double precioUnitario, int cantidad) {
        return precioUnitario * cantidad;
    }

    @Override
    public String getDescripcion() {
        return "Sin descuento (precio regular)";
    }
}
