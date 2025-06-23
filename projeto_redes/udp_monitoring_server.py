import socket
import json
import threading
import time
import random
from datetime import datetime

class MonitoringServer:
    def __init__(self, host='localhost', port=9090, config_file='server_config.json'):
        self.host = host
        self.port = port
        self.config_file = config_file
        self.devices = {}
        self.running = False
        
        # Carregar configuração inicial
        self.load_config()
        
        # Iniciar thread de simulação de sensores
        self.sensor_thread = threading.Thread(target=self.simulate_sensors)
        self.sensor_thread.daemon = True
    
    def load_config(self):
        """Carrega configuração do arquivo JSON"""
        try:
            with open(self.config_file, 'r') as f:
                self.devices = json.load(f)
            print(f"Configuração carregada: {len(self.devices)} dispositivos")
            
            # Exibir dispositivos carregados
            for device, value in self.devices.items():
                print(f"  {device}: {value}")
                
        except FileNotFoundError:
            print(f"Arquivo de configuração não encontrado: {self.config_file}")
            print("Criando configuração padrão...")
            self.create_default_config()
        except json.JSONDecodeError:
            print("Erro ao decodificar arquivo de configuração")
            self.create_default_config()
    
    def create_default_config(self):
        """Cria configuração padrão"""
        self.devices = {
            "actuator_light_meetroom": "off",
            "sensor_airtemp_meetroom": 22.5,
            "sensor_airhumid_meetroom": 60.0,
            "actuator_airtemp_guarita": 23.0,
            "actuator_air_guarita": "on",
            "sensor_airtemp_guarita": 23.0,
            "actuator_light_reception": "on",
            "sensor_airtemp_reception": 21.0,
            "sensor_airhumid_reception": 55.0
        }
        
        # Salvar configuração padrão
        with open(self.config_file, 'w') as f:
            json.dump(self.devices, f, indent=2)
        
        print("Configuração padrão criada e salva")
    
    def simulate_sensors(self):
        """Simula leituras de sensores"""
        while self.running:
            for device_name, value in self.devices.items():
                if device_name.startswith('sensor_'):
                    # Simular variação nos sensores
                    if 'airtemp' in device_name:
                        # Temperatura varia entre 18-28°C
                        self.devices[device_name] = round(random.uniform(18.0, 28.0), 1)
                    elif 'airhumid' in device_name:
                        # Umidade varia entre 40-80%
                        self.devices[device_name] = round(random.uniform(40.0, 80.0), 1)
            
            time.sleep(30)  # Atualizar a cada 30 segundos
    
    def handle_list_req(self):
        """Processa comando LIST"""
        device_list = list(self.devices.keys())
        response = {
            "cmd": "list_resp",
            "place": device_list
        }
        return json.dumps(response)
    
    def handle_get_req(self, data):
        """Processa comando GET"""
        place = data.get('place')
        
        if place == 'all':
            # Retornar todos os valores
            device_names = list(self.devices.keys())
            values = list(self.devices.values())
            response = {
                "cmd": "get_resp",
                "place": device_names,
                "value": values
            }
        else:
            # Retornar valor específico
            value = self.devices.get(place, "device_not_found")
            response = {
                "cmd": "get_resp",
                "place": place,
                "value": value
            }
        
        return json.dumps(response)
    
    def handle_set_req(self, data):
        """Processa comando SET"""
        locate = data.get('locate')
        value = data.get('value')
        
        # Verificar se é um atuador
        if not locate.startswith('actuator_'):
            response = {
                "cmd": "set_resp",
                "locate": locate,
                "value": "error: read_only_device"
            }
        elif locate in self.devices:
            # Atualizar valor do atuador
            self.devices[locate] = value
            
            # Salvar configuração atualizada
            try:
                with open(self.config_file, 'w') as f:
                    json.dump(self.devices, f, indent=2)
            except Exception as e:
                print(f"Erro ao salvar configuração: {e}")
            
            response = {
                "cmd": "set_resp",
                "locate": locate,
                "value": value
            }
            
            print(f"Dispositivo {locate} alterado para: {value}")
        else:
            response = {
                "cmd": "set_resp",
                "locate": locate,
                "value": "error: device_not_found"
            }
        
        return json.dumps(response)
    
    def process_request(self, data, address):
        """Processa requisição do cliente"""
        try:
            request = json.loads(data)
            cmd = request.get('cmd')
            
            print(f"Comando recebido de {address}: {cmd}")
            
            if cmd == 'list_req':
                response = self.handle_list_req()
            elif cmd == 'get_req':
                response = self.handle_get_req(request)
            elif cmd == 'set_req':
                response = self.handle_set_req(request)
            else:
                response = json.dumps({"error": "Comando não reconhecido"})
            
            return response
            
        except json.JSONDecodeError:
            return json.dumps({"error": "JSON inválido"})
        except Exception as e:
            print(f"Erro ao processar requisição: {e}")
            return json.dumps({"error": "Erro interno do servidor"})
    
    def start_server(self):
        """Inicia o servidor UDP"""
        self.running = True
        
        # Iniciar simulação de sensores
        self.sensor_thread.start()
        
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
            server_socket.bind((self.host, self.port))
            
            print(f"Servidor de monitoramento iniciado em {self.host}:{self.port}")
            print(f"Arquivo de configuração: {self.config_file}")
            print("Aguardando requisições...\n")
            
            try:
                while self.running:
                    # Receber dados do cliente
                    data, address = server_socket.recvfrom(1024)
                    
                    # Processar requisição
                    response = self.process_request(data.decode('utf-8'), address)
                    
                    # Enviar resposta
                    server_socket.sendto(response.encode('utf-8'), address)
                    
            except KeyboardInterrupt:
                print("\nServidor encerrado pelo usuário")
            finally:
                self.running = False

if __name__ == "__main__":
    server = MonitoringServer()
    server.start_server()