import socket
import json
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import threading
import time
from datetime import datetime

class MonitoringClient:
    def __init__(self, host='localhost', port=9090):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.devices = {}
        self.monitoring = False
        self.monitor_interval = 10  # segundos
        
        # Criar interface gráfica
        self.create_gui()
        
    def create_gui(self):
        """Cria a interface gráfica"""
        self.root = tk.Tk()
        self.root.title("Sistema de Monitoramento - Cliente")
        self.root.geometry("800x600")
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=("wens"))
        
        # Configurar pesos para redimensionamento
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(2, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Frame de conexão
        conn_frame = ttk.LabelFrame(main_frame, text="Conexão", padding="5")
        conn_frame.grid(row=0, column=0, columnspan=2, sticky=("we"), pady=(0, 10))
        
        ttk.Label(conn_frame, text="Servidor:").grid(row=0, column=0, padx=(0, 5))
        self.host_var = tk.StringVar(value=self.host)
        ttk.Entry(conn_frame, textvariable=self.host_var, width=15).grid(row=0, column=1, padx=(0, 10))
        
        ttk.Label(conn_frame, text="Porta:").grid(row=0, column=2, padx=(0, 5))
        self.port_var = tk.StringVar(value=str(self.port))
        ttk.Entry(conn_frame, textvariable=self.port_var, width=8).grid(row=0, column=3, padx=(0, 10))
        
        ttk.Button(conn_frame, text="Conectar", command=self.connect_server).grid(row=0, column=4)
        
        # Frame de controles
        control_frame = ttk.LabelFrame(main_frame, text="Controles", padding="5")
        control_frame.grid(row=1, column=0, columnspan=2, sticky=("we"), pady=(0, 10))
        
        ttk.Button(control_frame, text="Listar Dispositivos", command=self.list_devices).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(control_frame, text="Obter Todos os Valores", command=self.get_all_values).grid(row=0, column=1, padx=(0, 5))
        
        # Monitoramento automático
        ttk.Label(control_frame, text="Intervalo (s):").grid(row=0, column=2, padx=(10, 5))
        self.interval_var = tk.StringVar(value=str(self.monitor_interval))
        interval_entry = ttk.Entry(control_frame, textvariable=self.interval_var, width=8)
        interval_entry.grid(row=0, column=3, padx=(0, 5))
        
        self.monitor_button = ttk.Button(control_frame, text="Iniciar Monitoramento", command=self.toggle_monitoring)
        self.monitor_button.grid(row=0, column=4, padx=(5, 0))
        
        # Frame de dispositivos
        devices_frame = ttk.LabelFrame(main_frame, text="Dispositivos", padding="5")
        devices_frame.grid(row=2, column=0, columnspan=2, sticky=("wens"))
        devices_frame.grid_rowconfigure(0, weight=1)
        devices_frame.grid_columnconfigure(0, weight=1)
        
        # Treeview para mostrar dispositivos
        self.tree = ttk.Treeview(devices_frame, columns=('Tipo', 'Dispositivo', 'Local', 'Valor', 'Última Atualização'), show='headings')
        self.tree.grid(row=0, column=0, sticky=("wens"))
        
        # Configurar colunas
        self.tree.heading('Tipo', text='Tipo')
        self.tree.heading('Dispositivo', text='Dispositivo')
        self.tree.heading('Local', text='Local')
        self.tree.heading('Valor', text='Valor')
        self.tree.heading('Última Atualização', text='Última Atualização')
        
        self.tree.column('Tipo', width=80)
        self.tree.column('Dispositivo', width=100)
        self.tree.column('Local', width=120)
        self.tree.column('Valor', width=100)
        self.tree.column('Última Atualização', width=150)
        
        # Scrollbar para treeview
        scrollbar = ttk.Scrollbar(devices_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky=("ns"))
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Bind para duplo clique (controlar atuadores)
        self.tree.bind('<Double-1>', self.on_device_double_click)
        
        # Frame de logs
        log_frame = ttk.LabelFrame(main_frame, text="Logs", padding="5")
        log_frame.grid(row=3, column=0, columnspan=2, sticky=("we"), pady=(10, 0))
        log_frame.grid_columnconfigure(0, weight=1)
        
        self.log_text = tk.Text(log_frame, height=8, width=80)
        self.log_text.grid(row=0, column=0, sticky=("we"))
        
        log_scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        log_scrollbar.grid(row=0, column=1, sticky=("ns"))
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        
    def log_message(self, message):
        """Adiciona mensagem ao log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def send_request(self, request):
        """Envia requisição UDP para o servidor"""
        try:
            request_json = json.dumps(request)
            self.socket.sendto(request_json.encode('utf-8'), (self.host, self.port))
            
            # Receber resposta
            data, address = self.socket.recvfrom(1024)
            return json.loads(data.decode('utf-8'))
            
        except Exception as e:
            self.log_message(f"Erro na comunicação: {e}")
            return None
    
    def connect_server(self):
        """Conecta ao servidor"""
        self.host = self.host_var.get()
        self.port = int(self.port_var.get())
        self.log_message(f"Conectando ao servidor {self.host}:{self.port}")
        
        # Testar conexão listando dispositivos
        self.list_devices()
    
    def list_devices(self):
        """Lista dispositivos do servidor"""
        request = {"cmd": "list_req"}
        response = self.send_request(request)
        
        if response and response.get('cmd') == 'list_resp':
            devices = response.get('place', [])
            self.log_message(f"Dispositivos encontrados: {len(devices)}")
            
            # Limpar treeview
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Adicionar dispositivos ao treeview
            for device in devices:
                parts = device.split('_')
                if len(parts) >= 3:
                    device_type = parts[0]
                    device_name = parts[1]
                    location = '_'.join(parts[2:])
                    
                    self.tree.insert('', 'end', iid=device, values=(
                        device_type, device_name, location, 'N/A', 'N/A'
                    ))
            
            # Obter valores iniciais
            self.get_all_values()
        else:
            self.log_message("Erro ao listar dispositivos")
    
    def get_all_values(self):
        """Obtém todos os valores dos dispositivos"""
        request = {"cmd": "get_req", "place": "all"}
        response = self.send_request(request)
        
        if response and response.get('cmd') == 'get_resp':
            device_names = response.get('place', [])
            values = response.get('value', [])
            
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            for device_name, value in zip(device_names, values):
                # Atualizar treeview
                if self.tree.exists(device_name):
                    current_values = list(self.tree.item(device_name, 'values'))
                    current_values[3] = str(value)  # Valor
                    current_values[4] = timestamp   # Timestamp
                    self.tree.item(device_name, values=current_values)
            
            self.log_message(f"Valores atualizados ({len(device_names)} dispositivos)")
        else:
            self.log_message("Erro ao obter valores")
    
    def get_single_value(self, device_name):
        """Obtém valor de um dispositivo específico"""
        request = {"cmd": "get_req", "place": device_name}
        response = self.send_request(request)
        
        if response and response.get('cmd') == 'get_resp':
            value = response.get('value')
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            if self.tree.exists(device_name):
                current_values = list(self.tree.item(device_name, 'values'))
                current_values[3] = str(value)
                current_values[4] = timestamp
                self.tree.item(device_name, values=current_values)
            
            return value
        return None
    
    def set_device_value(self, device_name, value):
        """Define valor de um atuador"""
        request = {
            "cmd": "set_req",
            "locate": device_name,
            "value": value
        }
        response = self.send_request(request)
        
        if response and response.get('cmd') == 'set_resp':
            returned_value = response.get('value')
            
            if 'error' in str(returned_value):
                self.log_message(f"Erro ao alterar {device_name}: {returned_value}")
                return False
            else:
                self.log_message(f"Dispositivo {device_name} alterado para: {returned_value}")
                
                # Atualizar treeview
                timestamp = datetime.now().strftime("%H:%M:%S")
                if self.tree.exists(device_name):
                    current_values = list(self.tree.item(device_name, 'values'))
                    current_values[3] = str(returned_value)
                    current_values[4] = timestamp
                    self.tree.item(device_name, values=current_values)
                
                return True
        
        self.log_message(f"Erro ao alterar dispositivo {device_name}")
        return False
    
    def on_device_double_click(self, event):
        """Manipula duplo clique em dispositivo"""
        selection = self.tree.selection()
        if selection:
            device_name = selection[0]
            values = self.tree.item(device_name, 'values')
            device_type = values[0]
            
            if device_type == 'actuator':
                self.control_actuator(device_name, values)
            else:
                # Para sensores, apenas atualizar valor
                self.get_single_value(device_name)
    
    def control_actuator(self, device_name, current_values):
        """Controla um atuador"""
        device_type = current_values[0]
        device_name_parts = current_values[1]
        location = current_values[2]
        current_value = current_values[3]
        
        # Criar janela de controle
        control_window = tk.Toplevel(self.root)
        control_window.title(f"Controlar {device_name}")
        control_window.geometry("300x200")
        control_window.resizable(False, False)
        
        # Centralizar janela
        control_window.transient(self.root)
        control_window.grab_set()
        
        frame = ttk.Frame(control_window, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text=f"Dispositivo: {device_name}").pack(pady=5)
        ttk.Label(frame, text=f"Tipo: {device_type}").pack(pady=5)
        ttk.Label(frame, text=f"Local: {location}").pack(pady=5)
        ttk.Label(frame, text=f"Valor atual: {current_value}").pack(pady=5)
        
        ttk.Label(frame, text="Novo valor:").pack(pady=5)
        
        # Entrada de valor baseada no tipo de dispositivo
        if 'light' in device_name or 'air' in device_name:
            # Para luzes e ar-condicionado (on/off)
            value_var = tk.StringVar(value=current_value if current_value in ['on', 'off'] else 'off')
            value_frame = ttk.Frame(frame)
            value_frame.pack(pady=5)
            
            ttk.Radiobutton(value_frame, text="Ligado", variable=value_var, value="on").pack(side=tk.LEFT, padx=5)
            ttk.Radiobutton(value_frame, text="Desligado", variable=value_var, value="off").pack(side=tk.LEFT, padx=5)
        
        elif 'airtemp' in device_name:
            # Para temperatura
            value_var = tk.StringVar(value=current_value if current_value != 'N/A' else '22.0')
            entry_frame = ttk.Frame(frame)
            entry_frame.pack(pady=5)
            
            ttk.Entry(entry_frame, textvariable=value_var, width=10).pack(side=tk.LEFT, padx=5)
            ttk.Label(entry_frame, text="°C").pack(side=tk.LEFT)
        
        else:
            # Entrada genérica
            value_var = tk.StringVar(value=current_value if current_value != 'N/A' else '')
            ttk.Entry(frame, textvariable=value_var, width=20).pack(pady=5)
        
        # Botões
        button_frame = ttk.Frame(frame)
        button_frame.pack(pady=10)
        
        def apply_change():
            new_value = value_var.get()
            
            # Validar valor para temperatura
            if 'airtemp' in device_name:
                try:
                    float(new_value)
                except ValueError:
                    messagebox.showerror("Erro", "Valor de temperatura deve ser numérico")
                    return
            
            if self.set_device_value(device_name, new_value):
                control_window.destroy()
        
        ttk.Button(button_frame, text="Aplicar", command=apply_change).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancelar", command=control_window.destroy).pack(side=tk.LEFT, padx=5)
    
    def toggle_monitoring(self):
        """Inicia/para o monitoramento automático"""
        if not self.monitoring:
            try:
                self.monitor_interval = int(self.interval_var.get())
                if self.monitor_interval < 1:
                    raise ValueError("Intervalo deve ser maior que 0")
            except ValueError:
                messagebox.showerror("Erro", "Intervalo deve ser um número inteiro positivo")
                return
            
            self.monitoring = True
            self.monitor_button.config(text="Parar Monitoramento")
            self.log_message(f"Monitoramento iniciado (intervalo: {self.monitor_interval}s)")
            
            # Iniciar thread de monitoramento
            self.monitor_thread = threading.Thread(target=self.monitor_loop)
            self.monitor_thread.daemon = True
            self.monitor_thread.start()
        else:
            self.monitoring = False
            self.monitor_button.config(text="Iniciar Monitoramento")
            self.log_message("Monitoramento parado")
    
    def monitor_loop(self):
        """Loop de monitoramento"""
        while self.monitoring:
            self.get_all_values()
            time.sleep(self.monitor_interval)
    
    def run(self):
        """Executa a aplicação"""
        self.log_message("Cliente de monitoramento iniciado")
        self.log_message("Duplo clique em um atuador para controlá-lo")
        
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.log_message("Aplicação encerrada pelo usuário")
        finally:
            self.monitoring = False
            self.socket.close()

if __name__ == "__main__":
    client = MonitoringClient()
    client.run()