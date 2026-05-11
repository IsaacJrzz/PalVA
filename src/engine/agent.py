import mesa
import random

class HominidAgent(mesa.Agent):
    def __init__(self, model, attributes=None):
        # En Mesa 3.x, el modelo genera el ID automáticamente si no se pasa
        super().__init__(model)
        
        # Atributos biológicos
        if attributes is None:
            self.attributes = {
                "metabolic_rate": 1.0,
                "reproduction_threshold": 150,
                "vision_range": 2,
                "diet_efficiency": 1.0
            }
        else:
            self.attributes = attributes

        self.energy = 100 

    def move(self):
        # Elige una celda vecina al azar
        neighbors = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        new_position = self.random.choice(neighbors)
        self.model.grid.move_agent(self, new_position)
        self.energy -= self.attributes["metabolic_rate"]

    def eat(self):
        x, y = self.pos
        # Sacamos comida del mapa de recursos del modelo
        intake = self.model.env.consume_resource(x, y, 10) * self.attributes["diet_efficiency"]
        self.energy += intake

    def step(self):
        self.move()
        self.eat()
        
        # Lógica de muerte
        if self.energy <= 0:
            self.model.kill_agent(self)