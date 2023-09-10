import socket
import pickle

def client():
    host = '127.0.0.1'
    port = 123  # Puerto del Servidor 3 (donde se envían los datos de puntuación)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    while True:
        # Recibir datos serializados (diccionario de puntuación)
        data = client_socket.recv(4096)

        if not data:
            break

        # Deserializar los datos en un diccionario de puntuación
        scores = pickle.loads(data)
        
        # Procesar la puntuación recibida
        for client_ip, score in scores.items():
            print(f"Puntuación de {client_ip}: {score}")

    client_socket.close()

if __name__ == "__main__":
    client()
