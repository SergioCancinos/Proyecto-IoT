#!/usr/bin/python
# Universidad del Valle de Guatemala
# Angel Basegoda 13256
# Erick  Hernández Woc 13197
# Johnny del Cid  13032
# Sergio Cancinos 13062
# final.py 
# El programa utiliza el sensor PIR para mandar mensajes a twitter cada vez que el sensor indique que hubo movimiento. 
# Permite que solamente se manden dos tweets y en el tweet manda el número de prueba y la hora actual con el reloj del raspberry. 
#     Solamente se permiten mandar estos tweets al en un intervalo definido de tiempo en minutos no en horas.
#     FALTAN LOS HORARIOS DE COMIDA


# Author : Matt Hawkins
# Date   : 21/01/2013
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tweepy
# Import required Python libraries
import RPi.GPIO as GPIO
import time
from time import strftime
from datetime import datetime

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

# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)
cont = 0
 
# Define GPIO to use on Pi
GPIO_PIR = 7
 
print "PIR Module Test (CTRL-C to exit)"
 
# Set pin as input
GPIO.setup(GPIO_PIR,GPIO.IN)      # Echo
 
Current_State  = 0
Previous_State = 0
timeMin2 = 99
timeMin = 0

class raspberryDateTime:
    
    def get_time(self):
        time = datetime.now().strftime('%H:%M:%S')
        # In time string we store the time in format Hours:Minutes:Seconds
        return time

    def get_min(self):
        mins = datetime.now().strftime('%M')
        return int(mins)

dateTime = raspberryDateTime()

try:
 
  print "Waiting for PIR to settle ..."
 
  # Loop until PIR output is 0
  while GPIO.input(GPIO_PIR)==1:
    Current_State  = 0
 
  print "  Ready"
 
  # Loop until users quits with CTRL-C
  while True :
## TIEMPO REAL    
    tReal= dateTime.get_time()
    
    # Read PIR state
    Current_State = GPIO.input(GPIO_PIR)
 
    if Current_State==1 and Previous_State==0:
      # PIR is triggered
      print "  Motion detected!"
##se cuenta cuantas veces se le sirve comida
##siendo un maximo de 2 veces

##      AQUI DEBE IR EL SERVO
      if cont <= 1:
        if cont == 0:
          timeMin = dateTime.get_min()
        timeDif = timeMin2 - timeMin
        timeMin2 = dateTime.get_min()
        if timeDif >= 1:
          cont = cont + 1
          timeDif = time
          x.update_status('Prueba #'+str(cont)+str(tReal))
      # Record previous state
      Previous_State=1
    elif Current_State==0 and Previous_State==1:
      # PIR has returned to ready state
      print "  Ready"
      Previous_State=0
 
    # Wait for 10 milliseconds
    time.sleep(0.01)
 
except KeyboardInterrupt:
  print "  Quit"
  # Reset GPIO settings
  GPIO.cleanup()

