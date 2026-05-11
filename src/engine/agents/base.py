import mesa
import random

class HominidBase(mesa.Agent):
    def __init__(self, model, attributes=None):
        super().__init__(model)
        self.attributes = attributes if attributes else self.get_default_attributes()
        self.energy = 150.0
        self.species = "Generic Hominid"

    def get_default_attributes(self):
        return {
            "metabolic_rate": 3.5,
            "reproduction_threshold": 200.0,
            "intelligence": 0.1,
            "speed": 1,
            "resilience": 0.5
        }

    def move(self):
        # Lógica de movimiento base (puedes luego mover esto a behaviors/movement.py)
        neighbors = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        self.model.grid.move_agent(self, self.model.random.choice(neighbors))
        self.energy -= self.attributes["metabolic_rate"]

    def eat(self):
        x, y = self.pos
        extraction = 10 * (1 + self.attributes["intelligence"])
        self.energy += self.model.env.consume_resource(x, y, extraction)

    def step(self):
        self.move()
        self.eat()
        if self.energy <= 0:
            self.model.kill_agent(self)