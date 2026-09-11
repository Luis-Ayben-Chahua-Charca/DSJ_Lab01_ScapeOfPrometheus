from items.asteroid import AsteroidPickup
from items.astronaut import AstronautPickup
from items.probe import ProbePickup
from items.satellite import SatellitePickup
from items.telescope import TelescopePickup

# Los 5 ítems reales (no incluye ShieldPickup, que es un drop aparte).
ITEM_CLASSES = [TelescopePickup, ProbePickup, AsteroidPickup, SatellitePickup, AstronautPickup]
