import socket
import os
import time 

def enviarArquivo(ipServer, portaServer, caminhoArquivo):
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # cria o socket 
    cliente.connect((ipServer, portaServer)) # inicia a conexão com o servidor

    nomeArquivo = os.path.basename(caminhoArquivo) 
    tamanhoArquivo = os.path.getsize(caminhoArquivo)

    # envia o nome e tamanho do arquivo
    cliente.send(nomeArquivo.encode())
    time.sleep(0.1)  # espera para o servidor poder receber o nome do arquivo
    cliente.send(str(tamanhoArquivo).encode()) # envia o arquivo

    # Enviando o arquivo
    with open(caminhoArquivo, 'rb') as arquivo:
        bytesEnviados = 0 # quantidade de bytes enviados
        while bytesEnviados < tamanhoArquivo:
            dados = arquivo.read(1024) # lê 1024 bytes do conteúdo do arquivo
            cliente.send(dados) # envia o pedaço de dados
            bytesEnviados += len(dados)
            progresso = (bytesEnviados / tamanhoArquivo) * 100 # progresso
            print(f'{nomeArquivo} - {progresso:.2f}%')

    print(f'Arquivo {nomeArquivo} enviado.')

    cliente.close() # encerra a conexão


if __name__ == '__main__':
    ipServer = '172.29.0.8'
    portaServer = 12345
    caminhoArquivo = 'teste.txt' # caminho do arquivo enviado

    enviarArquivo(ipServer, portaServer, caminhoArquivo)
