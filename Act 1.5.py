import ply.lex as lex
import tkinter as tk
from tkinter import scrolledtext
from tabulate import tabulate


# Lista de tokens
tokens = [
    'IDENTIFICADOR',
    'TIPO_DE_DATO',
    'CORCHETE_DE_APERTURA',
    'CORCHETE_DE_CIERRE',
    'PARENTESIS_DE_APERTURA',
    'PARENTESIS_DE_CIERRE',
    'LLAVE_DE_APERTURA',
    'RESERVADA',
    'PUNTO_Y_COMA',
    'OPERADOR_DE_INCREMENTO'
]

# Expresiones regulares para tokens
t_IDENTIFICADOR = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_CORCHETE_DE_APERTURA = r'\['
t_CORCHETE_DE_CIERRE = r'\]'
t_PARENTESIS_DE_APERTURA = r'\('
t_PARENTESIS_DE_CIERRE = r'\)'
t_LLAVE_DE_APERTURA = r'\{'
t_PUNTO_Y_COMA = r';'
t_OPERADOR_DE_INCREMENTO = r'\+\+'

def t_TIPO_DE_DATO(t):
    r'int'
    t.type = 'TIPO_DE_DATO'
    return t

def t_RESERVADA(t):
    r'for'
    t.type = 'RESERVADA'
    return t


# Ignorar espacios y tabulaciones
t_ignore = ' \t'

# Contador de líneas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Función para manejar errores
def t_error(t):
    print("Carácter ilegal '%s'" % t.value[0])
    t.lexer.skip(1)

# Construir el analizador léxico
lexer = lex.lex()

# Función para analizar el texto de entrada
def analizar(texto):
    lexer.input(texto)
    tokens_encontrados = []
    while True:
        tok = lexer.token()
        if not tok:
            break  # No hay más tokens
        tokens_encontrados.append((tok.lineno, tok.type, tok.value))
    return tokens_encontrados

# Función para manejar el evento del botón "Analizar"
def analizar_texto():
    texto_entrada = entrada_texto.get("1.0", tk.END)
    tokens = analizar(texto_entrada)
    texto_salida.delete("1.0", tk.END)
    headers = ["Línea", "Componente léxico", "Lexema"]
    table_data = [(token[0], token[1], token[2]) for token in tokens]
    table = tabulate(table_data, headers=headers, tablefmt="pipe")
    texto_salida.insert(tk.END, table)

# Crear la interfaz gráfica
ventana = tk.Tk()
ventana.title("Analizador Léxico")

frame_entrada = tk.Frame(ventana)
frame_entrada.pack()

etiqueta = tk.Label(frame_entrada, text="Ingrese su código:")
etiqueta.pack()

entrada_texto = scrolledtext.ScrolledText(frame_entrada, height=10, width=50)
entrada_texto.pack()

boton_analizar = tk.Button(frame_entrada, text="Analizar", command=analizar_texto)
boton_analizar.pack()

frame_salida = tk.Frame(ventana)
frame_salida.pack()

etiqueta_resultado = tk.Label(frame_salida, text="Resultado del análisis léxico:")
etiqueta_resultado.pack()

texto_salida = scrolledtext.ScrolledText(frame_salida, height=32, width=70)
texto_salida.pack()

ventana.mainloop()