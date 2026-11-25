package strategy;

import java.util.Locale;

/**
 * Cliente de demostración para el patrón Strategy.
 */
public class Main {
    private static void mostrarResumen(CalculadoraPrecios calculadora, String producto,
                                       double precioUnitario, int cantidad) {
        double subtotal = precioUnitario * cantidad;
        double totalFinal = calculadora.calcularTotal(precioUnitario, cantidad);
        double ahorro = subtotal - totalFinal;

        System.out.println("Estrategia : " + calculadora.getDescripcionEstrategia());
        System.out.printf(Locale.US, "Producto   : %s (%d x S/ %.2f = S/ %.2f)%n",
                producto, cantidad, precioUnitario, subtotal);
        System.out.printf(Locale.US, "Total final: S/ %.2f  (Ahorro: S/ %.2f)%n",
                totalFinal, ahorro);
        System.out.println("--------------------------------------------------");
    }

    public static void main(String[] args) {
        System.out.println("=== PATRÓN STRATEGY: PROMOCIONES DE PRODUCTOS ===");

        String producto = "Audífonos Bluetooth";
        double precioUnitario = 120.00;
        int cantidad = 4;

        CalculadoraPrecios calculadora = new CalculadoraPrecios(new SinDescuento());
        mostrarResumen(calculadora, producto, precioUnitario, cantidad);

        calculadora.setEstrategia(new DescuentoPorcentaje(20));
        mostrarResumen(calculadora, producto, precioUnitario, cantidad);

        calculadora.setEstrategia(new DescuentoMontoFijo(75.00));
        mostrarResumen(calculadora, producto, precioUnitario, cantidad);

        calculadora.setEstrategia(new PromocionDosPorUno());
        mostrarResumen(calculadora, producto, precioUnitario, cantidad);
    }
}
