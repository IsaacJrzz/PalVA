import solara
import mesa
from src.engine.model import PaleoWorld
from src.engine.agents.archaic import Australopithecus, Habilis, Erectus
from src.engine.agents.modern import Sapiens, Neanderthal, Denisovano, Heidelbergensis
import matplotlib.pyplot as plt

# Función para representar agentes en el grid
def agent_portrayal(agent):
    portrayal = {
        "Shape": "circle",
        "Filled": "true",
        "Layer": 0,
        "r": 0.5,
    }
    if isinstance(agent, Australopithecus):
        portrayal["Color"] = "red"
        portrayal["r"] = 0.3
    elif isinstance(agent, Habilis):
        portrayal["Color"] = "orange"
        portrayal["r"] = 0.4
    elif isinstance(agent, Erectus):
        portrayal["Color"] = "yellow"
        portrayal["r"] = 0.5
    elif isinstance(agent, Heidelbergensis):
        portrayal["Color"] = "green"
        portrayal["r"] = 0.5
    elif isinstance(agent, Neanderthal):
        portrayal["Color"] = "blue"
        portrayal["r"] = 0.4
    elif isinstance(agent, Denisovano):
        portrayal["Color"] = "purple"
        portrayal["r"] = 0.3
    elif isinstance(agent, Sapiens):
        portrayal["Color"] = "pink"
        portrayal["r"] = 0.4
    return portrayal

# Componente de Solara para la simulación
@solara.component
def SimulationView():
    # Estado para el modelo
    model_state, set_model_state = solara.use_state(PaleoWorld(50, 50, 60))
    running, set_running = solara.use_state(False)

    def step():
        if running:
            model_state.step()

    # Efecto para ejecutar pasos
    solara.use_effect(step, [running])

    with solara.Column():
        solara.Title("Simulación Evolutiva PALVA - Frontend Web")

        with solara.Row():
            solara.Button("Paso", on_click=lambda: model_state.step())
            solara.Button("Iniciar", on_click=lambda: set_running(True))
            solara.Button("Pausar", on_click=lambda: set_running(False))
            solara.Button("Reiniciar", on_click=lambda: set_model_state(PaleoWorld(50, 50, 60)))

        solara.Text(f"Año AEC: {model_state.year:,}")
        solara.Text(f"Población total: {len(model_state.population)}")

        # Grid de visualización usando Mesa
        solara.Markdown("### Grid de Simulación")
        mesa.visualization.solara_viz.SolaraViz(
            model_state,
            agent_portrayal,
            name="PaleoWorld Simulation"
        )

        # Gráfico de poblaciones
        solara.Markdown("### Evolución de Poblaciones")
        if hasattr(model_state, 'datacollector') and not model_state.datacollector.get_model_vars_dataframe().empty:
            df = model_state.datacollector.get_model_vars_dataframe()
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(df.index, df['Austra'], label='Australopithecus', color='red')
            ax.plot(df.index, df['Habilis'], label='Habilis', color='orange')
            ax.plot(df.index, df['Erectus'], label='Erectus', color='yellow')
            ax.plot(df.index, df['Heidel'], label='Heidelbergensis', color='green')
            ax.plot(df.index, df['Neander'], label='Neanderthal', color='blue')
            ax.plot(df.index, df['Denisov'], label='Denisovano', color='purple')
            ax.plot(df.index, df['Sapiens'], label='Sapiens', color='pink')
            ax.set_xlabel('Pasos')
            ax.set_ylabel('Población')
            ax.set_title('Evolución de Especies Hominidas')
            ax.legend()
            ax.grid(True)
            solara.FigureMatplotlib(fig)

# Ejecutar la app
if __name__ == "__main__":
    solara.run(SimulationView)