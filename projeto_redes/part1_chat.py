import socket
import struct
import threading

MCAST_GRP = '0'
MCAST_PORT = 5007

class Cliente:
    def __init__(self):
        self.socket = None

    def criar_socket(self):
        # Retorna uma porta aleatória.
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(('', MCAST_PORT))
        mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
        self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    def criar_pkg(self, mensagem):
        # (UDP)
        # pkg -> mensagem a ser enviada.
        return mensagem.encode('utf-8')
    
    def send(self, destinatario, mensagem):
        # (ip, porta) -> tuple | ambas são informações do destinatário. 
        pkg = self.criar_pkg(mensagem)
        self.socket.sendto(pkg, destinatario)
    
    def receive(self, rx):
        # Rx se trata de um buffer onde armazenada a mensagem.
        data, addr = self.socket.recvfrom(rx)
        return data.decode('utf-8'), addr

class Servidor:
    def __init__(self):
        self.socket = None

    def criar_socket(self):
        # Porta qualquer fixa
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.IP_MULTICAST_TTL, 1)

    def send(self, destinatario, mensagem):
        # (ip, porta) -> ex.: 192.168.0.1 : 50000, tuple | inverte as informações recebidas e envia de volta uma nova msg.
        # PING... PONG
        pkg = mensagem.encode('utf-8')
        self.socket.sendto(pkg, destinatario)
    
    def receive(self, rx):
        # Tratar msg recebida, confirmar.
        data, addr = self.socket.recvfrom(rx)
        return data.decode('utf-8'), addr
    
def cliente_func():
    cliente = Cliente()
    cliente.criar_socket()
    
    while True:
        mensagem, addr = cliente.receive(1024)
        print(f"{addr} \n {mensagem}")

        resposta = input("Mensagem: ")
        cliente.send(resposta, (MCAST_GRP, MCAST_PORT))

def servidor_func():
    servidor = Servidor()
    servidor.criar_socket()

    while True:
        mensagem = input("Mensagem: ")
        servidor.send(mensagem, (MCAST_GRP, MCAST_PORT))

        print("Aguardando resposta...")
        data, addr = servidor.receive(1024)
        print(f"{addr} \n {mensagem}")

if __name__ == "__main__":
    escolha = input("Iniciar como: (c) cliente ou (s) servidor?")

    if escolha == 'c':
        cliente_func()
    elif escolha == 's':
        servidor_func()
    else:
        print("Opcao invalida. Encerrando.")
