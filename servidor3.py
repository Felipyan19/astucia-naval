import socket
import pickle
import tkinter as tk

# Variable global para el cuadro de texto
text_box = None

def display_scores(scores):
    global text_box  # Acceder a la variable global
    text_box.delete("1.0", tk.END)  # Borrar el contenido actual del cuadro de texto
    for client_ip, score in scores.items():
        text_box.insert(tk.END, f"{client_ip}: {score}\n")

def server3():
    host = '127.0.0.1'
    port = 123  # Puerto en el que escucha el Servidor 3

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"Server 3 is listening on {host}:{port}")

    # Crear la ventana emergente
    window = tk.Tk()
    window.title("Puntuación de Jugadores")

    global text_box  # Acceder a la variable global
    # Crear un cuadro de texto para mostrar los datos
    text_box = tk.Text(window)
    text_box.pack()

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")

        # Recibir datos serializados (diccionario de puntuación)
        data = client_socket.recv(4096)

        if not data:
            break

        # Deserializar los datos en un diccionario de puntuación
        scores = pickle.loads(data)
        
        # Mostrar los datos de puntuación en el cuadro de texto
        display_scores(scores)

        client_socket.close()

    window.mainloop()  # Mantener la ventana abierta

if __name__ == "__main__":
    server3()
