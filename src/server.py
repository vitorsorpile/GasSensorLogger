import socket
import os
from threading import Thread, Lock
from datetime import datetime, timedelta
import threading


class Server:
    def __init__(self, address, port):
        self.DATABASE_PATH = './db/'
        self.address = address
        self.port = port
        self.threads = []
        self.mutex = Lock()
        
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.s.settimeout(5)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((address, port))
        
        print("socket binded to port", port)

    def start(self):
        self.stop_threads = False
        try:
            self.s.listen(5)
            
            while True:
                c, addr = self.s.accept()
                print ('Got connection from', addr )

                #c.send('Please send your connection mode: 1-> Sensor | 2 -> Reader'.encode())
                
                connection_mode = c.recv(64).decode()

                if connection_mode == '0':
                    tmp = Thread(target = self.handle_sensor, args= (c, addr))
                # Close the connection with the client
                elif connection_mode == '1':
                    tmp = Thread(target = self.handle_reader, args= (c, addr))
                else:
                    print(f'Invalid connection mode: {connection_mode}')
                    c.send(f'{connection_mode} is not a valid connection mode...'.encode())
                    c.close()
                    continue

                self.threads.append(tmp)
                tmp.start()
        except KeyboardInterrupt:
            self.stop_threads = True
            for thread in self.threads:
                thread.join()
            self.s.close()
        except Exception as e:
            print(e)



    def handle_sensor(self, client, address):
        print(f"sensor conectado no IP: {address[0]} - porta: {address[1]}")
        client.send('ACK'.encode())
        while (True):
            
            msg = client.recv(1024).decode()
            
            if not msg or self.stop_threads == True:
                client.close()
                break
            self.mutex.acquire()
            try:
                print(f'sensor enviou o valor {msg}')
                now = datetime.now()
                today = now.strftime('%Y-%m-%d')
                with open(self.DATABASE_PATH + today + '.txt', 'a') as file:
                    file.write(now.strftime('%Y-%m-%d %H:%M:%S - ') +  msg + '\n')
            finally:
                self.mutex.release()
            

    def handle_reader(self, client, address):
        print(f"reader conectado no IP: {address[0]} - porta: {address[1]}")
 
        while True:
            client.send('\nDigite a data inicial e a data final do perído que deseja saber os dados no formato "YYYY-MM-DD YYYY-MM-DD" ou pressione Enter para sair:\n'.encode())
            print('ue')
            msg = client.recv(1024).decode()
            print(f'msg: {msg}')
            if not msg or self.stop_threads == True:
                print(f'Encerrando conexão com {address[0]} - porta: {address[1]}')
                client.close()
                break

            self.mutex.acquire()
            print(f'{threading.get_native_id()}: peguei o mutex')
            try:
                initialDateStr, finalDateStr = msg.split(' ')
                initialDate = str_to_date(initialDateStr)
                finalDate = str_to_date(finalDateStr)
                
                if not initialDate:
                    client.send('ERRO: Data inicial inválida...\n'.encode())
                    continue

                if not finalDate:
                    client.send('ERRO: Data final inválida...\n'.encode())
                    continue

                if initialDate > finalDate:
                    client.send('ERRO: Data final anterior à data inicial...\n'.encode())
                    continue
                
                for date in daterange(initialDate, finalDate):
                    filePath = self.DATABASE_PATH + date + '.txt'
                    print(f'Tentando ler dados no arquivo {filePath}')
                    if os.path.exists(filePath):
                        with open(filePath, 'r') as file:
                            for line in file:
                                print(f'Sent {msg} to {client}')
                                client.send(line.encode())
                    else:
                        client.send(f'Não há dados disponível para o dia {date}\n'.encode()) 
                client.send('EOF'.encode())
            except:
                client.send('ERRO: Algo inesperado aconteceu...\n'.encode())

            finally:
                print(f'{threading.get_native_id()}: liberei o mutex')
                self.mutex.release()

def str_to_date(date_string):
    try:
        return datetime.strptime(date_string, "%Y-%m-%d")
    except ValueError:
        return False

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days + 1)):
        yield (datetime.strftime(start_date + timedelta(days = n), "%Y-%m-%d"))

if __name__ == '__main__':
    server = Server('', 8080)
    server.start()