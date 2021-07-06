import grammar
import os
import tkinter
from tkinter import ttk
from tkinter import Menu
from tkinter import filedialog
from tkinter import scrolledtext
from tkinter import Frame
from tkinter import Canvas
from tkinter import Scrollbar
import re
raiz = tkinter.Tk()

def salir(): #SALIR DEL PROGRAMA
    value = messagebox.askokcancel("Salir", "Está seguro que desea salir?")
    if value :
        raiz.destroy()

def cerrarDoc(): # CERRAR UN DOCUMENTO
    value = messagebox.askretrycancel("Reintentar", "No es posible cerrar el documento.")
    if value == False:
        raiz.destroy()

archivo = ""   #PATH DEL ARCHIVO EN MEMORIA

def nuevo():   #NUEVO ARCHIVO
    global archivo
    editor.delete("1.0", tkinter.END)
    archivo = ""

def abrir():       #ABRIR ARCHIVO
    global archivo
    archivo = filedialog.askopenfilename(title = "Abrir Archivo", initialdir = "C:/")

    entrada = open(archivo, "r",encoding="UTF-8")
    content = entrada.read()

    editor.delete(1.0, tkinter.END)
    for s in recorrerInput(content):
        editor.insert(tkinter.INSERT, s[1], s[0])
    entrada.close()
    lineas()

def guardarArchivo():   #GUARDAR 
    global archivo
    if archivo == "":
        guardarComo()
    else:
        guardarc = open(archivo, "w",encoding="UTF-8")
        guardarc.write(editor.get(1.0, tkinter.END))
        guardarc.close()

def guardarComo():      #GUARDAR COMO
    global archivo
    guardar = filedialog.asksaveasfilename(defaultextension=".jpr",title = "Guardar Archivo", initialdir = "C:/",filetypes=[
                    ("Text Files", "*.jpr")
                ])
    fguardar = open(guardar, "w+",encoding="UTF-8")
    fguardar.write(editor.get("1.0", tkinter.END))
    fguardar.close()
    archivo = guardar

def openPDF(name):      #ABRIRI UN PDF
    dirname = os.path.dirname(__file__)
    direcc = os.path.join(dirname, name)
    os.startfile(direcc)

def lineas(*args):      #ACTUALIZAR LINEAS
    lines.delete("all")
    
    cont = editor.index("@1,0")
    while True :
        dline= editor.dlineinfo(cont)
        if dline is None: 
            break
        y = dline[1]
        strline = str(cont).split(".")[0]
        
        lines.create_text(2,y,anchor="nw", text=strline, font = ("Arial", 10))
        cont = editor.index("%s+1line" % cont)
        posicionCursor = editor.index(tkinter.INSERT)
        pos = ttk.Label(scrollable_frame,text= posicionCursor)
        pos.grid(column = 1,row=1)
        pos.config(text=str(posicionCursor).replace(".",","))
    

def posicion(event):    #ACTUALIZAR POSICION
    #pos.config(text = "[" + str(editor.index(tkinter.INSERT)).replace(".",",") + "]" )
    posicionCursor = editor.index(tkinter.END)
    pos = ttk.Label(scrollable_frame,text= posicionCursor)
    pos.grid(column = 1,row=1)
    pos.config(text=str(posicionCursor).replace(".",","))



def recorrerInput(i):  #Funcion para obtener palabrvas reservadas, signos, numeros, etc
    lista = []
    val = ''
    counter = 0
    while counter < len(i):
        if re.search(r"[0-9]", i[counter]):
            val += i[counter]
        
        elif i[counter] == "$":
            if len(val) != 0:
                l = []
                l.append("variable")
                l.append(val)
                lista.append(l)
                val = ''
            val = "$"
        elif i[counter] == "<" or i[counter] == ">" or i[counter] == "+" or i[counter] == "-" or i[counter] == "*" or i[counter] == "/" or i[counter] == "=" or i[counter] == "!" or i[counter] == "~" or i[counter] == "%" or i[counter] == "^" or i[counter] == "|":
            if len(val) != 0:
                l = []
                l.append("variable")
                l.append(val)
                lista.append(l)
                val = ''
            l = []
            l.append("operacion")
            l.append(i[counter])
            lista.append(l)
        elif i[counter] == "\"":
            if len(val) != 0:
                l = []
                l.append("variable")
                l.append(val)
                lista.append(l)
                val = ''
            val = i[counter]
            counter += 1
            while counter < len(i):
                if i[counter] == "\"":
                    val += i[counter]
                    l = []
                    l.append("string")
                    l.append(val)
                    lista.append(l)
                    val = ''
                    break
                val += i[counter]
                counter += 1
        elif i[counter] == "#":
            if len(val) != 0:
                l = []
                l.append("variable")
                l.append(val)
                lista.append(l)
                val = ''
            val = i[counter]
            counter += 1
            multilinea = True
            while counter < len(i):
                
                if i[counter] == "*":
                    multilinea = False
                if multilinea:
                    if i[counter] == "\n":
                        val += i[counter]
                        l = []
                        l.append("comentario")
                        l.append(val)
                        lista.append(l)
                        val = ''
                        break
                else:
                    if i[counter] == "#":
                        val += i[counter]
                        l = []
                        l.append("comentario")
                        l.append(val)
                        lista.append(l)
                        val = ''
                        break
                
                val += i[counter]
                counter += 1
        elif i[counter] == "\'":
            if len(val) != 0:
                l = []
                l.append("variable")
                l.append(val)
                lista.append(l)
                val = ''
            val = i[counter]
            counter += 1
            while counter < len(i):
                if i[counter] == "\'":
                    val += i[counter]
                    l = []
                    l.append("string")
                    l.append(val)
                    lista.append(l)
                    val = ''
                    break
                val += i[counter]
                counter += 1
        else:
            if len(val) != 0:
                l = []
                l.append("variable")
                l.append(val)
                lista.append(l)
                val = ''
            l = []
            l.append("signo")
            l.append(i[counter])
            lista.append(l)
        counter +=1
    for s in lista:
        if s[1].lower() == 'var' or s[1] == 'float' or s[1] == 'char' or s[1] == 'print' or s[1] == 'main' or s[1] == 'goto' or s[1] == 'unset' or s[1] == 'exit' or s[1] == 'if' or s[1] == 'abs' or s[1] == 'xor' or s[1] == 'array' or s[1] == 'read':
            s[0] = 'reservada'
        elif s[1][0] != "$":
            if s[0] == 'variable':
                s[0] = 'etiqueta'
    return lista



#ELEMENTOS

frame = Frame(raiz, bg="gray60")
canvas = Canvas(frame, bg="gray60")
scrollbar = Scrollbar(frame, orient="vertical", command=canvas.yview)
scrollbar2 = Scrollbar(frame, orient="horizontal", command=canvas.xview)
scrollable_frame = Frame(canvas, bg="gray60")

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

canvas.configure(xscrollcommand=scrollbar2.set, yscrollcommand=scrollbar.set, width = 1250, height = 700)

cont = 0

pos = ttk.Label(scrollable_frame, text = str(cont))
pos.grid(column = 1, row = 1)
editor = scrolledtext.ScrolledText(scrollable_frame, undo = True, width = 60, height = 19)
consola = scrolledtext.ScrolledText(scrollable_frame,background = 'black', foreground = "white",undo = True, width = 60, height = 19)
lines = Canvas(scrollable_frame, width = 30, height = 300, background = 'gray60')

#CAMBIO DE COLORES
editor.tag_config('reservada', foreground='blue')
editor.tag_config('variable', foreground='maroon4')
editor.tag_config('string', foreground='orange')
editor.tag_config('comentario', foreground='gray')
editor.tag_config('operacion', foreground='green')
editor.tag_config('etiqueta', foreground='purple')

# FUNCIONALIDADES EN EL TECLADO

editor.grid(column = 1, row = 3, pady = 25, padx = 0)
consola.grid(column = 2, row = 3, pady = 25, padx = 30,)
lines.grid(column = 0, row = 3)

editor.bind('<Return>', lineas)
editor.bind('<BackSpace>', lineas)
editor.bind('<<Change>>', lineas)
editor.bind('<Configure>', lineas)
editor.bind('<KeyPress>', lineas)
editor.bind('<Button-1>', posicion)

def changs():
    content = editor.get("1.0", tkinter.END)

    editor.delete(1.0, tkinter.END)
    for s in recorrerInput(content):
        editor.insert(tkinter.INSERT, s[1], s[0])
    
html = ""
def analizar():
    content = editor.get("1.0", tkinter.END)
    ast = grammar.ejecutar(content,raiz,consola)
    consola.delete(1.0, tkinter.END)
    consola.insert(tkinter.INSERT, ast.getConsola())
    print(ast.getConsola())
    html = """<!DOCTYPE html>
<html>
<body>

<h2>Errores</h2>

<table style="width:100%">
  <tr>
    <th>Tipo</th>
    <th>Descripcion</th> 
    <th>Linea</th>
    <th>Columna</th>
  </tr>
"""
    for error in ast.getExcepciones():                   # CAPTURA DE ERRORES LEXICOS Y SINTACTICOS
        html += "<tr><td>"+error.tipo+"</td><td>"+error.descripcion+"</td><td>"+str(error.fila)+"</td><td>"+str(error.columna)+"</td></tr>"
    
    html+= """</table>

</body>
</html>"""
    html2 = """<!DOCTYPE html>
<html>
<body>

<h2>Tabla de simbolos</h2>

<table style="width:100%">
  <tr>
    <th>Identificador</th>
    <th>Ambito</th> 
    <th>Valor</th>
    <th>Tipo</th>
    <th>Columna</th>
    <th>Linea</th>
  </tr>
"""
    print(len(ast.reporteSimbolo))
    for error in ast.reporteSimbolo:                   # CAPTURA DE ERRORES LEXICOS Y SINTACTICOS
        tipo = error.getTipo()
        if error.arreglo:
            tipo += "->Arreglo"
        html2 += "<tr><td>"+error.getID()+"</td><td>"+error.getAmbito()+"</td><td>"+str(error.getValor())+"</td><td>"+str(tipo)+"</td><td>"+str(error.getColumna())+"</td><td>"+str(error.getFila())+"</td></tr>"
    
    html2+= """</table>

</body>
</html>"""
    dirname = os.path.dirname(__file__)
    direcc = os.path.join(dirname, 'ast.dot')
    arch = open(direcc, "w+")
    arch.write(ast.dot)
    arch.close()
    os.system('dot -T pdf -o ast.pdf ast.dot')
    openPDF(os.path.join(dirname,'ast.pdf'))
    fguardar = open("./errores.html", "w+",encoding="UTF-8")
    fguardar.write(html)
    fguardar.close()
    openPDF("./errores.html")
    fguardar = open("./simbolos.html", "w+",encoding="UTF-8")
    fguardar.write(html2)
    fguardar.close()
    openPDF("./simbolos.html")
    



B = tkinter.Button(scrollable_frame, text ="Ejecutar", command = analizar)
B.grid(row=5,column=1)

frame.grid(sticky='news')
canvas.grid(row=0,column=1)
scrollbar.grid(row=0, column=2, sticky='ns')
scrollbar2.grid(row=1, column=1, sticky='ns')

my_menu = Menu(raiz)
raiz.config(menu=my_menu)

# Add File Menu
file_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New" ,command=nuevo)
file_menu.add_command(label="Open", command=abrir)
file_menu.add_command(label="Save", command=guardarArchivo)
file_menu.add_command(label="Save As...",command=guardarComo)
file_menu.add_separator()
file_menu.add_command(label="Print File", command=changs)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=raiz.quit)

raiz.mainloop()