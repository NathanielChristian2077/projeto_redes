import socket
import json
import base64
import hashlib
import os

class FileClient:
    def __init__(self, host='localhost', port=8080):
        self.host = host
        self.port = port
        self.client_dir = 'client_files'
        
        # Criar diretório do cliente se não existir
        if not os.path.exists(self.client_dir):
            os.makedirs(self.client_dir)
    
    def calculate_hash(self, data):
        """Calcula hash SHA-256 dos dados"""
        return hashlib.sha256(data).hexdigest()
    
    def connect_to_server(self):
        """Conecta ao servidor"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            return True
        except Exception as e:
            print(f"Erro ao conectar ao servidor: {e}")
            return False
    
    def send_request(self, request):
        """Envia requisição e recebe resposta"""
        try:
            request_json = json.dumps(request)
            self.socket.send(request_json.encode('utf-8'))
            
            response = self.socket.recv(65536).decode('utf-8')
            return json.loads(response)
        except Exception as e:
            print(f"Erro na comunicação: {e}")
            return None
    
    def list_files(self):
        """Lista arquivos do servidor"""
        request = {"cmd": "list_req"}
        response = self.send_request(request)
        
        if response and response.get('cmd') == 'list_resp':
            files = response.get('files', [])
            print(f"\nArquivos no servidor ({len(files)}):")
            for i, file in enumerate(files, 1):
                print(f"{i}. {file}")
            return files
        else:
            print("Erro ao listar arquivos")
            return []
    
    def upload_file(self, file_path):
        """Faz upload de um arquivo"""
        if not os.path.exists(file_path):
            print(f"Arquivo não encontrado: {file_path}")
            return False
        
        try:
            # Ler arquivo
            with open(file_path, 'rb') as f:
                file_bytes = f.read()
            
            # Calcular hash e codificar em base64
            file_hash = self.calculate_hash(file_bytes)
            file_base64 = base64.b64encode(file_bytes).decode('utf-8')
            file_name = os.path.basename(file_path)
            
            request = {
                "cmd": "put_req",
                "file": file_name,
                "hash": file_hash,
                "value": file_base64
            }
            
            print(f"Enviando arquivo {file_name}...")
            response = self.send_request(request)
            
            if response and response.get('cmd') == 'put_resp':
                status = response.get('status')
                if status == 'ok':
                    print(f"Arquivo {file_name} enviado com sucesso!")
                    return True
                else:
                    print(f"Falha ao enviar arquivo {file_name}")
                    return False
            else:
                print("Erro na resposta do servidor")
                return False
                
        except Exception as e:
            print(f"Erro ao fazer upload: {e}")
            return False
    
    def download_file(self, file_name):
        """Faz download de um arquivo"""
        request = {
            "cmd": "get_req",
            "file": file_name
        }
        
        print(f"Baixando arquivo {file_name}...")
        response = self.send_request(request)
        
        if response and response.get('cmd') == 'get_resp':
            file_hash = response.get('hash')
            file_base64 = response.get('value')
            
            if not file_hash or not file_base64:
                print(f"Arquivo {file_name} não encontrado no servidor")
                return False
            
            try:
                # Decodificar arquivo
                file_bytes = base64.b64decode(file_base64)
                
                # Verificar integridade
                calculated_hash = self.calculate_hash(file_bytes)
                if calculated_hash != file_hash:
                    print("Erro: Arquivo corrompido!")
                    return False
                
                # Salvar arquivo
                file_path = os.path.join(self.client_dir, file_name)
                with open(file_path, 'wb') as f:
                    f.write(file_bytes)
                
                print(f"Arquivo {file_name} baixado com sucesso!")
                print(f"Salvo em: {os.path.abspath(file_path)}")
                return True
                
            except Exception as e:
                print(f"Erro ao processar arquivo: {e}")
                return False
        else:
            print("Erro na resposta do servidor")
            return False
    
    def disconnect(self):
        """Desconecta do servidor"""
        if hasattr(self, 'socket'):
            self.socket.close()
    
    def run_interactive(self):
        """Executa interface interativa"""
        if not self.connect_to_server():
            return
        
        try:
            while True:
                print("\n=== CLIENTE DE ARQUIVOS ===")
                print("1. Listar arquivos do servidor")
                print("2. Fazer upload de arquivo")
                print("3. Fazer download de arquivo")
                print("4. Sair")
                
                choice = input("\nEscolha uma opção: ").strip()
                
                if choice == '1':
                    self.list_files()
                
                elif choice == '2':
                    file_path = input("Digite o caminho do arquivo para upload: ").strip()
                    if file_path:
                        self.upload_file(file_path)
                
                elif choice == '3':
                    # Primeiro listar arquivos disponíveis
                    files = self.list_files()
                    if files:
                        file_name = input("Digite o nome do arquivo para download: ").strip()
                        if file_name:
                            self.download_file(file_name)
                
                elif choice == '4':
                    print("Saindo...")
                    break
                
                else:
                    print("Opção inválida!")
        
        except KeyboardInterrupt:
            print("\nCliente encerrado pelo usuário")
        finally:
            self.disconnect()

if __name__ == "__main__":
    client = FileClient()
    client.run_interactive()