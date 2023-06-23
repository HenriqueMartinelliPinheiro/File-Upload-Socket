# server.py

import socket
import threading
import os

def handle_client(client_socket, client_address):
    print(f'[+] Handling connection from {client_address}')

    # Recebendo o nome do arquivo
    file_name = client_socket.recv(1024).decode()

    # Recebendo o tamanho do arquivo
    file_size = int(client_socket.recv(1024).decode())
    print(f'[+] Receiving file {file_name} of size {file_size} bytes')

    # Recebendo o arquivo
    with open(file_name, 'wb') as f:
        bytes_received = 0
        while bytes_received < file_size:
            chunk = client_socket.recv(1024)
            f.write(chunk)
            bytes_received += len(chunk)
            progress = (bytes_received / file_size) * 100
            print(f'[+] {file_name} - {progress:.2f}%')

    print(f'[+] File {file_name} received successfully')

    client_socket.close()


def main():
    server_ip = '0.0.0.0'
    server_port = 12345

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((server_ip, server_port))
    server.listen(5)

    print(f'[+] Server listening on {server_ip}:{server_port}')

    try:
        while True:
            client_socket, client_address = server.accept()
            client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_handler.start()
    except KeyboardInterrupt:
        print('\n[+] Server shutting down')
        server.close()


if __name__ == '__main__':
    main()
