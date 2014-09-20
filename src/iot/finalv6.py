# -*- coding: utf-8 -*-
# Universidad del Valle de Guatemala
# Angel Basegoda 13256
# Erick  Hernández Woc 13197
# Johnny del Cid  13032
# Sergio Cancinos 13062
# final.py 
# El programa utiliza el sensor PIR para mandar mensajes a twitter cada vez que el sensor indique que hubo movimiento. 
# Permite que solamente se manden dos tweets y en el tweet manda el número de prueba y la hora actual con el reloj del raspberry. 
#  Solamente se permiten mandar estos tweets al en un intervalo definido de tiempo en minutos y en horas de tiempo real
# Se tiene un sensor de fuerza el cual manda la lectura de cuanta comida hace falta en el recipiente. 


#!/usr/bin/python
#!/usr/bin/env python

#se importan todas las librerias necesarias
import tweepy
import RPi.GPIO as GPIO
import time
from time import strftime
from datetime import datetime
import RPi.GPIO as GPIO, time, os
DEBUG=1
GPIO.setmode(GPIO.BOARD)

#Informacion para conectarse con la app
CONSUMER_KEY = 'IGrdYa7WN7CdUcRkGM9JayCe4'
CONSUMER_SECRET = 'qbqStO71i91BCOPFUXMKx3mhwC1Xatk3GnlwM1Yp1b7QeV3uZc'
ACCESS_KEY = '2817354110-u5tRa5y92pdAegtemBfaUAVduQI6bWwr3DOaG9d'
ACCESS_SECRET = '1NzC3X3iqm6HXBH5st2zqukFHlbpPLsKlbEuFyO0SBUgj'
#En esta parte nos identifica para poder realizar operaciones
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
#update_status('mensaje' o variable) es para actualizar nuestro estado
x = tweepy.API(auth)

## inicializacion de servo

GPIO.setup(7,GPIO.OUT)

p= GPIO.PWM(7,50)

p.start(7.5)

# Use BCM GPIO references
# instead of physical pin numbers
## PIR
GPIO.setmode(GPIO.BCM)
cont = 0
 
# se define el GPIO a utilizar
GPIO_PIR = 7

# se define el pin como salida
GPIO.setup(GPIO_PIR,GPIO.IN)
 
Current_State  = 0
Previous_State = 0
timeMin2 = 99
timeMin = 0
a = 0

## se define el metodo para obtener la cantidad de peso leido
def RCtime (RCpin):
    reading=0
    
    GPIO.setup(RCpin, GPIO.OUT)

    GPIO.output(RCpin, GPIO.LOW)

    time.sleep(0.1)


    GPIO.setup(RCpin, GPIO.IN)

    while (GPIO.input(RCpin) == GPIO.LOW):
        reading += 1
    return reading/1000

## se crea la clase y sus respectivos metodos para obtener la hora de la raspberry
class raspberryDateTime:

## se obtienen el tiempo real, los minutos y las horas en los formatos respectivos    
    def get_time(self):
        time = datetime.now().strftime('%H:%M:%S')
        return time

    def get_min(self):
        mins = datetime.now().strftime('%M')
        return int(mins)

    def get_hor(self):
        hora = datetime.now().strftime('%H')
        return int(hora)

## se crea un objeto de esa clase
dateTime = raspberryDateTime()

try:
 
  print "Waiting for PIR to settle ..."

## se espera la activacion del PIR 
  while GPIO.input(GPIO_PIR)==1:
    Current_State  = 0
 
  print "  Ready"
  p.ChangeDutyCycle(7.5)#neutro
 
  while True :
    
## se obtiene el tiempo real
    tReal= dateTime.get_time()
    timeHor = dateTime.get_hor()

## se define la condicion para que solamente sirva a ciertas horas del dia
    if (timeHor >= 14 and timeHor < 17) or (timeHor >= 12 and timeHor < 14) or (timeHor >= 19 and timeHor < 20):
        # Read PIR state
        Current_State = GPIO.input(GPIO_PIR)
     
        if Current_State==1 and Previous_State==0:
          # PIR is triggered
          print "  Motion detected!"
    ##se cuenta cuantas veces se le sirve comida
    ##siendo un maximo de 2 veces

          
##          REGRESAR EL CONTADOR A 1 LUEGO DE LAS PRUEBAS ££££££££££££££££££££££££££££££££££££££££££££££££££££££

          
          if cont <= 30:
            a += 10

## se obtiene el minuto al cual se sirve por primera vez el alimento
            if cont == 0:
              timeMin = dateTime.get_min()
            timeDif = timeMin2 - timeMin
## se obtiene el segundo minuto al cual se activa el sensor
## si la diferencia entre los dos minutos es menor a 20, no se sirve comida           
            timeMin2 = dateTime.get_min()
            if timeDif >= 0:
              cont = cont + 1
              timeDif = time
              p.ChangeDutyCycle(12.5)#180

## se despliega el mensaje respectivo dependiendo de la cantidad de alimento restante              
              if a < 75:
                  msg = "Bastante alimento restante."
              if a >= 75 and a < 150:
                  msg = "Suficiente alimento restante."
              if a >= 150 and a < 225:
                  msg = "Bajo nivel de alimento restante."
              if a >= 225 and a < 300:
                  msg = "Muy bajo nivel de alimento restante."
              if a >= 300:
                  msg = "Sin alimento restante."

              time.sleep(3)#tiempo que se servira el alimento
              # se envia el tweet
              x.update_status('Prueba #'+str(cont)+" at "+str(tReal)+". "+msg)
              p.ChangeDutyCycle(7.5)#neutro
          Previous_State=1
        elif Current_State==0 and Previous_State==1:
          print "  Ready"
          Previous_State=0
     
        time.sleep(0.01)

#se termina el proceso cuando se presiona CTRL + C
except KeyboardInterrupt:
  GPIO.cleanup()
