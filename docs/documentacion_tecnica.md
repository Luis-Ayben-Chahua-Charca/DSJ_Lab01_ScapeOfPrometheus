# Documentación técnica — The Scape of Prometheus

## Qué es el proyecto

Juego 2D top-down hecho en **Python + Pygame** (pygame 2.6.1). El jugador controla una nave que explora un mapa de salas conectadas por puertas, combate oleadas de enemigos que la persiguen, recoge ítems y escudos, y debe derrotar al jefe de la sala final para ganar la run.

## Estructura de carpetas

| Carpeta | Responsabilidad |
|---|---|
| `core/` | Arranque de Pygame, bucle principal del juego (`Game`), carga de assets, constantes de motor (pantalla, FPS, colores). |
| `entities/` | Clases del jugador y los enemigos (posición, movimiento, vida, orientación). |
| `weapons/` | La bala del jugador: su trayectoria y su punto de origen según la dirección disparada. |
| `items/` | Los pickups del suelo: escudo y los 5 ítems permanentes, todos comparten una clase base. |
| `bosses/` | Los 3 jefes (Apolo, Anubis, Loki): comportamiento, proyectiles propios y HUD de nombre/vida. |
| `rooms/` | El mapa de salas: qué sala es cada una, sus conexiones, y el manejador que controla en cuál está el jugador. |
| `systems/` | Lógica transversal: colisiones, spawn de enemigos, navegación entre salas, puntaje. |
| `ui/` | Todo lo que se dibuja en pantalla fuera del mundo de juego: HUD de vida/score, minimapa, paredes/puertas, pantallas de Game Over y Victoria. |
| `data/` | Constantes de configuración y el layout fijo del mapa de salas. |
| `assets/` | Imágenes, sonidos y música. |

## Controles

- **Movimiento:** `W`/`A`/`S`/`D` (arriba/izquierda/abajo/derecha), en las 4 direcciones libremente dentro de la sala.
- **Disparo:** flechas direccionales (↑↓←→). Dispara en la dirección de la flecha presionada, con un cooldown entre disparos (más rápido si se tiene el ítem Telescopio). Mantener la flecha presionada sigue disparando automáticamente apenas el cooldown lo permite, sin necesidad de soltar y volver a apretar. Si se sostiene más de una flecha a la vez, dispara en una sola dirección con prioridad arriba > abajo > izquierda > derecha.
- La nave rota visualmente para apuntar hacia la última dirección en la que disparó — el movimiento no cambia hacia dónde mira.

## Sistema de salas

El mapa es fijo, con 9 salas: una sala inicial (`start`, sin enemigos) desde la que salen cuatro brazos — norte, sur, oeste (con una sala de ítem colgando de ella) y una cadena de tres salas al este que dobla hacia el norte hasta la sala del jefe. Cada sala sabe qué vecino tiene en cada lado (o ninguno, si ese borde es pared llena). La cantidad de enemigos de cada sala de combate se sortea (entre 2 y 6) cada vez que empieza una run.

- **Puertas:** un hueco en la pared del lado donde hay conexión con otra sala.
- **Puerta cerrada** (la sala donde estás parado todavía tiene enemigos vivos): se comporta como pared, no se puede cruzar. Se ve marcada en rojo con una X.
- **Puerta abierta** (la sala está limpia): se puede caminar a través de ella. Al cruzar, aparecés cerca del borde opuesto de la sala vecina.
- Los enemigos de una sala se generan la primera vez que se entra a ella; si ya está limpia, no vuelven a aparecer.
- La **sala de ítem** no tiene enemigos y siempre entrega, la primera vez que se entra, un ítem al azar en el centro de la sala (garantizado, no depende del dado de drops).
- La **sala del jefe** genera, la primera vez que se entra, uno de los 3 jefes al azar (nunca se repite el mismo dos veces seguidas mientras no se agoten los 3).
- **Minimapa** (esquina superior derecha): un cuadrado por sala conocida — resaltada la sala actual, en un tono distinto las salas ya visitadas y las salas vecinas todavía no exploradas. Se va revelando a medida que el jugador se acerca, no muestra el mapa completo desde el inicio.

## Sistema de vida

- El jugador tiene una cantidad de escudos (vida) representada por íconos en la esquina superior izquierda.
- Pierde un escudo al tocar a un enemigo (no hace falta que lo mate una bala). Tras recibir daño, queda brevemente invulnerable (parpadea) y no puede volver a perder vida hasta que el parpadeo termine.
- Los enemigos muertos por bala a veces (1 de cada 5) dejan caer un pickup de escudo en el suelo. Recogerlo **cura un escudo**, pero no aumenta el máximo, y no se puede recoger si la vida ya está llena (se queda intacto en el suelo hasta que haga falta).
- El máximo de escudos solo sube con el ítem Astronauta (ver abajo).
- Si la vida llega a 0: pantalla de Game Over.

## Jefes

Al entrar por primera vez a la sala del jefe aparece uno de estos 3 (elegido al azar, sin repetir hasta agotar los 3), con el doble de tamaño de un enemigo común, un fade-in de su sprite y su nombre, y una barra de vida abajo de la pantalla:

- **Apolo** — se acerca brevemente, gira sobre sí mismo (telegraph del ataque) y dispara una ráfaga de proyectiles en 8 direcciones a la vez.
- **Anubis** — no persigue: se alinea con la columna del jugador, muestra una advertencia breve y dispara un rayo continuo por esa columna.
- **Loki** — se desvanece y se teletransporta a una de las 4 paredes de la sala; tras una breve pausa, encadena varios ataques seguidos (disparo recto, diagonal, o una ráfaga de proyectiles paralelos, según hacia dónde da esa pared) antes de desvanecerse otra vez y cambiar de pared.

Los tres dañan al jugador por contacto directo además de con sus ataques. Las balas del jugador les restan vida por impacto; llegar a 0 gana la run.

## Cómo se gana

Derrotar al jefe de la sala final.

## Ítems

Los enemigos muertos por bala también pueden (1 de cada 10, en un dado aparte del escudo) dejar caer uno de estos 5 ítems al azar. Sus efectos son permanentes durante la run y se acumulan si se recogen varias veces:

1. **Telescopio** — dispara más seguido (cada copia reduce a la mitad el tiempo entre disparos).
2. **Sonda** — aumenta la velocidad de movimiento (+50% por copia).
3. **Asteroide** — las balas atraviesan enemigos en vez de destruirse al primer impacto, pudiendo matar a varios en su trayectoria.
4. **Satélite** — hace más lenta la persecución de todos los enemigos del mapa, incluso los que todavía no aparecieron.
5. **Astronauta** — agrega 2 escudos al máximo de vida (vacíos; se llenan recogiendo escudos normales).

## HUD en pantalla

Además de los escudos de vida (arriba a la izquierda) y el puntaje, el jugador ve en todo momento qué ítems permanentes tiene recogidos: un ícono por cada ítem del que tiene al menos una copia, con un número encima si acumuló más de una (Telescopio, Sonda o Satélite). El minimapa y, durante la pelea, el nombre y la barra de vida del jefe, completan la información en pantalla — ver las secciones correspondientes arriba.

## Audio

Mientras se explora el mapa suena una música de fondo distinta a la que suena durante la pelea contra el jefe: al entrar a su sala, la música cambia a un tema propio de ese jefe en particular. Además, las acciones principales del juego tienen su propio efecto de sonido: disparar, recibir daño, recoger un escudo o ítem, los proyectiles de los jefes al dispararse, y el desenlace de la run (victoria o derrota).

## Cómo reiniciar una run

Desde la pantalla de **Game Over** o **Victoria**, presionar **R** reinicia todo desde cero (mapa, vida, ítems, puntaje) y vuelve a jugar. **ESC** cierra el juego desde esas mismas pantallas.
