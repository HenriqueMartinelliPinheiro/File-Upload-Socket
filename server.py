import socket
import threading
import os

def receberArquivo(socketCliente, ipCliente):
    print(f'Processando requisição de: {ipCliente}')

    nomeArquivo = socketCliente.recv(1024).decode() #recebe o nome do arquivo com no máximo 1024 bytes

    tamanhoArquivo = int(socketCliente.recv(1024).decode()) # recebe o tamnho do arquivo e converte em int
    print(f'Recebendo Arquivo{nomeArquivo}')

    diretorio = "arquivos" # diretório onde o arquivo será salvo
    os.makedirs(diretorio, exist_ok=True) # se o diretório não existir é criado
    caminhoArquivo = os.path.join(diretorio, nomeArquivo) # caminho completo do arquivo

    with open(caminhoArquivo, 'wb') as arquivo: 
        bytesEnviados = 0 # quantidade de bytes recebidos até o momento
        while bytesEnviados < tamanhoArquivo:
            dados = socketCliente.recv(1024) # recebe 1024 bytes por vez
            arquivo.write(dados) # escreve no arquivo
            bytesEnviados += len(dados)
            progresso = (bytesEnviados / tamanhoArquivo) * 100 # progresso do upload
            print(f'{nomeArquivo} - {progresso:.2f}%')

    print(f'Arquivo {nomeArquivo} recebido')

    socketCliente.close() # encerra a conexão


def main():
    ipServer = '0.0.0.0'
    portaServer = 12345

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # cria o socket
    server.bind((ipServer,portaServer)) # vincula o socket ao IP e porta
    server.listen(5) # fica esperando conexões, no máximo 5

    print(f'[+] Servidor Aguradando em {ipServer}:{portaServer}')

    try:
        while True:
            socketCliente, ipCliente = server.accept() # aceita conexão do socket do cliente
            requisicaoCliente = threading.Thread(target=receberArquivo, args=(socketCliente, ipCliente))
            # cria a thread para a função receberArquivo
            requisicaoCliente.start()
    except KeyboardInterrupt:
        print('\n[+] Desligando Servidor')
        server.close()


if __name__ == '__main__':
    main()
