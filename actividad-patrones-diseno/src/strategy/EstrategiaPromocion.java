package strategy;

/**
 * Interfaz Strategy: define el algoritmo intercambiable para calcular el total
 * de una compra aplicando una promoción específica.
 */
public interface EstrategiaPromocion {
    double aplicarPromocion(double precioUnitario, int cantidad);

    String getDescripcion();
}
