import socket
import pickle  # Para serializar/deserializar las matrices
import numpy as np

def compare_matrices(matrix1, matrix2):
    # Comparar elemento por elemento de las matrices
    for i in range(matrix1.shape[0]):
        for j in range(matrix1.shape[1]):
            if matrix1[i, j] == 1 and matrix2[i, j] == 1:
                return True  # Hay un "1" en la misma posición, disparo acertado
    return False  # No se encontraron "1" en la misma posición, disparo fallido
def server2():
    host = '127.0.0.1'
    port = 54321

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"Server 2 is listening on {host}:{port}")
    first_matrix_received = None  # Variable para almacenar la primera matriz recibida
    client_scores = {} 

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")

        # Recibir datos serializados
        data = client_socket.recv(4096)

        if not data:
            break

        received_matrix_list = pickle.loads(data)
        received_matrix = np.array(received_matrix_list)  # Convertir la lista de listas en una matriz NumPy

        # Almacenar la primera matriz recibida si aún no se ha almacenado
        if first_matrix_received is None:
            first_matrix_received = received_matrix
            response = "Barcos registrados correctamente"
            
        else:
            # Comparar la matriz recibida con la primera matriz almacenada
            if compare_matrices(first_matrix_received, received_matrix):
                print("Disparo acertado")
                response = "Disparo acertado"
                # Incrementar la puntuación del cliente
                client_ip = addr[0]
                if client_ip in client_scores:
                    client_scores[client_ip] += 1
                else:
                    client_scores[client_ip] = 1
                print(f"Puntuación de {client_ip}: {client_scores[client_ip]}")
                # Envía la puntuación al servidor 3
                send_score_to_server3(client_scores)
            else:
                print("Disparo fallido")
                response = "Disparo fallido"

        client_socket.send(response.encode('utf-8'))
        # Hacer algo con la matriz recibida, por ejemplo, imprimir en el servidor
        print(f"Data from client: {addr} in server 1")
        for row in received_matrix:
            print(row)

        client_socket.close()

def send_score_to_server3(scores):
    # Establece la conexión con el servidor 3 y envía la puntuación
    host = '127.0.0.1'
    port = 123  # Puerto del Servidor 3

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # Serializa y envía el diccionario de puntuación
    serialized_scores = pickle.dumps(scores)
    client_socket.send(serialized_scores)

    client_socket.close()

if __name__ == "__main__":
    server2()