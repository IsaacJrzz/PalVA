import numpy as np

class EnvironmentManager:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # Mapa de biomas
        self.terrain_map = np.zeros((width, height))
        self.terrain_map[width//3 : 2*width//3, :] = 1 # Sabana
        self.terrain_map[2*width//3:, :] = 2           # Desierto
        
        # Inicialización de recursos
        self.resource_map = np.where(self.terrain_map == 0, 30.0, 12.0)
        self.resource_map = np.where(self.terrain_map == 2, 1.5, self.resource_map)

    def consume_resource(self, x, y, amount):
        available = self.resource_map[x, y]
        taken = min(available, amount)
        self.resource_map[x, y] -= taken
        return taken

    def apply_regeneration(self):
        # La selva (0) regenera más rápido que el desierto (2)
        reg_rate = np.where(self.terrain_map == 0, 0.25, 0.08)
        reg_rate = np.where(self.terrain_map == 2, 0.01, reg_rate)
        
        self.resource_map += reg_rate
        # Capacidad máxima de carga del suelo
        max_cap = np.where(self.terrain_map == 0, 50.0, 15.0)
        self.resource_map = np.clip(self.resource_map, 0, max_cap)