from src.engine.agents.base import HominidBase
from src.engine.behaviors.movement import smart_move
from src.engine.behaviors.genetics import apply_mutation

class Sapiens(HominidBase):
    def __init__(self, model, attributes=None):
        super().__init__(model, attributes)
        self.species = "Homo Sapiens"

    def move(self):
        # El Sapiens usa la estrategia de movimiento inteligente definida en behaviors
        smart_move(self)
        # Su cerebro gasta más energía (metabolismo base + coste cerebral)
        self.energy -= (self.attributes["metabolic_rate"] * 1.1)

    def step(self):
        super().step()
        if self.energy > self.attributes["reproduction_threshold"]:
            self.reproduce()

    def reproduce(self):
        self.energy /= 2.1
        child_attrs = apply_mutation(self.attributes)
        child = Sapiens(self.model, child_attrs)
        if self.pos:
            self.model.grid.place_agent(child, self.pos)
            self.model.population.append(child)

class Neanderthal(HominidBase):
    def __init__(self, model, attributes=None):
        super().__init__(model, attributes)
        self.species = "Neanderthal"

    def move(self):
        smart_move(self)
        # Son más pesados, gastan más energía al moverse
        self.energy -= (self.attributes["metabolic_rate"] * 1.3)

class Denisovano(HominidBase):
    def __init__(self, model, attributes=None):
        super().__init__(model, attributes)
        self.species = "Denisovano"
        # Atributo único: mejor resistencia al frío/altitud
        self.attributes["resilience"] *= 1.2

class Heidelbergensis(HominidBase):
    def __init__(self, model, attributes=None):
        if attributes is None:
            # Homo heidelbergensis: Antecesor de Neanderthal y Sapiens
            attributes = {
                "metabolic_rate": 1.5,
                "reproduction_threshold": 90.0,
                "intelligence": 0.7,
                "speed": 3,
                "resilience": 1.2,
                "mutation_rate": 0.06
            }
        super().__init__(model, attributes)
        self.species = "Heidelbergensis"

    def move(self):
        smart_move(self)
        self.energy -= (self.attributes["metabolic_rate"] * 1.05)

    def step(self):
        super().step()
        if self.energy > self.attributes["reproduction_threshold"]:
            self.reproduce()

    def reproduce(self):
        self.energy /= 1.9
        child_attrs = apply_mutation(self.attributes)
        child = Heidelbergensis(self.model, child_attrs)
        if self.pos:
            self.model.grid.place_agent(child, self.pos)
            self.model.population.append(child)