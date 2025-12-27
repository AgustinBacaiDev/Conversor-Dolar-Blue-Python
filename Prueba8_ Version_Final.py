import tkinter as tk
from tkinter import messagebox, ttk
import requests
from datetime import datetime

# ==========================================
# LÓGICA DE NEGOCIO (El "Cerebro")
# ==========================================

def obtener_precio_dolar():
   """Busca el precio del dólar en la API y lo devuelve."""
   try:
       # Timeout de 5 segundos por si la web está caída
        respuesta = requests.get("https://dolarapi.com/v1/dolares/blue")
        respuesta.raise_for_status() # Verifica si hubo error en la conexión
        datos = respuesta.json()
        return float(datos["venta"])
   except:
       # Si algo falla, devolvemos un valor de referencia
        return 1500.0
        
def calcular_conversión(pesos,precio_dolar):
    """Realiza la cuenta mantemática"""
    return pesos / precio_dolar

def generar_feedback(monto_dolares):
    """Devuelve un mensake según la cantidad de dólares."""
    if monto_dolares > 500:
        return "¡Wow! Estás ahorrando fuerte. ¡Bien ahí!"
    elif monto_dolares > 100:
        return "Es un buen monto para empezar el mes."
    else:
        return "Bueno, de a poco se empieza. ¡A seguir ahorrando!"

# ==========================================
# GESTIÓN DE DATOS (Persistencia)
# ==========================================

def guardar_historial(monto, precio_usado):
    """SOLO escribe en el archivo .txt"""
    ahora = datetime.now() .strftime ("%d/%m/%Y %H:%M")
    línea = f"[{ahora}] - Precio: ${precio_usado} | Compró US${monto:.2f}\n"
    
    with open("historial_dolar.txt", "a", encoding="utf-8") as archivo:
        archivo.write(línea)
        
def actualizar_lista_historial():
    """SOLO lee el archivo y actualiza la lista visual"""
    lista_visual_historial.delete(0, tk.END)
    try:
        with open("historial_dolar.txt", "r", encoding="utf-8") as archivo:
            lineas = archivo.readlines()
            for linea in reversed(lineas):
                lista_visual_historial.insert(tk.END, linea.strip())
    except FileNotFoundError:
        lista_visual_historial.insert(tk.END, "Aún no hay registros.")

# ==========================================
# INTERFAZ DE USUARIO (Terminal)
# ==========================================

procesando = False

def click_boton_calcular(event=None):
    global procesando
    
    if procesando:
        return
    
    entrada = cuadro_entrada.get()
    try:
        monto_pesos = float(entrada)
        if monto_pesos <= 0:
            messagebox.showwarning("Atención", "Poné un monto mayor a cero.")
            return
        
        procesando = True
        boton.config(text="Calculando...", bg="#5a6268", fg="white")
        ventana.update()
        
        precio = obtener_precio_dolar()
        dolares = calcular_conversión(monto_pesos, precio)
        
        etiqueta_resultado.config(text=f"US${dolares:.2f}", fg="#1a73e8")
        etiqueta_feedback.config(text=generar_feedback(dolares))
        
        guardar_historial(dolares, precio)
        actualizar_lista_historial()
        
        boton.config(text="CALCULAR COMPRA", bg="#28a745", fg="white")
        procesando = False
        
    except ValueError:
        messagebox.showerror("Error", f"'{entrada}' no es válido. Usá solo números.")
        boton.config(text="CALCULAR COMPRA", bg="#28a745", fg="white")
        procesando = False

ventana = tk.Tk()
ventana.title("Conversor Dólar Blue Pro")
ventana.geometry("400x500")

cuaderno = ttk.Notebook(ventana)
cuaderno.pack(fill='both', expand=True)

pestana_calc = ttk.Frame (cuaderno)
pestana_hist = ttk.Frame (cuaderno)

cuaderno.add(pestana_calc, text=" Calculadora ")
cuaderno.add(pestana_hist, text=" Historial ")

tk.Label(pestana_calc, text="Conversor Pro", font=("Arial", 16, "bold")).pack(pady=10)
precio_hoy = obtener_precio_dolar()
tk.Label(pestana_calc, text=f"Dólar Blue hoy: ${precio_hoy}", font=("Arial", 10, "italic")).pack()

tk.Label(pestana_calc, text="\n¿Cuántos pesos tenés?", font=("Arial", 11)).pack()
cuadro_entrada = tk.Entry(pestana_calc, font=("Arial", 14), justify="center")
cuadro_entrada.pack(pady=10)
cuadro_entrada.focus()

cuadro_entrada.bind("<Return>", click_boton_calcular)

boton = tk.Button(pestana_calc, text="CALCULAR COMPRA", bg="#28a745", fg="white", font=("Arial", 10, "bold"), padx=10, pady=5, command=click_boton_calcular)
boton.pack(pady=20)

etiqueta_resultado = tk.Label(pestana_calc, text="US$ 0.00", font=("Arial", 20, "italic"), fg="gray")
etiqueta_resultado.pack()

etiqueta_feedback = tk.Label(pestana_calc, text="", font=("Arial", 10, "italic"), fg="gray")
etiqueta_feedback.pack(pady=10)

tk.Label(pestana_hist, text= "Registro de compras", font=("Arial", 12, "bold")).pack(pady=10)
lista_visual_historial = tk.Listbox(pestana_hist, font=("Courier", 9), width=50)
lista_visual_historial.pack(padx=10, pady=10, fill='both', expand=True)

actualizar_lista_historial()

ventana.mainloop()