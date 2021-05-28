import serial
import time

ser = serial.Serial(port='COM4', baudrate=9600)

def open_door():
    ser.write('1'.encode())
    time.sleep(20)
    ser.write('0'.encode())
    #ser.close()

def close_door():
    ser.write('0'.encode())
    #ser.close()