

# #!/usr/bin/python
# # -*- coding: utf-8 -*-
 
# # Ejemplo cliente - servidor en python
# # Programa Servidor
# # www.elfreneticoinformatico.com


# #Importacines:
# import socket #utilidades de red y conexion



# #Definimos parámetros necesarios por defeccto
# ip = "0.0.0.0"
# puerto = 8000
# dataConection = (ip, puerto)
# conexionesMaximas = 5 #Podrán conectarse 5 clientes como máximo

# #Creamos el servidor.
# #socket.AF_INET para indicar que utilizaremos Ipv4
# #socket.SOCK_STREAM para utilizar TCP/IP (no udp)
# socketServidor = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# socketServidor.bind(dataConection) #Asignamos los valores del servidor
# socketServidor.listen(conexionesMaximas) #Asignamos el número máximo de conexiones

# print("Esperando conexiones en %s:%s" %(ip, puerto))
# cliente, direccion = socketServidor.accept()
# print("Conexion establecida con %s:%s" %(direccion[0], direccion[1]))

# #Bucle de escucha. En él indicamos la forma de actuar al recibir las tramas del cliente
# while True:
#     datos = cliente.recv(1024) #El número indica el número maximo de bytes
    
    
#     if datos == "exit".encode("utf-8"):
#         cliente.send("exit".encode("utf-8"))
#         break
#     print("RECIBIDO: %s" %datos)
#     cliente.sendall(("-- Recibido --".encode("utf-8")))

# print("------- CONEXIÓN CERRADA ---------")
# socketServidor.close()

import Pyro.core
import Pyro.naming
import comp_trig

class calculo(Pyro.core.ObjBase, comp_trig.funciones):
    def __init__(self):
        Pyro.core.ObjBase.__init__(self)

Pyro.core.initServer()
ns = Pyro.naming.NameServerLocator().getNS()
daemon = Pyro.core.Daemon()
daemon.useNameServer(ns)
uri = daemon.connect(calculo(),"cluster")
print "El Servidor esta preparado"
daemon.requestLoop()
