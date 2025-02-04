# utils/tokenizer.py
from tensorflow.keras.preprocessing.text import Tokenizer
import re

def custom_tokenizer(expresiones):
    tokenizer = Tokenizer(char_level=False)
    tokenizer.fit_on_texts(expresiones)
    return tokenizer

def normalize_expression(expresion):
    # Normaliza la expresión (ejemplo básico)
    expresion = re.sub(r'\s+', '', expresion)  # Elimina espacios
    expresion = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expresion)  # Convierte 2x a 2*x
    return expresion