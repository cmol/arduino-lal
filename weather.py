#!/usr/bin/env python
import serial
#import Thread
import sqlite3
import datetime
import signal
import sys
from sys import stdout

class Weather: 

  #object __logging
  WIND_DIRECTION = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']

  def __init__(self):
    pass

  def update(self, wind_direction, wind_speed, temperature, preasure, humidity):
    self.__wind_direction = int(int(wind_direction)/128)
    self.__wind_speed = int(wind_speed)
    self.__temperature = int(temperature)
    self.__preasure = float(preasure)/1000
    self.__humidity = int(humidity)/10

  def log(self):
    db.execute('INSERT INTO log (logged, wind_direction, wind_Speed, temperature, preasure, humidity) VALUES (?, ?, ?, ?, ?, ?)', (datetime.datetime.now(), self.__wind_direction, self.__wind_speed, self.__temperature, self.__preasure, self.__humidity))
    db.commit()

  def __str__(self):
    return ('V: %s %sm/s T:%sK P:%s H:%s' % (Weather.WIND_DIRECTION[self.__wind_direction], self.__wind_speed, self.__temperature, self.__preasure, self.__humidity))
#End weather

# Handle exit gracefully

def exit_handler(signal, frame):
  print 'You pressed Ctrl+C!'
  sys.exit(0)

signal.signal(signal.SIGINT, exit_handler)

db = sqlite3.connect('log.db')

try:
  db.execute('CREATE TABLE log (logged datetime, wind_direction int, wind_speed int, temperature int, preasure float, humidity)')
except:
  pass

ser = serial.Serial(port = "/dev/ttyUSB0", baudrate = 9600)
weather = Weather()

while True:
  sensors = ser.readline().split(';')
  if len(sensors) != 5:
    continue
  weather.update(*sensors);
  stdout.write("\r%s" % '{: <48}'.format(weather))
  stdout.flush()
  weather.log()
  ser.write("1:%s" % '{: <32}'.format(weather))
