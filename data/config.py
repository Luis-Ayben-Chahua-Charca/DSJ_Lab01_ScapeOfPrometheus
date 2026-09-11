from core.constants import GREEN, SCREEN_HEIGHT, SCREEN_WIDTH

# ==========================================
# Jugador
# ==========================================
PLAYER_SIZE = 64
PLAYER_SPEED = 4

PLAYER_START_X = SCREEN_WIDTH // 2 - PLAYER_SIZE // 2
PLAYER_START_Y = SCREEN_HEIGHT // 2 - PLAYER_SIZE // 2

PLAYER_MAX_HP = 3
PLAYER_INVULNERABILITY_DURATION = 2.0  # segundos, no frames — así no depende de los FPS

FIRE_COOLDOWN_BASE = 0.75  # segundos entre disparos (Telescopio lo reduce)
ROTATION_LERP_FACTOR = 0.25  # % de acercamiento al ángulo objetivo por frame

# ==========================================
# Enemigos
# ==========================================
ENEMY_SIZE = 64
ENEMY_CHASE_SPEED = 1.5

COMBAT_ROOM_MIN_ENEMIES = 2
COMBAT_ROOM_MAX_ENEMIES = 6

# Exclusión de spawn: no aparecer pegado a una puerta ni encima del jugador
DOOR_SPAWN_EXCLUSION = 40
ENEMY_SPAWN_MIN_DISTANCE_FROM_PLAYER = 100

# ==========================================
# Bala
# ==========================================
BULLET_SPEED = 10

# ==========================================
# Colisiones
# ==========================================
COLLISION_DISTANCE = 27

# ==========================================
# Drops
# ==========================================
SHIELD_DROP_CHANCE = 0.20
PICKUP_SIZE = 32

ITEM_DROP_CHANCE = 0.05
ITEM_PICKUP_SIZE = round(PICKUP_SIZE * 1.3)

TELESCOPE_COOLDOWN_MULTIPLIER = 0.5  # cada copia multiplica el cooldown efectivo por esto
SPEED_ITEM_BONUS = 0.5  # cada Sonda suma +50% de PLAYER_SPEED (aditivo, no compuesto)
SATELLITE_CHASE_MULTIPLIER_STEP = 0.5  # cada Satélite multiplica la persecución enemiga por esto
SATELLITE_MIN_CHASE_MULTIPLIER = 0.1  # piso: nunca deja a los enemigos casi congelados
ASTRONAUT_BONUS_HP = 2

# ==========================================
# Salas: paredes y puertas
# ==========================================
WALL_THICKNESS = 30
DOOR_WIDTH = 120

# Área jugable dentro de una sala (adentro de las paredes)
PLAYER_MIN_X = WALL_THICKNESS
PLAYER_MAX_X = SCREEN_WIDTH - WALL_THICKNESS - PLAYER_SIZE
PLAYER_MIN_Y = WALL_THICKNESS
PLAYER_MAX_Y = SCREEN_HEIGHT - WALL_THICKNESS - PLAYER_SIZE

ENEMY_MIN_X = WALL_THICKNESS
ENEMY_MAX_X = SCREEN_WIDTH - WALL_THICKNESS - ENEMY_SIZE
ENEMY_MIN_Y = WALL_THICKNESS
ENEMY_MAX_Y = SCREEN_HEIGHT - WALL_THICKNESS - ENEMY_SIZE

# Banda (rango) donde debe estar el centro del jugador para poder
# cruzar la puerta de un borde norte/sur (banda en X) o este/oeste (banda en Y)
DOOR_BAND_X = ((SCREEN_WIDTH - DOOR_WIDTH) // 2, (SCREEN_WIDTH + DOOR_WIDTH) // 2)
DOOR_BAND_Y = ((SCREEN_HEIGHT - DOOR_WIDTH) // 2, (SCREEN_HEIGHT + DOOR_WIDTH) // 2)

WALL_COLOR = (90, 90, 90)
DOOR_CLOSED_COLOR = (150, 30, 30)
DOOR_MARK_COLOR = (20, 20, 20)

# ==========================================
# UI
# ==========================================
SHIELD_ICON_SIZE = 28
SHIELD_ICON_GAP = 4
SHIELD_ICON_POS = (10, 10)
SHIELD_ICON_EMPTY_ALPHA = 70  # opacidad (0-255) de los espacios de vida ya perdidos

SCORE_FONT_SIZE = 32
SCORE_TEXT_POS = (10, 46)
SCORE_COLOR = GREEN

GAME_OVER_FONT_SIZE = 64
GAME_OVER_COLOR = GREEN

HINT_FONT_SIZE = 28

MINIMAP_CELL_SIZE = 18
MINIMAP_GAP = 3
MINIMAP_MARGIN = 10

MINIMAP_VISITED_COLOR = (200, 200, 200)
MINIMAP_DISCOVERED_COLOR = (80, 80, 80)
MINIMAP_CURRENT_COLOR = (255, 215, 0)
MINIMAP_BORDER_COLOR = (20, 20, 20)

# ==========================================
# Jefes (comunes a los 3)
# ==========================================
BOSS_MAX_HP = 40  # valor inicial para probar, ajustable tras jugarlo
BOSS_SIZE = ENEMY_SIZE * 2
BOSS_FADE_DURATION = 0.9  # segundos del fade-in de sprite + nombre al entrar

BOSS_MIN_X = WALL_THICKNESS
BOSS_MAX_X = SCREEN_WIDTH - WALL_THICKNESS - BOSS_SIZE
BOSS_MIN_Y = WALL_THICKNESS
BOSS_MAX_Y = SCREEN_HEIGHT - WALL_THICKNESS - BOSS_SIZE

PLASMA_BALL_SIZE = 24  # el archivo real es un ícono de 3600x3600, se reduce mucho

BOSS_NAME_FONT_SIZE = 36
BOSS_NAME_COLOR = GREEN
BOSS_NAME_Y = 90

BOSS_HP_BAR_WIDTH = 320
BOSS_HP_BAR_HEIGHT = 22
BOSS_HP_BAR_MARGIN_BOTTOM = 24
BOSS_HP_BAR_BG_COLOR = (40, 40, 40)
BOSS_HP_BAR_COLOR = (200, 40, 40)
BOSS_HP_BAR_BORDER_COLOR = (20, 20, 20)

# ==========================================
# Apolo (orange_boss)
# ==========================================
APOLLO_APPROACH_SPEED = 2.5  # px/frame, ver bosses/apollo.py
APOLLO_APPROACH_DURATION = 1.0  # segundos que dura cada acercamiento breve
APOLLO_MIN_DISTANCE_TO_PLAYER = 150  # deja de acercarse a esta distancia
APOLLO_SPIN_DURATION = 2.0
APOLLO_PROJECTILE_COUNT = 8
APOLLO_PROJECTILE_SPEED = 5  # px/frame

# ==========================================
# Anubis (black_boss)
# ==========================================
ANUBIS_BEAM_DURATION = 1.0
ANUBIS_BEAM_PAUSE = 2.0
ANUBIS_BEAM_THICKNESS = 30
ANUBIS_BEAM_COLOR = (255, 60, 60)
ANUBIS_ALIGN_SPEED = 3  # px/frame
ANUBIS_Y_OFFSET = 10  # separación fija respecto a la pared superior

ANUBIS_TELEGRAPH_DURATION = 1.0  # advertencia sin daño antes del rayo real
ANUBIS_TELEGRAPH_THICKNESS = 6  # bien más delgada que el rayo real (30px)
ANUBIS_TELEGRAPH_ALPHA = 120  # semitransparente

# ==========================================
# Loki (green_boss)
# ==========================================
LOKI_WALLS = ["top", "bottom", "left", "right"]
LOKI_WALL_OFFSET = 10  # separación fija respecto a la pared donde aparece

LOKI_FADE_DURATION = 0.4  # segundos del fade-out/fade-in de cada teletransporte
LOKI_GRACE_DURATION = 1.0  # segundos sin atacar recién reaparecido
LOKI_ATTACKS_PER_WALL = 3  # ataques seguidos antes de volver a teletransportarse
LOKI_WALL_DRIFT_SPEED = 0.8  # px/frame, vaivén cosmético a lo largo de la pared
LOKI_FIRE_COOLDOWN = 2.5  # segundos entre cada uno de los ataques de la parada
LOKI_PROJECTILE_SPEED = 5  # px/frame

LOKI_BURST_COUNT = 4  # disparos seguidos del patrón recto (antes era uno solo)
LOKI_BURST_INTERVAL = 0.25  # segundos entre cada disparo de la ráfaga recta

LOKI_PARALLEL_SHOT_COUNT = 5
LOKI_PARALLEL_GAP = 100  # > PLAYER_SIZE para que quepa entre dos proyectiles

# ==========================================
# HUD de ítems recogidos
# ==========================================
ITEM_HUD_ICON_SIZE = 28
ITEM_HUD_ICON_GAP = 6
ITEM_HUD_MARGIN = 10
ITEM_HUD_BADGE_FONT_SIZE = 16
ITEM_HUD_BADGE_COLOR = (20, 20, 20)
ITEM_HUD_BADGE_TEXT_COLOR = (255, 255, 255)

# ==========================================
# Audio
# ==========================================
# Segundos de fade-out de la pista actual antes de arrancar la siguiente en
# loop (exploración -> tema de jefe), para que el cambio no sea un corte seco.
MUSIC_TRANSITION_FADE_DURATION = 0.5
