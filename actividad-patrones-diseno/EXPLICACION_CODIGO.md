# Patrones de Diseño Comportamentales en Java: Observer, Strategy y Command

## 1. Introducción a los Patrones de Diseño Comportamentales

Los **patrones de diseño comportamentales** se enfocan en cómo interactúan y se reparten responsabilidades los objetos en tiempo de ejecución. Su propósito principal es reducir el acoplamiento rígido entre clases, permitiendo que la comunicación, las reglas de negocio y las solicitudes entre objetos puedan evolucionar sin reescribir la arquitectura completa.

En esta actividad se implementan tres patrones comportamentales fundamentales en **Java (OpenJDK 21)** dentro de la carpeta exclusiva `actividad-patrones-diseno/`:

```text
actividad-patrones-diseno/
├── src/
│   ├── observer/
│   │   ├── Observer.java
│   │   ├── Usuario.java
│   │   ├── SistemaNotificaciones.java
│   │   └── Main.java
│   ├── strategy/
│   │   ├── EstrategiaPromocion.java
│   │   ├── SinDescuento.java
│   │   ├── DescuentoPorcentaje.java
│   │   ├── DescuentoMontoFijo.java
│   │   ├── PromocionDosPorUno.java
│   │   ├── CalculadoraPrecios.java
│   │   └── Main.java
│   └── command/
│       ├── Command.java
│       ├── Televisor.java
│       ├── EncenderTelevisorCommand.java
│       ├── ApagarTelevisorCommand.java
│       ├── SubirVolumenCommand.java
│       ├── BajarVolumenCommand.java
│       ├── CambiarCanalCommand.java
│       ├── ControlRemoto.java
│       └── Main.java
├── EXPLICACION_CODIGO.md
├── Informe_Patrones_Diseno.docx
├── Presentacion_Patrones_Diseno.pptx
└── scripts/
```

---

## 2. Ejercicio 1: Patrón Observer — Sistema de Notificaciones

### 2.1 ¿En qué consiste y qué problema resuelve?
El patrón **Observer** define una relación de dependencia **uno a muchos** entre un objeto llamado **Sujeto (Observable)** y múltiples objetos llamados **Observadores**. Cuando el Sujeto cambia de estado o emite un evento, notifica de forma automática a todos los observadores suscritos.

- **Problema que resuelve:** Evita que el sistema emisor de eventos quede fuertemente acoplado a clases concretas de usuarios o canales de recepción, y elimina la necesidad de que los usuarios consulten constantemente (*polling*) si hay novedades.
- **Roles del patrón en este ejercicio:**
  - **Interfaz Observer:** `Observer` (`Observer.java`).
  - **Observador Concreto:** `Usuario` (`Usuario.java`).
  - **Sujeto / Observable:** `SistemaNotificaciones` (`SistemaNotificaciones.java`).
  - **Cliente:** `Main` (`Main.java`).

### 2.2 Explicación archivo por archivo y bloque por bloque

#### `src/observer/Observer.java`
- **Declaración de paquete (`package observer;`)**: Agrupa las clases del ejercicio dentro del espacio de nombres `observer`.
- **Interfaz `Observer`**: Establece el contrato mínimo que debe cumplir cualquier suscriptor.
- **Método `void actualizar(String mensaje)`**: Es el punto de entrada que invoca el sujeto cuando ocurre una notificación. Recibe el contenido del aviso como `String`.

#### `src/observer/Usuario.java`
- **Implementación (`public class Usuario implements Observer`)**: Convierte a `Usuario` en un observador concreto compatible con `SistemaNotificaciones`.
- **Atributo `private final String nombre`**: Almacena de manera inmutable el nombre del usuario para identificar quién recibe la notificación.
- **Constructor `public Usuario(String nombre)`**: Inicializa el nombre del usuario al instanciarlo.
- **Método `public String getNombre()`**: Expone el nombre del usuario de forma segura (encapsulamiento).
- **Método `@Override public void actualizar(String mensaje)`**: Implementa la reacción del usuario ante un evento del sistema, imprimiendo `[Notificación para <nombre>] -> <mensaje>`.
- **Método `@Override public String toString()`**: Devuelve `nombre` para que los mensajes de suscripción y desuscripción en consola muestren directamente el nombre legible del usuario.

#### `src/observer/SistemaNotificaciones.java`
- **Atributo `private final List<Observer> observadores = new ArrayList<>();`**: Mantiene la lista dinámica de observadores actualmente suscritos, programando contra la interfaz `Observer` y no contra la clase concreta `Usuario`.
- **Método `public void registrar(Observer observador)`**:
  - Valida que `observador` no sea `null` y que no esté ya registrado (`!observadores.contains(observador)`), evitando duplicados.
  - Agrega el observador a la lista e imprime `+ Suscrito: <observador>`.
- **Método `public void eliminar(Observer observador)`**:
  - Remueve al observador mediante `observadores.remove(observador)`.
  - Si existía en la lista, imprime `- Desuscrito: <observador>`. A partir de ese instante deja de recibir notificaciones.
- **Método `public void notificar(String mensaje)`**:
  - Imprime el encabezado `[SISTEMA] Emitiendo notificación: "<mensaje>"`.
  - Recorre la lista `observadores` con un ciclo `for-each` e invoca `observador.actualizar(mensaje)` en cada suscriptor activo.

#### `src/observer/Main.java`
- **Bloque de configuración inicial**: Crea una instancia de `SistemaNotificaciones` y tres objetos `Usuario` (`Ana`, `Carlos`, `Lucía`), registrándolos con `sistema.registrar(...)`.
- **Primera emisión**: Llama a `sistema.notificar("Nueva actualización v2.0 disponible.")`. Los tres usuarios suscritos reciben el aviso.
- **Desuscripción y segunda emisión**: Ejecuta `sistema.eliminar(carlos)` y vuelve a notificar `"Mantenimiento programado hoy a las 22:00."`. Solo `Ana` y `Lucía` reciben la notificación, comprobando que `Carlos` dejó de estar suscrito.
- **Suscripción dinámica y tercera emisión**: Registra a un cuarto usuario (`Diego`) y emite `"Promoción exclusiva de fin de semana activada."`, demostrando que nuevos observadores se incorporan en tiempo de ejecución sin modificar `SistemaNotificaciones`.

### 2.3 Cumplimiento de requisitos (Observer)

| Requisito solicitado | Implementación en el código |
|---|---|
| Interfaz `Observer` | `Observer.java` con el método `actualizar(String mensaje)` |
| Sujeto con registrar, eliminar y notificar | `SistemaNotificaciones.java` con `registrar()`, `eliminar()` y `notificar()` |
| Múltiples observadores concretos | `Usuario.java` instanciado para `Ana`, `Carlos`, `Lucía` y `Diego` |
| Demostración de recepción y desuscripción | `Main.java` emite notificaciones antes y después de `eliminar(carlos)` |

### 2.4 Compilación y salida real obtenida (Observer)

```powershell
javac -Xlint:all -encoding UTF-8 -d .tmp_bin actividad-patrones-diseno/src/observer/*.java
java -Dfile.encoding=UTF-8 -Dstdout.encoding=UTF-8 -cp .tmp_bin observer.Main
```

```text
=== PATRÓN OBSERVER: SISTEMA DE NOTIFICACIONES ===
+ Suscrito: Ana
+ Suscrito: Carlos
+ Suscrito: Lucía

[SISTEMA] Emitiendo notificación: "Nueva actualización v2.0 disponible."
  [Notificación para Ana] -> Nueva actualización v2.0 disponible.
  [Notificación para Carlos] -> Nueva actualización v2.0 disponible.
  [Notificación para Lucía] -> Nueva actualización v2.0 disponible.

- Desuscrito: Carlos

[SISTEMA] Emitiendo notificación: "Mantenimiento programado hoy a las 22:00."
  [Notificación para Ana] -> Mantenimiento programado hoy a las 22:00.
  [Notificación para Lucía] -> Mantenimiento programado hoy a las 22:00.

+ Suscrito: Diego

[SISTEMA] Emitiendo notificación: "Promoción exclusiva de fin de semana activada."
  [Notificación para Ana] -> Promoción exclusiva de fin de semana activada.
  [Notificación para Lucía] -> Promoción exclusiva de fin de semana activada.
  [Notificación para Diego] -> Promoción exclusiva de fin de semana activada.
```

---

## 3. Ejercicio 2: Patrón Strategy — Promociones de Productos

### 3.1 ¿En qué consiste y qué problema resuelve?
El patrón **Strategy** permite definir una familia de algoritmos (en este caso, reglas de cálculo de promociones), encapsular cada uno en una clase independiente con una interfaz común y hacerlos intercambiables en tiempo de ejecución.

- **Problema que resuelve:** Evita llenar una clase calculadora con largos bloques `if / else if` o `switch` por cada tipo de descuento. Si mañana aparece una nueva promoción (por ejemplo, descuento por cliente VIP o 3x2), basta con añadir una nueva clase que implemente `EstrategiaPromocion` sin tocar el código de `CalculadoraPrecios` (principio Abierto/Cerrado).
- **Roles del patrón en este ejercicio:**
  - **Interfaz Strategy:** `EstrategiaPromocion` (`EstrategiaPromocion.java`).
  - **Estrategias Concretas:** `SinDescuento`, `DescuentoPorcentaje`, `DescuentoMontoFijo`, `PromocionDosPorUno`.
  - **Contexto:** `CalculadoraPrecios` (`CalculadoraPrecios.java`).
  - **Cliente:** `Main` (`Main.java`).

### 3.2 Explicación archivo por archivo y bloque por bloque

#### `src/strategy/EstrategiaPromocion.java`
- **Método `double aplicarPromocion(double precioUnitario, int cantidad)`**: Define la firma uniforme para calcular el monto final a pagar a partir del precio unitario y la cantidad de unidades.
- **Método `String getDescripcion()`**: Devuelve el nombre descriptivo de la promoción aplicada para mostrarlo en los reportes de consola.

#### `src/strategy/SinDescuento.java`
- **`aplicarPromocion`**: Multiplica directamente `precioUnitario * cantidad` sin rebajas.
- **`getDescripcion`**: Retorna `"Sin descuento (precio regular)"`.

#### `src/strategy/DescuentoPorcentaje.java`
- **Atributo `private final double porcentaje`**: Guarda el porcentaje de descuento (por ejemplo, `20` para 20%).
- **Constructor `DescuentoPorcentaje(double porcentaje)`**: Valida que el porcentaje esté en el rango `[0, 100]` lanzando `IllegalArgumentException` si es inválido.
- **`aplicarPromocion`**: Calcula `subtotal = precioUnitario * cantidad` y aplica el factor `(1.0 - porcentaje / 100.0)`.
- **`getDescripcion`**: Formatea el texto con `Locale.US`, por ejemplo `"Descuento porcentual (20%)"`.

#### `src/strategy/DescuentoMontoFijo.java`
- **Atributo `private final double montoDescuento`**: Almacena el monto fijo a restar (por ejemplo, `S/ 75.00`).
- **Constructor `DescuentoMontoFijo(double montoDescuento)`**: Verifica que el descuento no sea negativo.
- **`aplicarPromocion`**: Resta `montoDescuento` al subtotal y usa `Math.max(0.0, ...)` para garantizar que el total nunca sea negativo si el bono supera el valor de la compra.
- **`getDescripcion`**: Retorna `"Descuento de monto fijo (S/ 75.00)"`.

#### `src/strategy/PromocionDosPorUno.java`
- **`aplicarPromocion`**: Calcula cuántas unidades deben cobrarse mediante `(cantidad / 2) + (cantidad % 2)` (por ejemplo, para 4 unidades cobra 2; para 5 unidades cobra 3) y multiplica ese valor por `precioUnitario`.
- **`getDescripcion`**: Retorna `"Promoción 2x1 (paga 1 de cada 2 unidades)"`.

#### `src/strategy/CalculadoraPrecios.java`
- **Atributo `private EstrategiaPromocion estrategia`**: Mantiene una referencia a la estrategia actualmente seleccionada.
- **Constructor `CalculadoraPrecios(EstrategiaPromocion estrategia)`**: Exige una estrategia inicial válida (no nula).
- **Método `public void setEstrategia(EstrategiaPromocion estrategia)`**: Permite reemplazar la estrategia en tiempo de ejecución sin recrear la calculadora.
- **Método `public double calcularTotal(double precioUnitario, int cantidad)`**: Delega el cálculo completo a `estrategia.aplicarPromocion(...)`.
- **Método `public String getDescripcionEstrategia()`**: Expone la descripción de la estrategia activa.

#### `src/strategy/Main.java`
- **Método auxiliar `mostrarResumen(...)`**: Calcula el subtotal (`precioUnitario * cantidad`), obtiene el total final usando `calculadora.calcularTotal(...)`, calcula el ahorro (`subtotal - totalFinal`) e imprime el resumen formateado.
- **Método `main`**: Define el caso de prueba `"Audífonos Bluetooth"` (`4` unidades a `S/ 120.00` = `S/ 480.00`), inicia `CalculadoraPrecios` con `SinDescuento` y luego cambia dinámicamente mediante `setEstrategia(...)` a `DescuentoPorcentaje(20)`, `DescuentoMontoFijo(75.00)` y `PromocionDosPorUno()`.

### 3.3 Cumplimiento de requisitos (Strategy)

| Requisito solicitado | Implementación en el código |
|---|---|
| Interfaz de estrategia | `EstrategiaPromocion.java` (`aplicarPromocion`, `getDescripcion`) |
| Al menos 3 estrategias concretas | 4 estrategias: `SinDescuento`, `DescuentoPorcentaje`, `DescuentoMontoFijo`, `PromocionDosPorUno` |
| Contexto con cambio en tiempo de ejecución | `CalculadoraPrecios.java` con `setEstrategia(...)` |
| Prueba con cada estrategia | `Main.java` evalúa las 4 promociones sobre el mismo producto y compara resultados |

### 3.4 Compilación y salida real obtenida (Strategy)

```powershell
javac -Xlint:all -encoding UTF-8 -d .tmp_bin actividad-patrones-diseno/src/strategy/*.java
java -Dfile.encoding=UTF-8 -Dstdout.encoding=UTF-8 -cp .tmp_bin strategy.Main
```

```text
=== PATRÓN STRATEGY: PROMOCIONES DE PRODUCTOS ===
Estrategia : Sin descuento (precio regular)
Producto   : Audífonos Bluetooth (4 x S/ 120.00 = S/ 480.00)
Total final: S/ 480.00  (Ahorro: S/ 0.00)
--------------------------------------------------
Estrategia : Descuento porcentual (20%)
Producto   : Audífonos Bluetooth (4 x S/ 120.00 = S/ 480.00)
Total final: S/ 384.00  (Ahorro: S/ 96.00)
--------------------------------------------------
Estrategia : Descuento de monto fijo (S/ 75.00)
Producto   : Audífonos Bluetooth (4 x S/ 120.00 = S/ 480.00)
Total final: S/ 405.00  (Ahorro: S/ 75.00)
--------------------------------------------------
Estrategia : Promoción 2x1 (paga 1 de cada 2 unidades)
Producto   : Audífonos Bluetooth (4 x S/ 120.00 = S/ 480.00)
Total final: S/ 240.00  (Ahorro: S/ 240.00)
--------------------------------------------------
```

---

## 4. Ejercicio 3: Patrón Command — Control Remoto de Televisor

### 4.1 ¿En qué consiste y qué problema resuelve?
El patrón **Command** encapsula una petición o acción como un objeto independiente que implementa una interfaz común (`Command`). De este modo, el objeto que dispara la acción (**Invocador**) queda totalmente desacoplado del objeto que sabe cómo ejecutarla (**Receptor**).

- **Problema que resuelve:** Evita que el control remoto (`ControlRemoto`) dependa directamente de métodos específicos del televisor o mantenga condicionales rígidos por cada botón. El control únicamente llama `comando.execute()`, sin importarle qué operación concreta se ejecutará.
- **Roles del patrón en este ejercicio:**
  - **Interfaz Command:** `Command` (`Command.java`).
  - **Receptor:** `Televisor` (`Televisor.java`).
  - **Comandos Concretos (5):** `EncenderTelevisorCommand`, `ApagarTelevisorCommand`, `SubirVolumenCommand`, `BajarVolumenCommand`, `CambiarCanalCommand`.
  - **Invocador:** `ControlRemoto` (`ControlRemoto.java`).
  - **Cliente:** `Main` (`Main.java`).

### 4.2 Explicación archivo por archivo y bloque por bloque

#### `src/command/Command.java`
- **Interfaz `Command`**: Declara un único método `void execute();`. Cualquier acción que el control remoto deba ejecutar implementará este contrato.

#### `src/command/Televisor.java`
- **Atributos de estado**:
  - `private boolean encendido = false;` (el televisor inicia apagado).
  - `private int volumen = 15;` (nivel inicial de volumen).
  - `private int canal = 1;` (canal inicial).
- **Cinco acciones reales**:
  1. **`encender()`**: Cambia `encendido = true` e informa el canal y volumen actuales.
  2. **`apagar()`**: Cambia `encendido = false` e imprime que el televisor fue apagado.
  3. **`subirVolumen()`**: Verifica que esté encendido; incrementa el volumen en `+5` con límite máximo `100` (`Math.min(100, volumen + 5)`).
  4. **`bajarVolumen()`**: Verifica que esté encendido; reduce el volumen en `-5` con límite mínimo `0` (`Math.max(0, volumen - 5)`).
  5. **`cambiarCanal(int nuevoCanal)`**: Verifica que esté encendido y que `nuevoCanal > 0`; actualiza `canal = nuevoCanal` e imprime el nuevo canal.

#### Comandos concretos (5 clases)
- **`EncenderTelevisorCommand.java`**: Guarda la referencia `private final Televisor televisor;` y en `execute()` invoca `televisor.encender()`.
- **`ApagarTelevisorCommand.java`**: Guarda `televisor` y en `execute()` invoca `televisor.apagar()`.
- **`SubirVolumenCommand.java`**: Guarda `televisor` y en `execute()` invoca `televisor.subirVolumen()`.
- **`BajarVolumenCommand.java`**: Guarda `televisor` y en `execute()` invoca `televisor.bajarVolumen()`.
- **`CambiarCanalCommand.java`**: Además de `televisor`, almacena el parámetro `private final int nuevoCanal;` pasado por constructor y en `execute()` llama a `televisor.cambiarCanal(nuevoCanal)`. Esto demuestra cómo un comando encapsula tanto al receptor como los argumentos necesarios para la acción.

#### `src/command/ControlRemoto.java`
- **Atributo `private Command comando`**: Guarda el comando asignado actualmente al botón del control.
- **Método `public void setCommand(Command comando)`**: Configura dinámicamente qué orden ejecutará el botón.
- **Método `public void presionarBoton()`**: Comprueba que `comando != null` y ejecuta `comando.execute()`. El control remoto nunca conoce ni importa `Televisor`.

#### `src/command/Main.java`
- **Ensamblaje de objetos**: Crea `Televisor tv` y `ControlRemoto control`, e instancia los 5 comandos concretos vinculados a `tv` (configurando `CambiarCanalCommand(tv, 7)`).
- **Ejecución secuencial de las 5 funcionalidades**:
  1. Encender televisor (`EncenderTelevisorCommand`).
  2. Subir volumen (`SubirVolumenCommand`, pasa de 15 a 20).
  3. Cambiar al canal 7 (`CambiarCanalCommand`).
  4. Bajar volumen (`BajarVolumenCommand`, pasa de 20 a 15).
  5. Apagar televisor (`ApagarTelevisorCommand`).

### 4.3 Cumplimiento de requisitos (Command)

| Requisito solicitado | Implementación en el código |
|---|---|
| Interfaz `Command` con `execute()` | `Command.java` |
| Receptor `Televisor` con 5 acciones reales | `Televisor.java` (`encender`, `apagar`, `subirVolumen`, `bajarVolumen`, `cambiarCanal`) |
| 5 comandos concretos | `EncenderTelevisorCommand`, `ApagarTelevisorCommand`, `SubirVolumenCommand`, `BajarVolumenCommand`, `CambiarCanalCommand` |
| Invocador `ControlRemoto` | `ControlRemoto.java` con `setCommand()` y `presionarBoton()` |
| Cliente que configura y ejecuta las 5 funcionalidades | `Main.java` ejecuta paso a paso las 5 acciones |

### 4.4 Compilación y salida real obtenida (Command)

```powershell
javac -Xlint:all -encoding UTF-8 -d .tmp_bin actividad-patrones-diseno/src/command/*.java
java -Dfile.encoding=UTF-8 -Dstdout.encoding=UTF-8 -cp .tmp_bin command.Main
```

```text
=== PATRÓN COMMAND: CONTROL REMOTO DE TELEVISOR ===

1. Acción: Encender televisor
  [TV] Televisor encendido (Canal 1, Volumen 15).

2. Acción: Subir volumen
  [TV] Volumen aumentado a 20.

3. Acción: Cambiar al canal 7
  [TV] Canal cambiado al 7.

4. Acción: Bajar volumen
  [TV] Volumen disminuido a 15.

5. Acción: Apagar televisor
  [TV] Televisor apagado.
```
