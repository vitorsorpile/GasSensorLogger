# Import socket module
import socket
from time import sleep
 

s = socket.socket()        
port = 8754             
s.connect(('127.0.0.1', port))



s.send('0'.encode())

res = s.recv(1024).decode()

if (res != 'ACK'):
    print('Algo deu errado...')
    exit()

i = 0
while True:
    s.send(str(i).encode())
    i += 1
    sleep(1)

# close the connection
s.close()  