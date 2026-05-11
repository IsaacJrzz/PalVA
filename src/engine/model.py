from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from src.engine.agents.archaic import Australopithecus, Habilis, Erectus
from src.engine.agents.modern import Sapiens, Neanderthal, Denisovano, Heidelbergensis

class PaleoWorld(Model):
    def __init__(self, width, height, initial_pop):
        super().__init__()
        self.grid = MultiGrid(width, height, True)
        self.population = []
        self.year = 4000000
        self.env = self

        self.population_limits = {
            "Australopithecus": max(60, (width * height) // 5),
            "Habilis": max(25, (width * height) // 8),
            "Erectus": max(30, (width * height) // 6),
            "Heidelbergensis": max(25, (width * height) // 8),
            "Sapiens": max(20, (width * height) // 10),
            "Neanderthal": max(10, (width * height) // 12),
            "Denisovano": max(5, (width * height) // 20)
        }
        self.overall_capacity = max(width * height // 2, 100)

        self.evolution_events = [
            {"year": 2000000, "action": self._extinct_species, "species": Australopithecus, "name": "Australopithecus"},
            {"year": 2400000, "action": self._spawn_species, "species": Habilis, "count": 50, "name": "Homo habilis"},
            {"year": 1900000, "action": self._spawn_species, "species": Erectus, "count": 40, "name": "Homo erectus"},
            {"year": 1400000, "action": self._extinct_species, "species": Habilis, "name": "Habilis"},
            {"year": 700000, "action": self._spawn_species, "species": Heidelbergensis, "count": 35, "name": "Homo heidelbergensis"},
            {"year": 400000, "action": self._spawn_species, "species": Neanderthal, "count": 20, "name": "Neanderthal"},
            {"year": 400000, "action": self._spawn_species, "species": Denisovano, "count": 15, "name": "Denisovano"},
            {"year": 300000, "action": self._spawn_species, "species": Sapiens, "count": 30, "name": "Homo sapiens"},
            {"year": 200000, "action": self._extinct_species, "species": Heidelbergensis, "name": "Heidelbergensis"},
            {"year": 100000, "action": self._extinct_species, "species": Erectus, "name": "Erectus"},
            {"year": 50000, "action": self._extinct_species, "species": Denisovano, "name": "Denisovano"},
            {"year": 40000, "action": self._extinct_species, "species": Neanderthal, "name": "Neanderthal"}
        ]
        self.next_event_index = 0

        self.datacollector = DataCollector(
            model_reporters={
                "Pop": lambda m: len(m.population),
                "Total": lambda m: len(m.population),
                "Austra": lambda m: len([a for a in m.population if isinstance(a, Australopithecus)]),
                "Habilis": lambda m: len([a for a in m.population if isinstance(a, Habilis)]),
                "Erectus": lambda m: len([a for a in m.population if isinstance(a, Erectus)]),
                "Heidel": lambda m: len([a for a in m.population if isinstance(a, Heidelbergensis)]),
                "Neander": lambda m: len([a for a in m.population if isinstance(a, Neanderthal)]),
                "Denisov": lambda m: len([a for a in m.population if isinstance(a, Denisovano)]),
                "Sapiens": lambda m: len([a for a in m.population if isinstance(a, Sapiens)])
            }
        )

        # Spawn inicial de Australopithecus
        for i in range(initial_pop):
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            a = Australopithecus(self)
            self.grid.place_agent(a, (x, y))
            self.population.append(a)

        self.datacollector.collect(self)

    def consume_resource(self, *args):
        return 15.0

    def kill_agent(self, agent):
        if agent in self.population:
            try:
                if agent.pos is not None:
                    self.grid.remove_agent(agent)
                self.population.remove(agent)
            except Exception:
                pass

    def step(self):
        self.year -= 10000

        # Ejecutar agentes (con copia de lista por seguridad)
        current_agents = list(self.population)
        for agent in current_agents:
            try:
                agent.step()
            except Exception:
                continue

        self._handle_evolution_events()
        self._enforce_capacity_limits()

        # Importante: Recolectar datos al final de cada paso
        self.datacollector.collect(self)

    def _handle_evolution_events(self):
        while self.next_event_index < len(self.evolution_events) and self.year <= self.evolution_events[self.next_event_index]["year"]:
            event = self.evolution_events[self.next_event_index]
            event["action"](event["species"], event.get("count", 0), event.get("name", ""))
            self.next_event_index += 1

    def _spawn_species(self, species_class, count, name="Especie"):
        if count <= 0:
            return

        current_count = len([a for a in self.population if isinstance(a, species_class)])
        limit = self.population_limits.get(species_class.__name__, self.overall_capacity)
        count = min(count, max(0, limit - current_count))
        if count <= 0:
            return

        print(f"\n[EVOLUCIÓN] {self.year} AEC: Aparece {name} ({species_class.__name__}).")
        for _ in range(count):
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            agent = species_class(self)
            self.grid.place_agent(agent, (x, y))
            self.population.append(agent)

    def _extinct_species(self, species_class, *_args, name="Especie"):
        print(f"\n[EXTINCIÓN] {self.year} AEC: {name} desaparece de la simulación.")
        for agent in list(self.population):
            if isinstance(agent, species_class):
                self.kill_agent(agent)

    def _enforce_capacity_limits(self):
        if len(self.population) > self.overall_capacity:
            excess = len(self.population) - self.overall_capacity
            for agent in list(self.population)[:excess]:
                self.kill_agent(agent)

        for species_name, limit in self.population_limits.items():
            species_agents = [a for a in self.population if a.__class__.__name__ == species_name]
            if len(species_agents) > limit:
                excess = len(species_agents) - limit
                self.random.shuffle(species_agents)
                for agent in species_agents[:excess]:
                    self.kill_agent(agent)