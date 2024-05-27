import socket
import threading

# Definir la dirección y el puerto en el que el servidor escuchará
HOST = '0.0.0.0'
PORT = 80

def handle_request(conn, addr):
    # Registrar los detalles de la solicitud entrante
    request = conn.recv(1024).decode('utf-8')
    print(f'Solicitud recibida de {addr}:\n{request}')

    # Construir la respuesta HTTP 404
    response = (
        "HTTP/1.1 404 Not Found\r\n"
        "Content-Type: text/html\r\n"
        "Content-Length: 22\r\n"
        "\r\n"
        "<h1>404 Not Found</h1>"
    )

    # Enviar la respuesta HTTP 404 al cliente
    conn.sendall(response.encode('utf-8'))

    # Cerrar la conexión
    conn.close()

def start_server():
    # Crear un socket de servidor
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # Permitir la reutilización de la dirección
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Enlazar el socket a la dirección y puerto especificados
        server_socket.bind((HOST, PORT))
        
        # Comenzar a escuchar conexiones entrantes
        server_socket.listen()
        print(f'Servidor escuchando en {HOST}:{PORT}')

        while True:
            # Aceptar una nueva conexión
            conn, addr = server_socket.accept()
            print(f'Conexión aceptada de {addr}')
            
            # Crear y comenzar un nuevo hilo para manejar la solicitud
            thread = threading.Thread(target=handle_request, args=(conn, addr))
            thread.start()

# Iniciar el servidor
if __name__ == '__main__':
    start_server()
