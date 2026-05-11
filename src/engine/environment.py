import numpy as np

class EnvironmentManager:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # Inicializamos capas: Recursos (comida) y Elevación (barreras)
        self.resource_map = np.zeros((width, height))
        self.elevation_map = np.zeros((width, height))
        self.setup_rift_valley()

    def setup_rift_valley(self):
        """Simula un valle fértil rodeado de zonas más áridas."""
        for x in range(self.width):
            for y in range(self.height):
                # Una franja central fértil (el Valle)
                if self.width // 3 < x < 2 * self.width // 3:
                    self.resource_map[x, y] = 30.0
                else:
                    self.resource_map[x, y] = 10.0
        
    def apply_regeneration(self, rate=0.2, max_capacity=50.0):
        """Simula el crecimiento de vegetación en cada turno."""
        self.resource_map += rate
        self.resource_map = np.clip(self.resource_map, 0, max_capacity)

    def consume_resource(self, x, y, amount):
        """Extrae calorías del mapa."""
        actual_consumed = min(self.resource_map[x, y], amount)
        self.resource_map[x, y] -= actual_consumed
        return actual_consumed