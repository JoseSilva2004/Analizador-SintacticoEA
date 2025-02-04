from data.generate_data import load_data_from_csv
from data.preprocess_data import preprocess_data
from model.build_model import build_model
from model.train_model import train_model
from utils.predict import predecir_expresion

def main():
    # Cargar datos desde el archivo CSV
    file_path = "data/datos.csv"  # Ruta al archivo CSV
    expresiones, etiquetas = load_data_from_csv(file_path)

    # Preprocesar datos
    X, y_tipos, y_operaciones, tokenizer, max_len, tipo_to_index, operacion_to_index = preprocess_data(expresiones, etiquetas)

    # Construir el modelo
    vocab_size = len(tokenizer.word_index) + 1
    embedding_dim = 64
    num_tipos = len(tipo_to_index)
    num_operaciones = len(operacion_to_index)
    model = build_model(vocab_size, embedding_dim, num_tipos, num_operaciones, max_len)

    # Entrenar el modelo
    train_model(model, X, {'tipos': y_tipos, 'operaciones': y_operaciones})

    # Hacer una predicción
    expresion_test = "x + y + z"
    tipo, operacion = predecir_expresion(model, tokenizer, max_len, tipo_to_index, operacion_to_index, expresion_test)
    print(f"La expresión '{expresion_test}' es clasificada como: {tipo}, Operacion: {operacion}")

if __name__ == "__main__":
    main()