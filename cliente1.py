import tkinter as tk
import socket
import pickle
import numpy as np

class MatrixEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Player 1")

        self.root.geometry("300x400")  # Ancho x Alto
        # Matrices iniciales y matrices de estado
        self.matrix1 = np.zeros((3, 3), dtype=int)
        self.matrix2 = np.zeros((3, 3), dtype=int)
        self.last_shot_matrix = None  # Matriz para el último disparo
        self.matrix1_buttons = [[None, None, None], [None, None, None], [None, None, None]]
        self.matrix2_buttons = [[None, None, None], [None, None, None], [None, None, None]]

        title_label1 = tk.Label(root, text="Disparos", font=("Helvetica", 16))
        title_label1.grid(row=0, column=0, columnspan=3)

        title_label2 = tk.Label(root, text="Barcos", font=("Helvetica", 16))
        title_label2.grid(row=4, column=0, columnspan=3)
        
        # Crear las matrices y etiquetas
        self.create_matrix_frame(self.matrix1, self.matrix1_buttons, 1)
        self.create_matrix_frame(self.matrix2, self.matrix2_buttons, 5)

        for i in range(3):
            for j in range(3):
                self.matrix1_buttons[i][j].config(state=tk.DISABLED)

        # Botón para imprimir ambas matrices y enviar la matriz 2 al servidor 1
        self.Disparo = tk.Button(root, text="Disparar", command=self.print_and_send_matrices)
        self.Disparo.grid(row=9, column=0, columnspan=3)

        self.Disparo.grid_remove()

        # Botón para enviar solo la matriz 2 al servidor 2
        self.send_matrix2_button = tk.Button(root, text="Registrar barcos", command=self.send_matrix2)
        self.send_matrix2_button.grid(row=10, column=0, columnspan=3)

    def create_matrix_frame(self, matrix, button_matrix, row_offset):
        matrix_frame = tk.Frame(self.root)
        matrix_frame.grid(row=row_offset, column=0, padx=10, pady=10)

        for i in range(3):
            for j in range(3):
                button = tk.Button(matrix_frame, text=str(matrix[i][j]), width=5,
                                   command=lambda r=i, c=j: self.toggle_button(matrix, button_matrix, r, c))
                button.grid(row=i, column=j)
                button_matrix[i][j] = button

    def toggle_button(self, matrix, button_matrix, row, col):
        matrix[row][col] = 1 if matrix[row][col] == 0 else 0
        button_matrix[row][col].config(text=str(matrix[row][col]))

        # Actualizar last_shot_matrix con el último disparo
        self.last_shot_matrix = np.zeros((3, 3), dtype=int)
        self.last_shot_matrix[row][col] = matrix[row][col]

        # Deshabilitar todos los botones de la matriz 1
        for i in range(3):
            for j in range(3):
                self.matrix1_buttons[i][j].config(state=tk.DISABLED)

    def print_and_send_matrices(self):
        # Imprimir matrices en la consola
        print("Matriz 1:")
        print(self.matrix1)

        print("\nMatriz 2:")
        print(self.matrix2)
        
        # Imprimir la tercera matriz (last_shot_matrix)
        print("\nÚltimo Disparo:")
        print(self.last_shot_matrix)

        self.send_matrix_to_server(1, self.last_shot_matrix)

        for i in range(3):
            for j in range(3):
                self.matrix1_buttons[i][j].config(state=tk.NORMAL)

    def send_matrix2(self):
        # Enviar solo la matriz 2 al servidor 2
        self.send_matrix_to_server(2, self.matrix2)

        # Deshabilitar los botones de la matriz 2
        for i in range(3):
            for j in range(3):
                self.matrix2_buttons[i][j].config(state=tk.DISABLED)

        # Ocultar el botón "Enviar Matriz 2"
        self.send_matrix2_button.grid_remove()
        self.Disparo.grid()

        for i in range(3):
            for j in range(3):
                self.matrix1_buttons[i][j].config(state=tk.NORMAL)

    def send_matrix_to_server(self, server_number, matrix):
        if server_number == 1:
            host = '127.0.0.1'
            port = 54321
        elif server_number == 2:
            host = '127.0.0.1'
            port = 12345
        else:
            return  # Manejar otros números de servidor según sea necesario

        # Establecer conexión con el servidor
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))

        # Serializar la lista de matrices y enviarla al servidor
        serialized_matrices = pickle.dumps(matrix)
        client_socket.send(serialized_matrices)


        data = client_socket.recv(1024)
        print(f"Servidor dice: {data.decode('utf-8')}")

        if data.decode('utf-8') == "Disparo acertado":
            print("Disparo acertado")

            # Cambiar el color del último disparo en la matriz 1
            for i in range(3):
                for j in range(3):
                    if self.last_shot_matrix[i][j] == 1:
                        self.matrix1_buttons[i][j].config(bg='green')  # Cambiar a color verde (o el color que desees)
                        self.matrix1_buttons[i][j].config(state=tk.DISABLED)

        # Cerrar la conexión con el servidor
        client_socket.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = MatrixEditor(root)
    root.mainloop()
