import tkinter as tk
from tkinter import Canvas, Frame, Label, Entry, Button, messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas as pdf_canvas

# Variables globales
Cadena = ""

# Definir estados y transiciones
states = {
    0: (100, 100), 1: (200, 100), 2: (300, 100), 3: (400, 50),
    4: (400, 150), 5: (500, 100), 6: (600, 100), 7: (700, 100), 8: (800, 100)
}

final_states = {5, 7, 8}  # Conjunto de estados finales
transitions = {
    0: {1: "1"},
    1: {2: "1"},
    2: {3: "1", 4: "0"},
    3: {5: "0"},
    4: {5: "1"},
    5: {6: "1"},
    6: {7: "0"},
    7: {8: "1", 1: "1", 0: "0"},
    8: {0: "1"}
}

# Función para crear círculos (estados)
def create_circle(x, y, r, canvas, color="white"):
    canvas.create_oval(x - r, y - r, x + r, y + r, outline="black", fill=color, width=2)

# Función para crear flechas (transiciones)
def create_arrow(canvas, x1, y1, x2, y2, label):
    canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST, width=2)
    mx, my = (x1 + x2) // 2, (y1 + y2) // 2
    canvas.create_text(mx, my - 10, text=label, font=("Arial", 12))

# Función para dibujar el autómata
def draw_automata(canvas, accepted):
    for state, (x, y) in states.items():
        color = "lightgreen" if state in final_states and accepted else "white"
        create_circle(x, y, 30, canvas, color)
        canvas.create_text(x, y, text=str(state), font=("Arial", 16))

    for s1, edges in transitions.items():
        x1, y1 = states[s1]
        for s2, label in edges.items():
            x2, y2 = states[s2]
            create_arrow(canvas, x1, y1, x2, y2, label)

# Función para procesar la cadena y determinar si es aceptada
def process_string():
    global Cadena
    current_state = 0  # Estado inicial
    for char in Cadena:
        found_transition = False
        for next_state, transition_char in transitions.get(current_state, {}).items():
            if char == transition_char:
                current_state = next_state
                found_transition = True
                break
        if not found_transition:
            messagebox.showerror("Error", "Cadena rechazada: no hay transición válida.")
            return  # No dibujar el autómata si hay un error

    if current_state in final_states:
        result_label.config(text="Cadena aceptada.")
        draw_canvas(True)  # Dibuja el autómata con aceptación verdadera
    else:
        messagebox.showerror("Error", "Cadena rechazada: estado final no alcanzado.")
        return  # No dibujar el autómata si no se alcanza un estado final

    generate_pdf(current_state in final_states)

# Función para crear la interfaz de entrada
def interface():
    global cadena_entry, result_label

    root = tk.Tk()
    root.title("Datos Autómatas")
    
    frame = Frame(root, width=400, height=500)
    frame.pack()
    
    Label(frame, text="AUTOMATA AFD ", fg="blue", font=("arial", 12)).place(x=155, y=40)

    Label(frame, text="Cadena a analizar", fg="black", font=("arial", 12)).place(x=60, y=100)
    cadena_entry = Entry(frame, font=("consolas", 14), width=25)
    cadena_entry.place(x=60, y=130)

    analizar_button = Button(frame, text="Analizar el Autómata", fg="white", bg="black", font=("arial", 14), width=22, height=1, command=get_input_data)
    analizar_button.place(x=60, y=170)

    result_label = Label(frame, text="", fg="black", font=("arial", 12))
    result_label.place(x=60, y=220)

    root.mainloop()

# Función para recoger datos de la interfaz
def get_input_data():
    global Cadena
    Cadena = cadena_entry.get()
    print("Cadena ingresada:", Cadena)
    process_string()

# Función para dibujar el autómata en un nuevo canvas
def draw_canvas(accepted):
    draw_root = tk.Tk()
    draw_root.title("AFD - Autómata Finito Determinista")

    draw_canvas = Canvas(draw_root, width=900, height=400, bg="white")
    draw_canvas.pack()

    draw_automata(draw_canvas, accepted)

    draw_root.mainloop()

# Función para generar PDF
def generate_pdf(accepted):
    pdf_filename = "Automatas.pdf"
    c = pdf_canvas.Canvas(pdf_filename, pagesize=letter)
    width, height = letter

    # Título
    c.drawString(100, height - 50, "Reporte del Autómata Finito Determinista")
    c.drawString(100, height - 80, "Cadena Analizada: " + Cadena)
    c.drawString(100, height - 100, "Resultado: " + ("Aceptada" if accepted else "Rechazada"))

   

    # Tabla de transiciones
    c.drawString(100, height - 130, "Tabla de Transiciones:")
    y = height - 150
    for state, edges in transitions.items():
        for next_state, label in edges.items():
            c.drawString(100, y, f"Desde estado {state} con '{label}' a estado {next_state}")
            y -= 20

     # Incluir la imagen del autómata
    c.drawImage("img.jpg", 300, height - 400, width=300, height=200)
    c.drawImage("automata.jpg", 100, height - 700, width=400, height=300)
    # Guardar el PDF
    c.save()
    print(f"PDF guardado como {pdf_filename}")


# Iniciar la interfaz
interface()
