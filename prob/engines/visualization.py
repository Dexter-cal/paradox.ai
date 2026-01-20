import matplotlib.pyplot as plt
import os
from datetime import datetime
import pandas as pd

class VisualizationEngine:
    def __init__(self, output_dir="prob/output/charts"):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def generate_bar_chart(self, data, x_label, y_label, title):
        """Generates a bar chart from a dictionary of data."""
        plt.figure(figsize=(10, 6))
        plt.bar(data.keys(), data.values())
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(title)

        filename = f"chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        path = os.path.join(self.output_dir, filename)
        plt.savefig(path)
        plt.close()
        return path

    def generate_from_dataframe(self, df, chart_type="line", **kwargs):
        """Generates a chart from a pandas DataFrame."""
        plt.figure(figsize=(10, 6))
        if chart_type == "line":
            df.plot(kind="line", **kwargs)
        elif chart_type == "bar":
            df.plot(kind="bar", **kwargs)
        elif chart_type == "hist":
            df.plot(kind="hist", **kwargs)

        filename = f"df_chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        path = os.path.join(self.output_dir, filename)
        plt.savefig(path)
        plt.close()
        return path
