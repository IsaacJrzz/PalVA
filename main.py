from src.engine.model import PaleoWorld

def run():
    model = PaleoWorld(50, 50, 30)
    print("--- Simulación Iniciada ---")
    
    for i in range(50):
        model.step()
        pop = len(model.agents)
        print(f"Paso {i} | Población: {pop}")
        if pop == 0: break

if __name__ == "__main__":
    run()