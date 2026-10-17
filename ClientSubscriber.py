import socket


def avvia_subscriber():
    host = '127.0.0.1'
    port = 1234

    # 1. Connessione al broker
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    # 2. Iscrizione al topic: utilizza il formato richiesto dal broker
    topic = input("Inserire un topic: ")
    messaggio_iscrizione = f"sub:{topic}\n"
    s.sendall(messaggio_iscrizione.encode('ascii'))
    print(f"Iscritto con successo al topic: {topic}")

    # 3. Ricezione continua dei messaggi pubblicati
    try:
        while True:
            dati = s.recv(1024)
            if not dati:
                print("Connessione chiusa dal server.")
                break
            messaggio = dati.decode('ascii').strip()
            print(f"Nuovo messaggio ricevuto: {messaggio}")
    except KeyboardInterrupt:
        print("Chiusura del subscriber.")
    finally:
        s.close()


if __name__ == '__main__':
    avvia_subscriber()