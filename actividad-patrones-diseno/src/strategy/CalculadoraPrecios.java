package strategy;

/**
 * Contexto: delega el cálculo del precio final a la estrategia de promoción
 * configurada y permite cambiarla dinámicamente en tiempo de ejecución.
 */
public class CalculadoraPrecios {
    private EstrategiaPromocion estrategia;

    public CalculadoraPrecios(EstrategiaPromocion estrategia) {
        if (estrategia == null) {
            throw new IllegalArgumentException("La estrategia inicial no puede ser nula.");
        }
        this.estrategia = estrategia;
    }

    public void setEstrategia(EstrategiaPromocion estrategia) {
        if (estrategia == null) {
            throw new IllegalArgumentException("La estrategia no puede ser nula.");
        }
        this.estrategia = estrategia;
    }

    public double calcularTotal(double precioUnitario, int cantidad) {
        return estrategia.aplicarPromocion(precioUnitario, cantidad);
    }

    public String getDescripcionEstrategia() {
        return estrategia.getDescripcion();
    }
}
