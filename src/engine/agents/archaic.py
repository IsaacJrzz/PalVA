import random
from src.engine.agents.base import HominidBase

def apply_mutation(attributes):
    """Crea variaciones genéticas en los hijos."""
    new_attributes = attributes.copy()
    mutation_rate = attributes.get("mutation_rate", 0.1)
    
    for key in new_attributes:
        if key != "mutation_rate":
            # Variación aleatoria basada en el mutation_rate
            variation = 1 + random.uniform(-mutation_rate, mutation_rate)
            new_attributes[key] *= variation
            
    return new_attributes

class Australopithecus(HominidBase):
    def __init__(self, model, attributes=None):
        if attributes is None:
            # Stats de supervivencia básica
            attributes = {
                "metabolic_rate": 3.0,
                "reproduction_threshold": 160.0,
                "intelligence": 0.05,
                "speed": 1,
                "resilience": 0.4,
                "mutation_rate": 0.2
            }
        super().__init__(model, attributes)
        self.species = "Australopithecus"

    def step(self):
        # Presión evolutiva: Muerte natural acelerada cerca de su extinción
        if self.model.year < 2500000:
            if random.random() < 0.15:
                self.model.kill_agent(self)
                return

        super().step() # Moverse y comer
        
        if self.energy > self.attributes["reproduction_threshold"]:
            self.reproduce()

    def reproduce(self):
        self.energy /= 2.5 # Coste de energía
        child_attrs = apply_mutation(self.attributes)
        child = Australopithecus(self.model, child_attrs)
        
        if self.pos:
            self.model.grid.place_agent(child, self.pos)
            self.model.population.append(child)

class Habilis(HominidBase):
    def __init__(self, model, attributes=None):
        if attributes is None:
            # Stats mejoradas: El Habilis es más eficiente
            attributes = {
                "metabolic_rate": 2.2,
                "reproduction_threshold": 110.0,
                "intelligence": 0.45,
                "speed": 2,
                "resilience": 0.8,
                "mutation_rate": 0.1
            }
        super().__init__(model, attributes)
        self.species = "Habilis"

    def step(self):
        super().step()
        
        if self.energy > self.attributes["reproduction_threshold"]:
            self.reproduce()

    def reproduce(self):
        # El Habilis cuida mejor a su prole (gasta menos energía relativa)
        self.energy /= 2.0 
        child_attrs = apply_mutation(self.attributes)
        child = Habilis(self.model, child_attrs)
        
        if self.pos:
            self.model.grid.place_agent(child, self.pos)
            self.model.population.append(child)

class Erectus(HominidBase):
    def __init__(self, model, attributes=None):
        if attributes is None:
            # Homo erectus: Mayor eficiencia metabólica, inteligencia y velocidad
            attributes = {
                "metabolic_rate": 1.8,
                "reproduction_threshold": 100.0,
                "intelligence": 0.6,
                "speed": 3,
                "resilience": 1.0,
                "mutation_rate": 0.08
            }
        super().__init__(model, attributes)
        self.species = "Erectus"

    def step(self):
        super().step()
        
        if self.energy > self.attributes["reproduction_threshold"]:
            self.reproduce()

    def reproduce(self):
        self.energy /= 1.8
        child_attrs = apply_mutation(self.attributes)
        child = Erectus(self.model, child_attrs)
        
        if self.pos:
            self.model.grid.place_agent(child, self.pos)
            self.model.population.append(child)