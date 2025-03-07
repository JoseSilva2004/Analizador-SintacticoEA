import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import time
from PIL import Image, ImageTk, ImageSequence
from data.generate_data import load_data_from_csv
from data.preprocess_data import preprocess_data
from model.build_model import build_model
from model.train_model import train_model
from utils.predict import predecir_expresion
from utils.resolver import resolver_expresion

# Función para cargar datos desde un archivo CSV
def cargar_datos():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        global expresiones, etiquetas
        expresiones, etiquetas = load_data_from_csv(file_path)
        messagebox.showinfo("Carga de Datos", "Datos cargados exitosamente.")

# Función para entrenar el modelo con animación de carga
def entrenar_modelo():
    global model, tokenizer, max_len, tipo_to_index, operacion_to_index
    if not expresiones:
        messagebox.showerror("Error", "Debe cargar los datos primero.")
        return
    
    progress_bar.grid(row=6, column=1, pady=10)  # Mostrar la barra de progreso
    root.update_idletasks()
    
    X, y_tipos, y_operaciones, tokenizer, max_len, tipo_to_index, operacion_to_index = preprocess_data(expresiones, etiquetas)
    vocab_size = len(tokenizer.word_index) + 1
    embedding_dim = 64
    num_tipos = len(tipo_to_index)
    num_operaciones = len(operacion_to_index)
    
    model = build_model(vocab_size, embedding_dim, num_tipos, num_operaciones, max_len)
    
    for i in range(5):
        progress_bar["value"] += 20
        root.update_idletasks()
        time.sleep(0.5)
    
    train_model(model, X, {'tipos': y_tipos, 'operaciones': y_operaciones})
    progress_bar.grid_remove()
    messagebox.showinfo("Entrenamiento", "Modelo entrenado exitosamente.")

# Configuración de la ventana principal
root = tk.Tk()
root.title("Clasificador de Expresiones Matemáticas")
root.geometry("800x500")
root.configure(bg="#2c3e50")

expresiones, etiquetas = None, None
model, tokenizer, max_len, tipo_to_index, operacion_to_index = None, None, None, None, None

# Cargar imágenes (primero la estática)
imagen_estatica = ImageTk.PhotoImage(Image.open("matematica.jpg"))  # Imagen fija
gif = Image.open("matematica.gif")  # Cargar el GIF
frames = [ImageTk.PhotoImage(frame.convert("RGBA")) for frame in ImageSequence.Iterator(gif)]  # Extraer los frames

gif_running = False  # Variable para controlar la animación

# Crear Label para mostrar la imagen/GIF
label_gif = tk.Label(root, bg="#2c3e50", image=imagen_estatica)
label_gif.grid(row=0, column=0, padx=10, pady=10)

# Función para animar el GIF
def animar_gif(indice=0):
    global gif_running
    if not gif_running:
        return
    frame = frames[indice]
    label_gif.config(image=frame)
    root.after(100, animar_gif, (indice + 1) % len(frames))  # Mostrar el siguiente frame

# Función para realizar una predicción con los pasos de resolución
def predecir():
    global gif_running
    expresion_test = entrada_expresion.get()
    if not expresion_test:
        messagebox.showerror("Error", "Ingrese una expresión.")
        return
    if model is None:
        messagebox.showerror("Error", "El modelo no está entrenado.")
        return

    # Cambiar la imagen a GIF antes de predecir
    gif_running = True
    animar_gif()

    tipo, operacion = predecir_expresion(model, tokenizer, max_len, tipo_to_index, operacion_to_index, expresion_test)
    pasos = resolver_expresion(expresion_test)  # Generar los pasos de resolución

    resultado.set(f"Tipo: {tipo}, Operación: {operacion}")
    pasos_texto.delete("1.0", tk.END)
    pasos_texto.insert(tk.END, "\n".join(pasos))

# Crear el frame de la UI a la derecha
frame_contenido = tk.Frame(root, bg="#34495e", padx=20, pady=20)
frame_contenido.grid(row=0, column=1, padx=20, pady=20)

# Elementos de la UI dentro del frame de contenido
title_label = tk.Label(frame_contenido, text="Clasificador de Expresiones", font=("Arial", 16, "bold"), fg="white", bg="#34495e")
title_label.grid(row=0, column=1, pady=10)

btn_cargar = ttk.Button(frame_contenido, text="Cargar Datos", command=cargar_datos)
btn_cargar.grid(row=1, column=1, pady=5)

btn_entrenar = ttk.Button(frame_contenido, text="Entrenar Modelo", command=entrenar_modelo)
btn_entrenar.grid(row=2, column=1, pady=5)

entrada_expresion = ttk.Entry(frame_contenido, width=40)
entrada_expresion.grid(row=3, column=1, pady=5)

btn_predecir = ttk.Button(frame_contenido, text="Predecir", command=predecir)
btn_predecir.grid(row=4, column=1, pady=5)

resultado = tk.StringVar()
label_resultado = tk.Label(frame_contenido, textvariable=resultado, font=("Arial", 12), fg="white", bg="#34495e")
label_resultado.grid(row=5, column=1, pady=10)

progress_bar = ttk.Progressbar(frame_contenido, orient="horizontal", length=300, mode="determinate")

# Área de texto para mostrar los pasos de resolución
pasos_texto = tk.Text(frame_contenido, height=8, width=50)
pasos_texto.grid(row=7, column=1, pady=10)

root.mainloop()
