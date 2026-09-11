# The Scape of Prometheus

Roguelite top-down espacial, hecho para el curso de Laboratorio de Diseño de Juegos (UNSA). Explorá un mapa de salas, limpiá oleadas de enemigos, juntá ítems y enfrentá a uno de tres jefes para completar la run.

## Hecho con

Python + [Pygame](https://www.pygame.org/) (2.6.1).

## Cómo correrlo

**Requiere Python 3.11 o 3.12** — pygame 2.6.1 no tiene wheels para 3.13+ (falla al intentar compilar desde código fuente).

```bash
pip install -r requirements.txt
python main.py
```

## Controles

- **Mover:** `W` `A` `S` `D`
- **Disparar:** flechas direccionales (mantené presionada para disparar seguido)
- **R:** reintentar (en las pantallas de Game Over / Victoria)

## Qué hay para jugar

- Un mapa de 9 salas conectado por puertas, con un minimapa que se va revelando a medida que explorás.
- Escudos de vida y 5 ítems permanentes que cambian cómo jugás (más cadencia de disparo, más velocidad, balas que perforan, enemigos más lentos, más vida máxima).
- Un jefe final, elegido al azar entre 3 (Apolo, Anubis, Loki), cada uno con su propio patrón de ataque.

Para el detalle técnico completo (arquitectura, sistemas, mecánicas), ver [`docs/documentacion_tecnica.md`](docs/documentacion_tecnica.md).
