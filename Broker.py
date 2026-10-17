import socket
import threading
import time


diz = {
           "meteo" : [],
           "sport" : []
       }


class Broker(threading.Thread):
   def __init__(self,sock):
       threading.Thread.__init__(self)
       self.sock = sock
       self.diz = diz

   def run(self):
       try:
           while True:
               filename = self.readLine(self.sock)
               if not filename:
                   break
               if filename[0] == "sub":
                   self.sub(filename)
               elif filename[0] == "pub":
                   self.pub(filename)
       except Exception as e:
           print(f"Error during client gestion: {e}")
       finally:
           self.sock.close()
           print('Transfer completed!. Connection to the client closed.')
           print('')


   def readLine(self, sk):
       data = b''
       while b'\n' not in data:
           packet = sk.recv(1024)
           if not packet:  # Gestisce la chiusura del client
               return None
           data += packet
       stringa_testo = data.decode('ascii').strip()
       return stringa_testo.split(":")


   def sub(self, filename):
        topic = filename[1]  # il messaggio dai client: ["sub", "topic"]
        if topic in self.diz.keys():
            self.diz[topic].append(self.sock)  # lo iscrive al topic
            print(f"Client registrato al topic: {topic}")
            while True:  # per disconnetterlo
                if not self.sock.recv(1024):
                    self.diz[topic].remove(self.sock)
                    break
            print(self.diz)


   def pub(self,filename):
    topic = filename[1]
    message = filename[2]
    if topic in self.diz.keys():
        messaggio_finale = f"{message}\n".encode('ascii')
        for i in self.diz[topic]:
            i.sendall(messaggio_finale)
    else:
        self.diz[topic] = []



















def Main():
   host = ''
   port = 1234


   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
   s.bind((host, port))
   s.listen(5)


   print('Server started.')


   while True:
       c, addr = s.accept()
       print('client connected ip:<' + str(addr) + '>')
       t = Broker(c)
       t.start()
   s.close()


if __name__ == '__main__':
   Main()
