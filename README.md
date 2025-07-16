# 🖧 AVALIAÇÃO 3 - REDES DE COMPUTADORES I

Implementação das Partes 1, 2 e 3 do projeto prático da disciplina Redes
de Computadores I.

**Autor**: Nathaniel Christian Silva Alves 

**Professor**: Robson Costa

**Curso**: Ciência da Computação – 3ª fase / 2025.1

## PARTE 1: Chat Multicast com UDP

### **Objetivo**:

Sistema de bate-papo que utiliza UDP com Multicast, com mensagens em
JSON e threads separadas para envio e recebimento.

### **Arquivo**:

* `udp_multicast_chat.py`

### **Como executar** :

* Execute o script em dois terminais diferentes: 
    ```bash
    python udp_multicast_chat.py
    ```

* Digite o nome de usuário quando solicitado. Envie mensagens e veja a comunicação em tempo real entre usuários.

### **Funcionalidades** : 

* Comunicação via Multicast UDP

* Threads paralelas para envio e recebimento simultâneo

* Mensagens com formato JSON:

    ```JSON
    {   
        "date": "dd/mm/aaaa", 
        "time": "hh:mm:ss", 
        "username": "usuario",
        "message": "mensagem" 
    }
    ```

## PARTE 2: Servidor de Arquivos TCP com Protocolo JSON

### **Objetivo** :

* Sistema cliente-servidor para transferência de arquivos com protocolo próprio baseado em JSON e uso de TCP.

### **Arquivos** :

* `tcp_file_server.py` – Servidor

* `tcp_file_client.py` – Cliente

### **Como executar** :

* Inicie o servidor: 
    ```bash
    python tcp_file_server.py
    ```
  - Cria a pasta server_files automaticamente.

* Execute o cliente: 
    ```bash
    python tcp_file_client.py
    ```
### **Funcionalidades** :

* **LIST_REQ / LIST_RESP** : Lista arquivos no servidor

* **PUT_REQ / PUT_RESP**: Envia arquivo ao servidor

* **GET_REQ / GET_RESP**: Baixa arquivo do servidor

* Verificação de integridade com **SHA-256**

* Arquivos codificados em **Base64**

* Suporte a múltiplos clientes com **multi-threading**

##  PARTE 3: Sistema de Monitoramento e Controle com UDP + Interface Gráfica

### **Objetivo** :

* Sistema de monitoramento e controle remoto de dispositivos (IoT) com UDP e mensagens em JSON, incluindo uma interface gráfica no cliente.

### **Arquivos** :

* `udp_monitoring_server.py` – Servidor de monitoramento

* `udp_monitoring_client.py` – Cliente com interface gráfica

* `server_config.json` – Arquivo de configuração dos dispositivos

### **Como executar** :

Certifique-se de que server_config.json esteja no mesmo diretório do servidor.

* Inicie o servidor: 
    ```bash
    python udp_monitoring_server.py
    ```

* Execute o cliente: 
    ```Bash
    python udp_monitoring_client.py
    ```
### **Funcionalidades** :

* #### Servidor:
    ---
    * **list_req / list_resp** : Lista dispositivos e ambientes

    * **get_req / get_resp** : Consulta estado/valor de dispositivos

    * **set_req / set_resp** : Altera valores de atuadores

    * Leitura da configuração inicial via JSON

    * Simulação de sensores de forma automática

    * **Validação de tipo** : sensores (somente leitura), atuadores (controle)

* #### Cliente:
    ---
    * Interface gráfica (Tkinter)

    * Visualização em tempo real de todos os dispositivos

    * Comando duplo clique para controle dos atuadores

    * Atualização periódica com intervalo configurável

    * Log de operações

### **Dispositivos suportados** :
| Tipo      | Dispositivo               | Exemplo |    
| :-------- | :-----------              | :-----: |
| Sensor    | Temperatura               | `sensor_airtemp_meetroom` 
| Sensor    |Umidade                    |`sensor_airhumid_meetroom` |
| Atuador   |Luz                        |`actuator_light_meetroom` |
| Atuador   |Ar-condicionado (on/off)   | `actuator_air_guarita` |
| Atuador   |Temperatura (numérico)     | `actuator_airtemp_guarita`|

## Instruções de Teste:

### Parte 1:

* Execute o chat em dois terminais e teste o envio simultâneo.

* Confirme o recebimento das mensagens com formato correto.

### Parte 2:

* Crie arquivos de teste locais.

* Faça upload e verifique a existência no diretório do servidor.

* Faça download e compare o hash.

### Parte 3:

* Execute o servidor e o cliente.

* Teste os comandos LIST, GET, SET diretamente pela interface gráfica.

* Altere estados e valores de atuadores e verifique persistência.

* Valide a simulação automática dos sensores.

## Requisitos:

* Python 3.6+

Bibliotecas: `socket`, `json`, `threading`, `hashlib`, `base64`,`os`, `time`, `datetime`, `tkinter`

---
