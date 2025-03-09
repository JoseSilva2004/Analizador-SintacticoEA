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
    
    # Mostrar barra de progreso y mensaje "Entrenando el modelo..."
    progress_bar.grid(row=6, column=1, pady=10)
    progress_label.config(text="Entrenando el modelo...")
    progress_label.grid(row=5, column=1, pady=5)
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
    
    # Ocultar barra de progreso y mensaje una vez terminado el entrenamiento
    progress_bar.grid_remove()
    progress_label.grid_remove()
    messagebox.showinfo("Entrenamiento", "Modelo entrenado exitosamente.")

# Función para realizar una predicción con los pasos de resolución
def predecir():
    expresion_test = entrada_expresion.get()
    if not expresion_test:
        messagebox.showerror("Error", "Ingrese una expresión.")
        return
    if model is None:
        messagebox.showerror("Error", "El modelo no está entrenado.")
        return

    tipo, operacion = predecir_expresion(model, tokenizer, max_len, tipo_to_index, operacion_to_index, expresion_test)
    pasos = resolver_expresion(expresion_test)  # Generar los pasos de resolución

    resultado.set(f"Clasificación: {tipo}, Operación: {operacion}")
    pasos_texto.delete("1.0", tk.END)
    pasos_texto.insert(tk.END, "\n".join(pasos))

# Función para animar el GIF de forma continua
def animar_gif(indice=0):
    frame = frames[indice]
    label_gif.config(image=frame)
    # Actualizamos cada 100ms, lo que hace que el GIF se mueva continuamente
    root.after(100, animar_gif, (indice + 1) % len(frames))  # El índice se reinicia después de todos los frames

# Configuración de la ventana principal
root = tk.Tk()
root.title("Analizador de Expresiones Algebraicas")
root.configure(bg="#2C3E50")  # Fondo oscuro para mejor contraste

# Maximizar la ventana sin ocultar la barra de tareas (pantalla casi completa)
root.state('zoomed')

expresiones, etiquetas = None, None
model, tokenizer, max_len, tipo_to_index, operacion_to_index = None, None, None, None, None

# Cargar imágenes (ajustar dimensiones para que coincidan con el GIF)
gif = Image.open("matematica.gif")  # Cargar el GIF

# Solo redimensionar si el tamaño del GIF excede un umbral
max_size = (350, 350)  # Definir el tamaño máximo deseado

# Comprobar si es necesario redimensionar
if gif.size[0] > max_size[0] or gif.size[1] > max_size[1]:
    gif = gif.resize(max_size)

imagen_estatica = gif.copy().convert("RGBA")  # Copiar el tamaño del GIF para la imagen estática
imagen_estatica = ImageTk.PhotoImage(imagen_estatica)  # Convertir a formato adecuado para Tkinter
logo_udo = Image.open("logo_udo.jpg").resize((150, 150))  # Ajustar tamaño
logo_udo = ImageTk.PhotoImage(logo_udo)

# Extraer los frames del GIF correctamente
frames = [ImageTk.PhotoImage(frame.convert("RGBA")) for frame in ImageSequence.Iterator(gif)]  # Extraer los frames

# Crear Label para mostrar la imagen/GIF
label_gif = tk.Label(root, bg="#2C3E50", image=imagen_estatica, relief="solid", bd=5)
label_gif.grid(row=0, column=0, padx=30, pady=20)

# Iniciar la animación del GIF de manera continua
animar_gif()  # Inicia el ciclo de animación inmediatamente

# Crear el frame de la UI a la derecha
frame_contenido = tk.Frame(root, bg="#34495E", padx=20, pady=20)
frame_contenido.grid(row=0, column=1, padx=30, pady=30)

# Elementos de la UI dentro del frame de contenido
title_label = tk.Label(frame_contenido, text="Analice y resuelva su expresión con IA", font=("Helvetica", 22, "bold"), fg="#ECF0F1", bg="#34495E")
title_label.grid(row=0, column=1, pady=20)

btn_cargar = ttk.Button(frame_contenido, text="Cargar Datos", command=cargar_datos, width=20, style="TButton")
btn_cargar.grid(row=1, column=1, pady=10)

btn_entrenar = ttk.Button(frame_contenido, text="Entrenar Modelo", command=entrenar_modelo, width=20, style="TButton")
btn_entrenar.grid(row=2, column=1, pady=10)

entrada_expresion = ttk.Entry(frame_contenido, width=40, font=("Helvetica", 14), style="TEntry")
entrada_expresion.grid(row=3, column=1, pady=10, padx=10)

btn_predecir = ttk.Button(frame_contenido, text="Predecir", command=predecir, width=20, style="TButton")
btn_predecir.grid(row=4, column=1, pady=10)

resultado = tk.StringVar()
label_resultado = tk.Label(frame_contenido, textvariable=resultado, font=("Helvetica", 16), fg="#ECF0F1", bg="#34495E")
label_resultado.grid(row=5, column=1, pady=20)

# Crear barra de progreso y etiqueta para mensajes
progress_label = tk.Label(frame_contenido, text="", font=("Helvetica", 14), fg="#ECF0F1", bg="#34495E")
progress_bar = ttk.Progressbar(frame_contenido, orient="horizontal", length=300, mode="determinate")
progress_bar.grid(row=6, column=1, pady=10)

# Área de texto para mostrar los pasos de resolución
pasos_texto = tk.Text(frame_contenido, height=8, width=50, font=("Helvetica", 14), wrap="word", bg="#ECF0F1", fg="#2C3E50")
pasos_texto.grid(row=7, column=1, pady=20)

frame_presentacion = tk.Frame(root, bg="#2C3E50", padx=20, pady=20)
frame_presentacion.grid(row=0, column=2, padx=1, pady=60, sticky="nsew")

# Agregar el logo de la UDO
label_logo = tk.Label(frame_presentacion, image=logo_udo, bg="#2C3E50")
label_logo.pack(pady=10)

# Texto de presentación
texto_presentacion = """
Universidad de Oriente Nucleo Nueva Esparta
Introduccion a la inteligencia artificial
Análisis y solución de expresiones algebraicas usando IA.
 


Desarrollado por:
Isaac Hernandez C.I 30563299
Jose Silva C.I 30230054
Emmanuel Aponte 

"""
label_presentacion = tk.Label(frame_presentacion, text=texto_presentacion, font=("Helvetica", 14), fg="white", bg="#2C3E50", justify="center")
label_presentacion.pack(pady=10)

# Estilo de botones y entrada
style = ttk.Style()
style.configure("TButton", 
                font=("Helvetica", 14),
                padding=10,
                relief="flat",
                background="#2980b9",
                foreground="black")
style.map("TButton", background=[("active", "#3498db")])

style.configure("TEntry", 
                font=("Helvetica", 14),
                padding=10)

root.mainloop()
