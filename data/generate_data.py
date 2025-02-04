# data/generate_data.py
import pandas as pd

def load_data_from_csv(file_path):
    """
    Carga los datos de entrenamiento desde un archivo CSV.
    
    Args:
        file_path (str): Ruta al archivo CSV.
    
    Returns:
        expresiones (list): Lista de expresiones algebraicas.
        etiquetas (list): Lista de etiquetas correspondientes.
    """
    # Leer el archivo CSV
    df = pd.read_csv(file_path)
    
    # Obtener las columnas como listas
    expresiones = df['expresion'].tolist()
    etiquetas = df['etiqueta'].tolist()
    
    return expresiones, etiquetas