import pandas as pd
import os

class StatsLogger:
    def __init__(self, filename="evolution_log.csv"):
        self.path = os.path.join("data", filename)
        self.data = []

    def log_step(self, step, year, model_vars):
        """
        Recibe los datos del paso actual y los guarda en una lista.
        """
        row = {"step": step, "year": year}
        row.update(model_vars)
        self.data.append(row)

    def save_to_csv(self):
        """
        Vuelca toda la información al disco.
        """
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        df = pd.DataFrame(self.data)
        df.to_csv(self.path, index=False)
        print(f"\n[INFO] Datos guardados exitosamente en: {self.path}")