import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from data.generate_data import load_data_from_csv
from data.preprocess_data import preprocess_data
from model.build_model import build_model
from model.train_model import train_model
from utils.predict import predecir_expresion

def cargar_datos():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        global expresiones, etiquetas
        expresiones, etiquetas = load_data_from_csv(file_path)
        messagebox.showinfo("Carga de Datos", "Datos cargados exitosamente.")

def entrenar_modelo():
    global model, tokenizer, max_len, tipo_to_index, operacion_to_index
    if not expresiones:
        messagebox.showerror("Error", "Debe cargar los datos primero.")
        return
    X, y_tipos, y_operaciones, tokenizer, max_len, tipo_to_index, operacion_to_index = preprocess_data(expresiones, etiquetas)
    vocab_size = len(tokenizer.word_index) + 1
    embedding_dim = 64
    num_tipos = len(tipo_to_index)
    num_operaciones = len(operacion_to_index)
    model = build_model(vocab_size, embedding_dim, num_tipos, num_operaciones, max_len)
    train_model(model, X, {'tipos': y_tipos, 'operaciones': y_operaciones})
    messagebox.showinfo("Entrenamiento", "Modelo entrenado exitosamente.")

def predecir():
    expresion_test = entrada_expresion.get()
    if not expresion_test:
        messagebox.showerror("Error", "Ingrese una expresión.")
        return
    if model is None:
        messagebox.showerror("Error", "El modelo no está entrenado.")
        return
    tipo, operacion = predecir_expresion(model, tokenizer, max_len, tipo_to_index, operacion_to_index, expresion_test)
    resultado.set(f"Tipo: {tipo}, Operación: {operacion}")

# Configuración de la ventana
root = tk.Tk()
root.title("Clasificador de Expresiones Algebraicas")
root.geometry("600x400")
root.configure(bg="#2c3e50")

expresiones, etiquetas = None, None
model, tokenizer, max_len, tipo_to_index, operacion_to_index = None, None, None, None, None

frame = tk.Frame(root, bg="#34495e", padx=20, pady=20)
frame.pack(expand=True)

title_label = tk.Label(frame, text="Clasificador de Expresiones", font=("Arial", 16, "bold"), fg="white", bg="#34495e")
title_label.pack(pady=10)

btn_cargar = ttk.Button(frame, text="Cargar Datos", command=cargar_datos)
btn_cargar.pack(pady=5)

btn_entrenar = ttk.Button(frame, text="Entrenar Modelo", command=entrenar_modelo)
btn_entrenar.pack(pady=5)

entrada_expresion = ttk.Entry(frame, width=40)
entrada_expresion.pack(pady=5)

btn_predecir = ttk.Button(frame, text="Predecir", command=predecir)
btn_predecir.pack(pady=5)

resultado = tk.StringVar()
label_resultado = tk.Label(frame, textvariable=resultado, font=("Arial", 12), fg="white", bg="#34495e")
label_resultado.pack(pady=10)

root.mainloop()
