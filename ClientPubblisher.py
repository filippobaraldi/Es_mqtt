import socket

def Main():

    host = '127.0.0.1'      # The remote host
    port = 1234             # The same port as used by the server

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    topic = input("Inserire un topic: ")
    contenuto = input("Inserire un contenuto: ")
    messaggio = f"pub:{topic}:{contenuto}\n"

    sock.sendall(messaggio.encode('ascii'))
    print("Messaggio inviato con successo.")

if __name__ == '__main__':
    Main()