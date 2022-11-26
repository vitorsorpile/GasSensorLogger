# main.py -- put your code here!\
from pins import *
from MQ2 import MQ2
from time import sleep
import socket


s = socket.socket()
port = 8754
address = '192.168.15.8'
#address = '172.20.10.2'

addr_info = socket.getaddrinfo("localhost", 8754)
print(addr_info)
# addr = addr_info[0][-1]
# print(addr)


print(f'Conectando ao servidor no IP {address} e porta {port}...', end ='')
s.connect((address, port))
print(f'\r-> Conectado ao servidor no IP {address} e porta {port}')

s.send('0'.encode())

res = s.recv(1024).decode()

if (res != 'ACK'):
    print('Algo deu errado...')
    exit()


MQ2_sensor = MQ2(gasSensor)

#MQ2_sensor.calculateR0()
while(1):
    value = MQ2_sensor.getPPM('CO')
    print(value)
    s.send((str(round(value, 3)) + '\n').encode())
    sleep(1)