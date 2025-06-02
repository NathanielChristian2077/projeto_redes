import os.path
import socket
import struct
import threading
import json
import datetime

MCAST_GRP = '224.0.0.27'
MCAST_PORT = 5007

# TODO write/read file.json format -> {
#    "date" : "date_value",
#    "time" : "time_value",
#    "username" : "username_value",
#    "message" : "message_value"
#  }

def write(path, username, message):
    time = datetime.datetime.now()
    nova_msg = {
        "date": time.strftime("%d/%m/%Y"),
        "time": time.strftime("%H:%M:%S"),
        "username": username,
        "message": message
    }
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as file:
                hist = json.load(file)
        except: json.JSONDecodeError:
            hist = []
    else:
        hist = []



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

    @staticmethod
    def criar_pkg(mensagem):
        # (UDP)
        # pkg -> mensagem a ser enviada.
        return mensagem.encode('utf-8')

    def send(self, mensagem):
        # (ip, porta) -> tuple | ambas são informações do destinatário.
        pkg = self.criar_pkg(mensagem)
        self.socket.sendto(pkg, (MCAST_GRP, MCAST_PORT))  # type: ignore

    def receive(self):
        # Rx se trata de um buffer onde armazenada a mensagem.
        while True:
            data, addr = self.socket.recvfrom(1024)  # type: ignore
            print(f"{data.decode('utf-8')}")


class Servidor:
    def __init__(self):
        self.socket = None

    def criar_socket(self):
        # Porta qualquer fixa
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)

    def send(self, mensagem):
        # (ip, porta) -> ex.: 192.168.0.1 : 50000, tuple | inverte as informações recebidas e envia de volta uma nova msg.
        # PING... PONG
        pkg = mensagem.encode('utf-8')
        self.socket.sendto(pkg, (MCAST_GRP, MCAST_PORT))  # type: ignore

    def receive(self):
        # Tratar msg recebida, confirmar.
        while True:
            data, addr = self.socket.recvfrom(1024)  # type: ignore
            print(f"{data.decode('utf-8')}")


def cliente_func():
    cliente = Cliente()
    cliente.criar_socket()

    threading.Thread(target=cliente.receive, daemon=True).start()

    while True:
        mensagem = input("Mensagem: ")
        cliente.send(mensagem)


def servidor_func():
    servidor = Servidor()
    servidor.criar_socket()

    threading.Thread(target=servidor.receive, daemon=True).start()

    while True:
        mensagem = input("Mensagem: ")
        servidor.send(mensagem)


if __name__ == "__main__":
    escolha = input("Iniciar como: (c) cliente ou (s) servidor?")

    if escolha == 'c':
        cliente_func()
    elif escolha == 's':
        servidor_func()
    else:
        print("Opcao invalida. Encerrando.")
