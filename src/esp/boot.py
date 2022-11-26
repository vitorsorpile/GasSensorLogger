# boot.py -- run on boot-up
import ubinascii
import machine
import micropython
import network
import socket
import esp
esp.osdebug(None)
import gc
gc.collect()


from config import WIFI_SSID, WIFI_PASSWORD
from pins import *

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(WIFI_SSID, WIFI_PASSWORD)

while station.isconnected() == False:
    pass

print(f'Connection to {WIFI_SSID} successful')
print(station.ifconfig())

# s = socket.socket()
# port = 8080
# address = '127.0.0.1'

# print(f'Conectando ao servidor no IP {address} e porta {port}')
# s.connect((address, port))

# s.send('0'.encode())

# res = s.recv(1024).decode()

# if (res != 'ACK'):
#     print('Algo deu errado...')
#     exit()
