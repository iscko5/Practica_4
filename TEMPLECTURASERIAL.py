# Automatizanos.com, 02/2016
# Basado en el codigo de Andreas Boesch, 04/2013 
# Mostrar valores numericos ( enviados como cadenas ASCII ) desde un dispositivo externo por un puerto serial
# La aplicacion envia un byte al dispositivo y muestra la respuesta tambien en forma de grafico de barra
 
# importar paquetes
import Tkinter as tk    	# para la interfaz grafica
import ttk              			# para widgets de la interfaz grafica
import tkMessageBox     	# Para cuadro de mensaje
import serial           		# para la comunicacion por puerto serial
import time             		# para los temporizadores
import threading        		# para realizacion de procesos en paralelo (hilos)
 
 # El proceso (hilo) que continuamente hara peticiones por el puerto serial al dispositivo externo
class myThread (threading.Thread):
    # inicializar la  clase
    def __init__(self, name, ser):
        threading.Thread.__init__(self)
        # Nombre del proceso (hilo)
        self.name = name
        # Informacion del puerto serial
        self.ser  = ser
	# la cadena que se recibira
	self.rcvstr=''
	# la cadena que se mostrara
	self.prnstr=''
 
    # Esto es llamado cuando el proceso (hilo) es iniciado con .start()
    def run(self):
        # contador de cada una de las lecturas
        self.conteo_datos = 0
        while self.ser.isOpen():

		# incrementar el contador ...
		self.conteo_datos += 1
		# asignar el valor de la variable que sera mostrada en la interfaz grafica
		conteoLecturas.set("conteos lectura: "+str(self.conteo_datos))

		# Enviando el comando (byte) al dispositivo serial
            
		try:
			# enviando comando
			self.ser.write("a")
			# esperar a que el dispositivo conteste
			time.sleep(0.1)
			# crear una cadena para los datos recibidos
			rcvstr = ''
			# Si hay algun dato disponible en el puerto serial, leerlo
			while self.ser.inWaiting() > 0:				
				self.rcvstr= self.ser.read(self.ser.inWaiting())
		except:
				# no hacer nada si el comando no se puede enviar
			pass
 
		# Asignando las variables de la interfaz grafica con la respuesta recibida

		self.prnstr=self.rcvstr.rstrip('\n')
		self.prnstr = self.prnstr +"  C"
		etiquetaVariable.set(self.prnstr)
				
		
		try:
			valorVariable.set(float(self.rcvstr)+ offsetBarra )
 		except:
			# No hacer nada en caso que la conversion falle por una cadena mal formateada
			pass

		# Tiempo en segundos entre peticiones de dato
		time.sleep(0.5)
             
             
 
# procedimiento de salida
def mSalir():
    # Preguntar si/no a la confirmacion de salida
    mExit = tkMessageBox.askyesno(title = "Salir", message = "Realmente desea salir?")
    if mExit > 0:
        # cerrar el puerto
        ser.close()
        # destruir la interfaz grafica
        root.destroy()
        return
 
# Enviar comandos por el puerto serial al dispositivo
def mSend(command):
    try:
        ser.write(command)
    except:
        print "No se puede enviar comando puerto cerrado?"
      
    return
 

         
# ===========================
# Inicio del programa principal
# ===========================
 
# provee informacion del puerto serial
ser = serial.Serial()

ser.port = '/dev/ttyUSB0'
#ser.port = 'COM6'
ser.baudrate = 9600
ser.timeout = 0
# abrir el puerto si este aun no se encuentra abierto
if ser.isOpen() == False:
    ser.open()
 
# inicializar la ventana principal
root = tk.Tk()
root.configure(background='black')
root.geometry("400x400")
root.title("Lectura variable dispositivo serial ")
 
# variables. Modificar maximo y minimo de barra dependiendo de la variable
etiquetaVariable	= tk.StringVar()
conteoLecturas	= tk.StringVar()
valorVariable		= tk.DoubleVar()
maximoBarra		= 150.0
minimoBarra		= -50.0
rangoBarra		= tk.DoubleVar()
offsetBarra		= tk.DoubleVar()

# Texot, titulos, etc

textoTitulo    				= ttk.Label(root, text = "LECTURA VARIABLE DISPOSITIVO SERIAL", foreground="white",background="black").grid(row=0, column=1)
textoPuerto   				= ttk.Label(root, text = "Puerto serial abierto: "+str(ser.isOpen()), foreground="white",background="black").grid(row=1, column=1)
textoNombrevariable 	= ttk.Label(root, text = "TEMPERATURA", foreground="white",background="black").grid(row=3, column=1)
textoConteolecturas		= ttk.Label(root,textvariable = conteoLecturas, foreground="white",background="black").grid(row=2,column=1)
textoValorvariable		= ttk.Label(root, textvariable = etiquetaVariable, foreground="yellow", background="black" ).grid(row=5, column=2)
textoPiedepagina		= ttk.Label(root, text = "Automatizanos.com", foreground="grey",background="black").grid(row=7, column=1)

# Boton de salir

botonSalir		= ttk.Button(root, text = "cerrar puerto y salir", command = mSalir).grid(row=6, column=1)

#Barra de progreso

if maximoBarra > 0.0 and minimoBarra >= 0.0 :
	rangoBarra = maximoBarra - minimoBarra
	offsetBarra = (-1) * minimoBarra 

if maximoBarra > 0.0 and minimoBarra < 0.0 :
	rangoBarra = maximoBarra  +abs(minimoBarra)
	offsetBarra = abs(minimoBarra) 

if maximoBarra < 0.0 and minimoBarra < 0.0 :
	rangoBarra = abs(minimoBarra) - abs(maximoBarra)
	offsetBarra = abs(minimoBarra) 

s = ttk.Style()
s.theme_use('clam')
s.configure("yellow.Vertical.TProgressbar", foreground='yellow', background='yellow')
progBar = 	ttk.Progressbar(root, orient="vertical",length=200, mode="determinate",maximum=rangoBarra,variable=valorVariable,style="yellow.Vertical.TProgressbar" ).grid(row=5,column=1)


# esperar
time.sleep(1)
# llamar e iniciar el proceso (hilo) de actualizacion de datos
thread1 = myThread("Actualizando", ser)
thread1.start()
 
# iniciar la interfaz grafica
root.mainloop()