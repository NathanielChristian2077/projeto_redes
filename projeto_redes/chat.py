import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime
import json
from utils import load_hist, hist_save

# Multicasting configs
MCAST_GRP = '224.0.1.7'
MCAST_PORT = 5007
USERNAME = input("Digite seu nome de usuário: ")

# Socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', MCAST_PORT))
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(MCAST_GRP) + socket.inet_aton('0.0.0.0'))

# GUI
window = tk.Tk()
window.title("MChast")
window.geometry("400x600")

chat_text = scrolledtext.ScrolledText(window, state='disabled', wrap=tk.WORD)
chat_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

frame_low = tk.Frame(window)
frame_low.pack(fill=tk.X, padx=10, pady=(0, 10))

msg_input = tk.Entry(window)
msg_input.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)

def send(event=None):
    msg = msg_input.get()
    if msg.strip() == "":
        return
    now = datetime.now()
    json_msg = {
        "date": now.strftime("%d/%m/%Y"),
        "time": now.strftime("%H:%M:%S"),
        "username": USERNAME,
        "message": msg
    }
    try:
        sock.sendto((json.dumps(json_msg).encode('utf-8')), (MCAST_GRP, MCAST_PORT))
        msg_input.delete(0, tk.END)
        hist_save(json_msg)
    except Exception as e:
        print(f"Erro no envio da mensagem: {e}")
msg_input.bind('<Return>', send)

# Botões
btn_send = tk.Button(frame_low, text="send", command=send)
btn_send.pack(side=tk.RIGHT, padx=(10, 0))

# Atualizando chat
def chat_update(msg_json):
    chat_text.configure(state='normal')
    chat_text.insert(tk.END, f"[{msg_json['date']} {msg_json['time']}] {msg_json['username']}: {msg_json['message']}\n")
    chat_text.see(tk.END)
    chat_text.configure(state='disabled')

# Threading
def thread_recv():
    while(True):
        data, _ = sock.recvfrom(1024)
        try:
            msg_json = json.loads(data.decode('utf-8'))
            chat_update(msg_json)
            hist_save(msg_json)
        except json.JSONDecodeError:
            continue

if __name__ == "__main__":
    # Loading hist
    for msg in load_hist():
        chat_update(msg)
    # Start da thread
    threading.Thread(target=thread_recv, daemon=True).start()
    # Loop básico do código
    window.mainloop()