import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences

def predecir_expresion(model, tokenizer, max_len, tipo_to_index, operacion_to_index, expresion):
    # Tokenizar la expresión
    sequence = tokenizer.texts_to_sequences([expresion])
    
    # Aplicar padding a la secuencia
    padded_sequence = pad_sequences(sequence, maxlen=max_len, padding='post')
    
    # Hacer la predicción
    prediccion_tipos, prediccion_operaciones = model.predict(padded_sequence)
    
    # Obtener la clase predicha para el tipo de expresión
    indice_tipo = np.argmax(prediccion_tipos)
    tipo = list(tipo_to_index.keys())[list(tipo_to_index.values()).index(indice_tipo)]
    
    # Obtener la clase predicha para la operación
    indice_operacion = np.argmax(prediccion_operaciones)
    operacion = list(operacion_to_index.keys())[list(operacion_to_index.values()).index(indice_operacion)]
    
    # Devolver el resultado
    return tipo, operacion