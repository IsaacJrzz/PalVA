from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.engine.model import PaleoWorld
from src.engine.agents.archaic import Australopithecus, Habilis, Erectus
from src.engine.agents.modern import Sapiens, Neanderthal, Denisovano, Heidelbergensis
import json

app = FastAPI(title="PALVA Simulation API", description="API for PaleoWorld evolutionary simulation")

# Configurar CORS para permitir requests desde el frontend React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar el dominio del frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo global de simulación
simulation_model = PaleoWorld(50, 50, 60)

class SimulationStatus(BaseModel):
    year: int
    total_population: int
    populations: dict
    grid: list
    evolution_events: list

@app.get("/status", response_model=SimulationStatus)
async def get_simulation_status():
    """Obtener el estado actual de la simulación"""
    df = simulation_model.datacollector.get_model_vars_dataframe()
    current_data = df.iloc[-1].to_dict() if not df.empty else {}

    # Crear representación del grid
    grid_data = []
    for x in range(simulation_model.grid.width):
        row = []
        for y in range(simulation_model.grid.height):
            cell_agents = simulation_model.grid.get_cell_list_contents([(x, y)])
            if cell_agents:
                agent = cell_agents[0]  # Asumir un agente por celda
                species = type(agent).__name__
                row.append({"species": species, "id": agent.unique_id})
            else:
                row.append(None)
        grid_data.append(row)

    # Eventos de evolución restantes
    remaining_events = [
        {"year": event["year"], "action": "spawn" if "spawn" in event["action"].__name__ else "extinct", "species": event["species"].__name__, "name": event.get("name", "")}
        for event in simulation_model.evolution_events[simulation_model.next_event_index:]
    ]

    return SimulationStatus(
        year=simulation_model.year,
        total_population=len(simulation_model.population),
        populations={
            "Australopithecus": current_data.get('Austra', 0),
            "Habilis": current_data.get('Habilis', 0),
            "Erectus": current_data.get('Erectus', 0),
            "Heidelbergensis": current_data.get('Heidel', 0),
            "Neanderthal": current_data.get('Neander', 0),
            "Denisovano": current_data.get('Denisov', 0),
            "Sapiens": current_data.get('Sapiens', 0)
        },
        grid=grid_data,
        evolution_events=remaining_events
    )

@app.post("/step")
async def execute_step():
    """Ejecutar un paso de la simulación"""
    try:
        simulation_model.step()
        return {"message": "Step executed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/reset")
async def reset_simulation():
    """Reiniciar la simulación"""
    global simulation_model
    simulation_model = PaleoWorld(50, 50, 60)
    return {"message": "Simulation reset successfully"}

@app.get("/population-data")
async def get_population_data():
    """Obtener datos históricos de poblaciones para gráficos"""
    df = simulation_model.datacollector.get_model_vars_dataframe()
    if df.empty:
        return {"data": []}

    data = []
    for index, row in df.iterrows():
        data.append({
            "step": int(index),
            "year": int(row.get('year', 0)),
            "Australopithecus": int(row.get('Austra', 0)),
            "Habilis": int(row.get('Habilis', 0)),
            "Erectus": int(row.get('Erectus', 0)),
            "Heidelbergensis": int(row.get('Heidel', 0)),
            "Neanderthal": int(row.get('Neander', 0)),
            "Denisovano": int(row.get('Denisov', 0)),
            "Sapiens": int(row.get('Sapiens', 0))
        })
    return {"data": data}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)