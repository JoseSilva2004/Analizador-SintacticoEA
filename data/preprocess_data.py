from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical
import numpy as np

def preprocess_data(expresiones, etiquetas):
    # Tokenización de las expresiones
    tokenizer = Tokenizer(char_level=True)
    tokenizer.fit_on_texts(expresiones)
    sequences = tokenizer.texts_to_sequences(expresiones)

    # Padding para que todas las secuencias tengan la misma longitud
    max_len = max(len(seq) for seq in sequences)
    X = pad_sequences(sequences, maxlen=max_len, padding='post')

    # Convertir etiquetas a números
    tipos = sorted(list(set([etiqueta.split('_')[0] for etiqueta in etiquetas])))
    operaciones = sorted(list(set([etiqueta.split('_')[1] if '_' in etiqueta else 'ninguna' for etiqueta in etiquetas])))

    tipo_to_index = {tipo: idx for idx, tipo in enumerate(tipos)}
    operacion_to_index = {operacion: idx for idx, operacion in enumerate(operaciones)}

    y_tipos = np.array([tipo_to_index[etiqueta.split('_')[0]] for etiqueta in etiquetas])
    y_operaciones = np.array([operacion_to_index[etiqueta.split('_')[1] if '_' in etiqueta else 'ninguna'] for etiqueta in etiquetas])

    # Convertir etiquetas a one-hot encoding
    y_tipos = to_categorical(y_tipos, num_classes=len(tipo_to_index))
    y_operaciones = to_categorical(y_operaciones, num_classes=len(operacion_to_index))

    return X, y_tipos, y_operaciones, tokenizer, max_len, tipo_to_index, operacion_to_index