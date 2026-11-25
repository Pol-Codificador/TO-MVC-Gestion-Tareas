package strategy;

/**
 * Estrategia concreta: promoción 2x1 (por cada 2 unidades se cobra solo 1).
 */
public class PromocionDosPorUno implements EstrategiaPromocion {
    @Override
    public double aplicarPromocion(double precioUnitario, int cantidad) {
        int unidadesAPagar = (cantidad / 2) + (cantidad % 2);
        return unidadesAPagar * precioUnitario;
    }

    @Override
    public String getDescripcion() {
        return "Promoción 2x1 (paga 1 de cada 2 unidades)";
    }
}
