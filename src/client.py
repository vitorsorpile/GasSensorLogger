# Import socket module
import socket    
from time import sleep        
 
# Create a socket object
s = socket.socket()        
 
# Define the port on which you want to connect
port = 8754               
 
# connect to the server on local computer
s.connect(('127.0.0.1', port))
# print (s.recv(1024).decode())

s.send('1'.encode())


while True:
    print (s.recv(1024).decode())
    
    msg = input('msg: ')

    s.send(msg.encode())
    if not msg:
        break

    response = ''
    while(1):
        response = s.recv(1024).decode()
      
        if (response.find('EOF') != -1):
            response = response.replace('EOF', '\n')
            break
        
        print(response, end='')
        if response.startswith('ERRO'):
            # print('Erro detectado')
            break
    
# close the connection
s.close()