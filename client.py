import socket
import os
import time 

def send_file(server_ip, server_port, file_path):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, server_port))

    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)

    # Enviando o nome do arquivo
    client.send(file_name.encode())

    # Adicionando um pequeno atraso para garantir que o servidor receba o nome do arquivo
    time.sleep(0.1)  # Adicione esta linha

    # Enviando o tamanho do arquivo
    client.send(str(file_size).encode())

    # Enviando o arquivo
    with open(file_path, 'rb') as f:
        bytes_sent = 0
        while bytes_sent < file_size:
            chunk = f.read(1024)
            client.send(chunk)
            bytes_sent += len(chunk)
            progress = (bytes_sent / file_size) * 100
            print(f'[+] {file_name} - {progress:.2f}%')

    print(f'[+] File {file_name} sent successfully')

    client.close()


if __name__ == '__main__':
    server_ip = '172.29.0.8'
    server_port = 12345
    file_path = 'teste.txt'  # Altere para o caminho do arquivo que deseja enviar

    send_file(server_ip, server_port, file_path)
