import socket
import json
import base64
import hashlib
import os
import threading
from datetime import datetime

class FileServer:
    def __init__(self, host='localhost', port=8080):
        self.host = host
        self.port = port
        self.server_dir = 'server_files'
        
        # Criar diretório do servidor se não existir
        if not os.path.exists(self.server_dir):
            os.makedirs(self.server_dir)
    
    def calculate_hash(self, data):
        """Calcula hash SHA-256 dos dados"""
        return hashlib.sha256(data).hexdigest()
    
    def handle_list_req(self):
        """Processa solicitação LIST_REQ"""
        try:
            files = os.listdir(self.server_dir)
            response = {
                "cmd": "list_resp",
                "files": files
            }
            return json.dumps(response)
        except Exception as e:
            print(f"Erro ao listar arquivos: {e}")
            return json.dumps({"cmd": "list_resp", "files": []})
    
    def handle_put_req(self, data):
        """Processa solicitação PUT_REQ"""
        try:
            file_name = data['file']
            file_hash = data['hash']
            file_base64 = data['value']
            
            # Decodificar arquivo
            file_bytes = base64.b64decode(file_base64)
            
            # Verificar integridade
            calculated_hash = self.calculate_hash(file_bytes)
            if calculated_hash != file_hash:
                return json.dumps({
                    "cmd": "put_resp",
                    "file": file_name,
                    "status": "fail"
                })
            
            # Salvar arquivo
            file_path = os.path.join(self.server_dir, file_name)
            with open(file_path, 'wb') as f:
                f.write(file_bytes)
            
            print(f"Arquivo {file_name} recebido e salvo com sucesso")
            
            return json.dumps({
                "cmd": "put_resp",
                "file": file_name,
                "status": "ok"
            })
            
        except Exception as e:
            print(f"Erro ao processar PUT_REQ: {e}")
            return json.dumps({
                "cmd": "put_resp",
                "file": data.get('file', 'unknown'),
                "status": "fail"
            })
    
    def handle_get_req(self, data):
        """Processa solicitação GET_REQ"""
        try:
            file_name = data['file']
            file_path = os.path.join(self.server_dir, file_name)
            
            if not os.path.exists(file_path):
                return json.dumps({
                    "cmd": "get_resp",
                    "file": file_name,
                    "hash": "",
                    "value": ""
                })
            
            # Ler arquivo
            with open(file_path, 'rb') as f:
                file_bytes = f.read()
            
            # Calcular hash e codificar em base64
            file_hash = self.calculate_hash(file_bytes)
            file_base64 = base64.b64encode(file_bytes).decode('utf-8')
            
            print(f"Enviando arquivo {file_name}")
            
            return json.dumps({
                "cmd": "get_resp",
                "file": file_name,
                "hash": file_hash,
                "value": file_base64
            })
            
        except Exception as e:
            print(f"Erro ao processar GET_REQ: {e}")
            return json.dumps({
                "cmd": "get_resp",
                "file": data.get('file', 'unknown'),
                "hash": "",
                "value": ""
            })
    
    def handle_client(self, client_socket, address):
        """Processa conexão do cliente"""
        print(f"Cliente conectado: {address}")
        
        try:
            while True:
                # Receber dados do cliente
                data = client_socket.recv(4096).decode('utf-8')
                if not data:
                    break
                
                print(f"Recebido de {address}: {data[:100]}...")
                
                try:
                    request = json.loads(data)
                    cmd = request.get('cmd')
                    
                    if cmd == 'list_req':
                        response = self.handle_list_req()
                    elif cmd == 'put_req':
                        response = self.handle_put_req(request)
                    elif cmd == 'get_req':
                        response = self.handle_get_req(request)
                    else:
                        response = json.dumps({"error": "Comando não reconhecido"})
                    
                    # Enviar resposta
                    client_socket.send(response.encode('utf-8'))
                    
                except json.JSONDecodeError:
                    error_response = json.dumps({"error": "JSON inválido"})
                    client_socket.send(error_response.encode('utf-8'))
                
        except Exception as e:
            print(f"Erro ao processar cliente {address}: {e}")
        finally:
            client_socket.close()
            print(f"Cliente {address} desconectado")
    
    def start_server(self):
        """Inicia o servidor"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((self.host, self.port))
            server_socket.listen(5)
            
            print(f"Servidor iniciado em {self.host}:{self.port}")
            print(f"Diretório de arquivos: {os.path.abspath(self.server_dir)}")
            
            while True:
                client_socket, address = server_socket.accept()
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, address)
                )
                client_thread.daemon = True
                client_thread.start()

if __name__ == "__main__":
    server = FileServer()
    try:
        server.start_server()
    except KeyboardInterrupt:
        print("\nServidor encerrado pelo usuário")