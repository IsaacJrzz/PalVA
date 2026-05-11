import os
import sys
import time

# Añadimos el directorio raíz al path para evitar problemas de importación
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.engine.model import PaleoWorld
from src.utils.stats_logger import StatsLogger

def run_simulation(steps=400):
    """
    Orquesta la ejecución de la simulación evolutiva.
    """
    # 1. Preparación del entorno
    if not os.path.exists("data"):
        os.makedirs("data")
        print("[SISTEMA] Carpeta /data creada.")

    # 2. Inicialización
    # Parámetros: Ancho, Alto, Población inicial de Australopithecus
    width, height = 50, 50
    initial_pop = 60
    model = PaleoWorld(width, height, initial_pop)
    logger = StatsLogger(filename="simulacion_evolutiva.csv")

    print("\n" + "="*95)
    print(f"{'MOTOR DE SIMULACIÓN PALVA v2.0 - ARQUITECTURA MODULAR':^95}")
    print("="*95)
    print(f"{'PASO':<8} | {'AÑO (AEC)':<15} | {'POB. TOTAL':<12} | {'AUSTRA':<8} | {'HABILIS':<8} | {'ERECTUS':<8} | {'HEIDEL':<8} | {'NEANDER':<8} | {'DENISOV':<8} | {'SAPIENS':<8}")    
    print("-"*115)

    try:
        for i in range(steps):
            # Ejecutar un paso del modelo
            model.step()
            
            # Extraer datos del DataCollector
            df_vars = model.datacollector.get_model_vars_dataframe()
            if not df_vars.empty:
                current_data = df_vars.iloc[-1].to_dict()
                
                # Registrar en el Logger de utilidades
                logger.log_step(i, model.year, current_data)
                
                # Formatear la etiqueta del tiempo
                if model.year >= 1000000:
                    time_label = f"{model.year/1000000:.2f}M"
                else:
                    time_label = f"{model.year:,}"

                # Mostrar progreso en consola
                print(f"{i:<8} | {time_label:>10} AEC | {int(current_data.get('Pop', 0)):<12} | "
                    f"{int(current_data.get('Austra', 0)):<8} | "
                    f"{int(current_data.get('Habilis', 0)):<8} | "
                    f"{int(current_data.get('Erectus', 0)):<8} | "
                    f"{int(current_data.get('Heidel', 0)):<8} | "
                    f"{int(current_data.get('Neander', 0)):<8} | "
                    f"{int(current_data.get('Denisov', 0)):<8} | "
                    f"{int(current_data.get('Sapiens', 0)):<8}")

            # Condición de parada si todos mueren
            if not df_vars.empty and current_data['Pop'] == 0:
                print("\n[AVISO] Extinción total detectada. La simulación se detiene.")
                break
                
            # Pequeña pausa opcional para poder leer la terminal (quitar si quieres velocidad máxima)
            # time.sleep(0.01)

    except KeyboardInterrupt:
        print("\n[AVISO] Simulación pausada/interrumpida por el usuario.")
    except Exception as e:
        print(f"\n[ERROR CRÍTICO] Ocurrió un fallo en el motor: {e}")
    finally:
        # 3. Finalización y guardado
        print("\n" + "-"*115)
        print("[PROCESO] Volcando datos históricos al disco...")
        logger.save_to_csv()
        print("="*115)
        print(f"{'SIMULACIÓN FINALIZADA':^115}")
        print("="*115)

if __name__ == "__main__":
    # Ajusta los steps a 400 para llegar desde 4M AEC hasta el año 0 (4M / 10k = 400)
    run_simulation(steps=400)