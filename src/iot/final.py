# Universidad del Valle de Guatemala
# Angel Basegoda 13256
# Erick  Hernández Woc 13197
# Johnny del Cid  13032
# Sergio Cancinos 13062
# final.py 
# El programa utiliza el sensor PIR para mandar mensajes a twitter cada vez que el sensor indique que hubo movimiento. 

#!/usr/bin/python
# -*- coding: utf-8 -*-
#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
import tweepy

sensorPin = 7
cont = 0
contp = 0
GPIO.setmode(GPIO.BOARD)
GPIO.setup(sensorPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

prevState = False
currState = False

#Informacion para conectarse con la app
CONSUMER_KEY = 'IGrdYa7WN7CdUcRkGM9JayCe4'
CONSUMER_SECRET = 'qbqStO71i91BCOPFUXMKx3mhwC1Xatk3GnlwM1Yp1b7QeV3uZc'
ACCESS_KEY = '2817354110-u5tRa5y92pdAegtemBfaUAVduQI6bWwr3DOaG9d'
ACCESS_SECRET = '1NzC3X3iqm6HXBH5st2zqukFHlbpPLsKlbEuFyO0SBUgj'
#En esta parte nos identifica para poder realizar operaciones
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
x = tweepy.API(auth)

while True:
    time.sleep(.1)
    prevState = currState
    currState = GPIO.input(sensorPin)
    if currState != prevState:
            cont = cont+1
	    print "GPIO pin {0} is {1}".format(sensorPin, "HIGH"+str(cont) if currState else "LOW"+str(cont))
    if currState == True & contp != cont:
            contp = contp + 1
            x.update_status('Prueba #'+str(cont))
