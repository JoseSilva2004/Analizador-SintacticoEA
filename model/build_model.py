from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Embedding, Conv1D, MaxPooling1D, LSTM, Dense, Dropout, GlobalMaxPooling1D, concatenate

def build_model(vocab_size, embedding_dim, num_tipos, num_operaciones, max_len):
    # Entrada
    input_layer = Input(shape=(max_len,))

    # Capa de embedding
    embedding = Embedding(input_dim=vocab_size, output_dim=embedding_dim)(input_layer)

    # Capa convolucional
    conv = Conv1D(128, 5, activation='relu')(embedding)
    pool = MaxPooling1D(2)(conv)

    # Capa LSTM
    lstm = LSTM(128, return_sequences=True)(pool)
    lstm = Dropout(0.5)(lstm)

    # Pooling global
    global_pool = GlobalMaxPooling1D()(lstm)

    # Capas densas
    dense = Dense(64, activation='relu')(global_pool)
    dense = Dropout(0.5)(dense)

    # Salida para el tipo de expresión
    output_tipos = Dense(num_tipos, activation='softmax', name='tipos')(dense)

    # Salida para la operación
    output_operaciones = Dense(num_operaciones, activation='softmax', name='operaciones')(dense)

    # Modelo
    model = Model(inputs=input_layer, outputs=[output_tipos, output_operaciones])

    # Compilar el modelo
    model.compile(
        optimizer='adam',
        loss={'tipos': 'categorical_crossentropy', 'operaciones': 'categorical_crossentropy'},
        metrics={'tipos': 'accuracy', 'operaciones': 'accuracy'}
    )

    return model