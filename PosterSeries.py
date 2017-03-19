import Tkinter as tk
from PIL import Image, ImageTk
import os
from tkFileDialog import askdirectory
from tkMessageBox import showinfo
from pytvmaze import get_show_list
from time import sleep
import urllib


i = 0
nuevas = []
imagenes = []
api_key = "7ec7b6f27dd346adf0c438b41f500cd8"
fanartv = "http://webservice.fanart.tv/v3/tv/"


def buscardir():  # --- cuando Busco el directorio de mis Series
    global i
    i = 0
    Raiz = askdirectory()
    Raiz = Raiz + "/"
    print(Raiz + " Ok")
    BarraEstado.config(text=Raiz)
    Variablestring.set(Raiz)
    Boton_Buscar.config(state='normal')
    Boton_Comenzar.config(state='disabled')
    Boton_Cont.config(state='disabled')


def Vacerca():  # --- Ventana que se abre al seleccionar del menu ACERCA
    showinfo("Acerca", "POSTERSERIES v.0.1")


def Disco_serie():
    Raiz = Variablestring.get()
    if Raiz == "":
        print("VACIO")
    else:
        print('Buscando series en: ') + Raiz
        Listado_Series.delete(0, 'end')
        for nombre_serie in os.listdir(Raiz):
            path1 = os.path.join(Raiz, nombre_serie)
            if os.path.isdir(path1):
                print(path1)
                Listado_Series.insert('end', nombre_serie)
                Mven.update()
                sleep(0.1)
                Boton_Comenzar.config(state='normal')


def Seguir():
    global i
    Raiz = Variablestring.get()
    if Raiz == "":
        print("SIGUE VACIO")
    else:
        if Listado_Series.size() <= i + 1:
            Boton_Comenzar.config(state='disabled')
        if Listado_Series.get(i) is None:
            print("mayor")
        Boton_Buscar.config(state='disabled')
        Boton_Cont.config(state='normal')
        print(Listado_Series.get(0, 'end'))
        Nombre_carpeta_serie = Listado_Series.get(i)
        SerieElegida.set(Nombre_carpeta_serie)
        Mven.update()
        BarraEstado.config(text="Buscando " + SerieElegida.get())
        i = i + 1
        Buscar_tvbd(Nombre_carpeta_serie)


def Buscar_tvbd(nombre):
    hasta = len(nuevas)
    if hasta != 0:
        del imagenes[:]
        del nuevas[:]
    Listado_encontrado.delete(0, 'end')
    Listado_tv = get_show_list(nombre)
    for show_encontrado in Listado_tv:
        #        print(show_encontrado, show_encontrado.externals['thetvdb'])
        tbdbexiste = show_encontrado.externals['thetvdb']
        print (tbdbexiste)
        if tbdbexiste is not None:
            nuevas.append(show_encontrado.externals)
            imagenes.append(show_encontrado.image)
            Listado_encontrado.insert('end', show_encontrado)
            Mven.update()
            sleep(0.1)
        # print(nuevas)
    if len(nuevas) == 1:
        Bajar_tv_ya(nuevas)


def Bajar_tv_ya(ya):
    print(ya[0])
    indice = Listado_encontrado.index(0)
    nombre1 = Listado_encontrado.get(Listado_encontrado.index(0))
    # -- verificar si el nombre se puede escribir en la carpeta
    # retirar caracteres \ / ? : * " > < | -- #
    nombre = caracteres(nombre1)
    anterior_nombre = SerieElegida.get()
    Raiz = Variablestring.get()
    os.rename(Raiz + "/" + anterior_nombre, Raiz + "/" + nombre)
    print(nuevas[indice])
    L_a = Listado_Series.get('end')
    if L_a != anterior_nombre:
        Seguir()
    else:
        Frenarapp()

# -- cuando apreto el OK, viene a procesar el seleccionado aca ---#


def Bajar_tv():
    global nuevas
    if Listado_encontrado.curselection() != ():
        indice = Listado_encontrado.index(Listado_encontrado.curselection())
        nombre1 = Listado_encontrado.get(Listado_encontrado.curselection())
    # -- verificar si el nombre se puede escribir en la carpeta
    # retirar caracteres \ / ? : * " > < | -- #
        nombre = caracteres(nombre1)
        anterior_nombre = SerieElegida.get()
        Raiz = Variablestring.get()
        # renombro el directorio para que sea igual a la serie
        os.rename(Raiz + "/" + anterior_nombre, Raiz + "/" + nombre)
        # busca la caratula --#
        tvdb = (nuevas[indice])
        Buscar_fanart(tvdb, nombre)
        L_a = Listado_Series.get('end')
        if L_a != anterior_nombre:
            Seguir()
        else:
            Frenarapp()

# --- descarga los archivos json de fanarttv para despues procesarlos ---#


def Buscar_fanart(tvdb, nombre):
    print str(tvdb['thetvdb'])
    jsontvdb = str(tvdb['thetvdb'])
    direccion = fanartv + jsontvdb + "?api_key=" + api_key
    urllib.urlretrieve(direccion, nombre + ".json")
    print("baje json " + nombre)
# --- Cuando termine de ver todos los directorios ---#


def Frenarapp():
    print("fin")
    Listado_Series.delete(0, 'end')
    Listado_encontrado.delete(0, 'end')
    SerieElegida.set("")
    BarraEstado.config(text="OK")
    Variablestring.set("")


def Imagen_ver():
    global imagenes
    if Listado_encontrado.curselection() != ():
        indice = Listado_encontrado.index(Listado_encontrado.curselection())
        img = str(imagenes[indice]['medium'])
        print("bajo imagen")
        print(img)
        urllib.urlretrieve(img, "1.jpg")
        ima = Image.open("1.jpg")
        tkimagenes = ImageTk.PhotoImage(ima)
        logo.config(image=tkimagenes)
        logo.image = tkimagenes
        Mven.update()


def caracteres(azul):
    # -- ver esto para cambiar caracteres de las carpetas
    # que no se pueden escribir -- #
    nom_serie = azul.translate(None, "\,/,?,:,*,>,<,|")
    print nom_serie
    return nom_serie


# --- Ventana Principal ---#

Mven = tk.Tk()


Mven.geometry("690x440")
Mven.title('POSTERSERIES')
menu = tk.Menu(Mven)
Mven.config(menu=menu)

ArchivoMenu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Archivo", menu=ArchivoMenu)
ArchivoMenu.add_command(label="Series en Disco...", command=buscardir)
ArchivoMenu.add_separator()
ArchivoMenu.add_command(label="Quitar", command=Mven.quit)
AyudaMenu = tk.Menu(menu)
menu.add_cascade(label="Ayuda", menu=AyudaMenu)
AyudaMenu.add_command(label="Acerca de...", command=Vacerca)

# frame contiene boton buscar y label raiz
Frame_superior = tk.Frame(Mven)

# frame contiene los listbox y botones
Frame_Medio = tk.Frame(Mven)

# --- Boton para comenzar la Busqueda ---#
Boton_Buscar = tk.Button(
    Frame_superior, text="Buscar en..", command=Disco_serie)
Boton_Buscar.pack(side='left', anchor='w')

# --- Donde estoy buscando ---#

Variablestring = tk.StringVar()
Raiz_Buscada = tk.Label(
    Frame_superior, textvariable=Variablestring, padx=5, pady=10)
Raiz_Buscada.pack(side='left', anchor='ne')

# --- Listado Series en Disco ---#
Listado_Series = tk.Listbox(
    Frame_Medio, selectmode='single', height=25, width=25)
Listado_Series.pack(side='left', anchor='nw')

Boton_Comenzar = tk.Button(Frame_Medio, text=">>", command=Seguir)
Boton_Comenzar.pack(side='left', anchor='n', fill='y', padx=2)

SerieElegida = tk.StringVar()
Serie_Buscada = tk.Label(
    Frame_Medio, textvariable=SerieElegida, padx=5, pady=5)
Serie_Buscada.pack(side='top', anchor='nw')

# --- Listado Series en Disco ---#
Listado_encontrado = tk.Listbox(
    Frame_Medio, selectmode='single', height=23, width=25)
Listado_encontrado.pack(side='left', anchor='nw')

Boton_Cont = tk.Button(Frame_Medio, text="Bajar", command=Bajar_tv)
Boton_Cont.pack(side='top', anchor='ne', fill='x', padx=2)
# --- las temporadas ---#

Boton_ver = tk.Button(Frame_Medio, text="PreVer", command=Imagen_ver)
Boton_ver.pack(side='top', anchor='ne', fill='x', padx=2)
# --- Donde estoy buscando ---#

# ---- Barra de Estado ---#
BarraEstado = tk.Label(Mven, text="Ok", bd=1, relief='sunken', anchor='w')
BarraEstado.pack(side='bottom', fill='x')

ima = Image.open("img/inicio.jpg")
tkimagenes = ImageTk.PhotoImage(ima)
logo = tk.Label(Frame_Medio, image=tkimagenes)
logo.image = tkimagenes
logo.pack(side='right', anchor='ne', padx=2)

# ubicaciones de los widget
Frame_superior.pack(side='top', anchor='w', padx=5)
Frame_Medio.pack(side='top', anchor='w', fill='x', padx=5)

Mven.mainloop()
