import random

def smart_move(agent):
    """
    Busca la celda vecina con más recursos. 
    Ideal para especies con alta inteligencia.
    """
    neighbors = agent.model.grid.get_neighborhood(agent.pos, moore=True, include_center=False)
    # Evaluamos la comida en cada celda vecina
    best_cell = max(neighbors, key=lambda c: agent.model.env.resource_map[c[0], c[1]])
    agent.model.grid.move_agent(agent, best_cell)

def random_move(agent):
    """
    Movimiento errático. Consume menos energía mental pero es poco eficiente.
    """
    neighbors = agent.model.grid.get_neighborhood(agent.pos, moore=True, include_center=False)
    new_pos = random.choice(neighbors)
    agent.model.grid.move_agent(agent, new_pos)