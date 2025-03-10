from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

def train_model(model, X, y, epochs=100, batch_size=32, validation_split=0.05):
    # Callbacks
    early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
    model_checkpoint = ModelCheckpoint('best_model.h5', monitor='val_loss', save_best_only=True)

    # Entrenamiento
    history = model.fit(
        X, y,
        epochs=epochs,
        batch_size=batch_size,
        validation_split=validation_split,
        callbacks=[early_stopping, model_checkpoint]
    )
    return history