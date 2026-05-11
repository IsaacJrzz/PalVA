import mesa
from .agent import HominidAgent
from .environment import EnvironmentManager

class PaleoWorld(mesa.Model):
    def __init__(self, width, height, initial_hominids):
        super().__init__()
        
        self.grid = mesa.space.MultiGrid(width, height, torus=False)
        self.env = EnvironmentManager(width, height)
        
        # Crear población inicial
        for i in range(initial_hominids):
            # Solo pasamos el modelo (self)
            a = HominidAgent(self)
            
            # Buscamos una posición al azar
            x = self.random.randrange(width)
            y = self.random.randrange(height)
            
            self.grid.place_agent(a, (x, y))

    def kill_agent(self, agent):
        # En Mesa 3.x, remove_agent es suficiente
        self.grid.remove_agent(agent)

    def step(self):
        self.env.apply_regeneration()
        # Esto ejecuta el 'step' de cada agente en orden aleatorio
        self.agents.shuffle_do("step")