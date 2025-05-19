# AVALIAÇÃO 3
- ## (Parte 1/3)
    - ### 1. IDENTIFICAÇÃO
       - ### CURSO: CIÊNCIA DA COMPUTAÇÃO FASE: 3ª ANO/SEMESTRE: 2025/1
       - ### DISCIPLINA: REDES DE COMPUTADORES I (RCA)
       - ### PROFESSOR: ROBSON COSTA DATA: 07/04/2024
Com base nos conceitos apresentados em aula e utilizando a linguagem de programação de
(sua preferência crie um programa de bate papo chat) :contendo as seguintes especificações
• , ;somente um programa será desenvolvido sendo este capaz de enviar e receber mensagens
◦ obs.: ,para o envio e recebimento de mensagens de forma simultânea a mesma porta de
,comunicação pode ser utilizada porém o envio e recebimento devem ser tratados em threads
;distintas
• a comunicação entre os nós comunicantes deve ser realizada obrigatoriamente via multicast;
◦ obs.: o padrão multicast ;exige a utilização do protocolo UDP
• o payload ( )carga útil da mensagem deve estar no formato JSON e seguir rigorosamente
o seguinte layout:
{
"date":"date_value",
"time":"time_value",
"username":"username_value",
"message":"message_value"
}
:onde
date_value ( / / ) ( );é a data dd mm aaaa de envio da mensagem obtida no nó origem
time_value ( : : ) ( );é a hora hh mm ss de envio da mensagem obtida no nó origem
username_value ;é o nome do usuário que enviou a mensagem
message_value ;é a mensagem em si
Instituto Federal de Santa Catarina – Câmpus Lages
Rua: Heitor Vila Lobos, 225 | São Francisco | Lages / SC | CEP: 88.506-400
Fone: (49) 3221-4200 | www.ifsc.edu.br | CNPJ 11.402.887/0011-32
p. 1/5
AVALIAÇÃO 3
(Parte 2/3)
1. IDENTIFICAÇÃO
CURSO: CIÊNCIA DA COMPUTAÇÃO FASE: 3ª ANO/SEMESTRE: 2025/1
DISCIPLINA: ( )REDES DE COMPUTADORES I RCA
PROFESSOR: ROBSON COSTA DATA: 07/05/2024
Utilizando o protocolo da camada de transporte TCP desenvolva um cliente e um servidor de
( ). ,arquivos similar ao servidor FTP Porém em vez de utilizar o protocolo FTP na camada de
, .aplicação você desenvolverá o seu próprio protocolo baseado no formato JSON Para fins de
, ( ).simplificação esta versão do servidor não suportará a criação e navegação de diretórios pastas
, :Sendo assim o servidor e o cliente devem operar com os seguintes comandos
• LIST_REQ – ;cliente solicita a lista de todos os arquivos armazenados no servidor
{
"cmd":"list_req",
}
• LIST_RESP – servidor envia ao cliente a lista de todos os arquivos armazenados no
;servidor
{
"cmd":"list_resp",
"files":"<file_list_vector>",
}
• PUT_REQ <file> – cliente envia ao servidor o arquivo definido em <file>;
{
"cmd":"put_req",
"file":"<file_name>",
"hash":"<hash_value>",
"value":"<file_byte_base64>",
}
• PUT_RESP – servidor envia ao cliente a confirmação de upload do arquivo <file>;
{
"cmd":"put_resp",
"file":"<file_name>",
"status":"<ok/fail>",
}
• GET_REQ <file> – cliente solicita o download do <file> armazenado no servidor;
{
"cmd":"get_req",
"file":"<file_name>",
}
• GET_RESP – servidor envia ao cliente o arquivo definido em <file>;
{
"cmd":"get_resp",
"file":"<file_name>",
"hash":"<hash_value>",
"value":"<file_byte_base64>",
}
Instituto Federal de Santa Catarina – Câmpus Lages
Rua: Heitor Vila Lobos, 225 | São Francisco | Lages / SC | CEP: 88.506-400
Fone: (49) 3221-4200 | www.ifsc.edu.br | CNPJ 11.402.887/0011-32
p. 2/5
AVALIAÇÃO 3
(Parte 3/3)
1. IDENTIFICAÇÃO
CURSO: CIÊNCIA DA COMPUTAÇÃO FASE: 3ª ANO/SEMESTRE: 2024/1
DISCIPLINA: ( )REDES DE COMPUTADORES I RCA
PROFESSOR: ROBSON COSTA DATA: 02/05/2024
Imagine que você trabalha em uma empresa de desenvolvimento de software e que em uma
:reunião com um dos clientes da empresa este relata o seguinte problema
“...Temos diversas filiais e estamos tendo um gasto excessivo de energia elétrica por conta de luzes
e aparelhos de ar-condicionado que se mantém ligados em horários os quais não há nenhum
funcionário na empresa. Gostaria de uma solução que nos permitisse monitorá-los, desligá-los e
ligá-los tudo remotamente...”
, &Diante deste relato a sua gerente de PD I solicita que você desenvolva uma solução que
. - ,resolva o problema do cliente Ao planejá la você chega a conclusão de que precisará criar um
software servidor que irá ser executado em cada filial e que terá sensores e atuadores ligados nele
(para a obtenção do estado e a realização de ações a parte do sensoriamento e acionamento será
). , ,abstraída do trabalho De forma complementar será necessário criar um software cliente que irá ser
, (executado na matriz da empresa e enviará solicitações de estado verificar qual o estado de alguns
) ( , , / )dispositivos e comandos liga desliga altera o valor o do dispositivos para que seja possível a
.realização do monitoramento e controle de forma remota Também se concluiu que por motivo de
,simplificação o protocolo de transporte a ser utilizado deverá ser o UDP e que o layout dos dados
. ,contidos na camada de aplicação será baseado em JSON Para simplificar assuma que somente exite
1 .filial e a matriz
:O servidor deve ser capaz de responder aos seguintes comandos do cliente
• LIST – ;lista todos os ambientes e seus respectivos sensores e atuadores da filial
• GET – / ;obtém o estado valor atual de um dispositivo
• SET – / ;altera o estado valor atual de um dispositivo
:Abaixo é apresentado uma lista de exemplos de operação
Obtenção da lista de ambientes monitorados/controlados na filial:
• :Cliente envia
{
"cmd":"list_req"
}
• :Servidor responde
{
"cmd":"list_resp",
"place":"[sensor_actuator_vector]",
}
sensor_actuator_vector – é uma lista com as chaves de sensores e atuadores contendo o
:seguinte layout <type>_<device>_<place> onde <type> (é o tipo sensor/actuator),
<device> é o dispositivo e <place> .é o local
Instituto Federal de Santa Catarina – Câmpus Lages
Rua: Heitor Vila Lobos, 225 | São Francisco | Lages / SC | CEP: 88.506-400
Fone: (49) 3221-4200 | www.ifsc.edu.br | CNPJ 11.402.887/0011-32
p. 3/5
Obtenção do estado das luzes da sala de reuniões:
• :Cliente envia
{
"cmd":"get_req",
"place":"actuator_light_meetroom",
}
• :Servidor responde
{
"cmd":"get_resp",
"place":"actuator_light_meetroom",
"value":"on",
}
Obtenção da temperatura na sala de reuniões:
• :Cliente envia
{
"cmd":"get_req",
"place":"sensor_airtemp_meetroom",
}
• :Servidor responde
{
"cmd":"get_resp",
"place":"sensor_airtemp_meetroom",
"value": 22.3,
}
Obtenção de todos os valores atuais de todos os lugares:
• :Cliente envia
{
"cmd":"get_req",
"place":"all",
}
• :Servidor responde
{
"cmd":"get_resp",
"place":"[sensor_actuator_vector_name]",
"value":"[values_vector]",
}
Desligamento do ar-condicionado da guarita:
• :Cliente envia
{
"cmd":"set_req",
"locate":"actuator_air_guarita",
"value":"off",
}
Instituto Federal de Santa Catarina – Câmpus Lages
Rua: Heitor Vila Lobos, 225 | São Francisco | Lages / SC | CEP: 88.506-400
Fone: (49) 3221-4200 | www.ifsc.edu.br | CNPJ 11.402.887/0011-32
p. 4/5
• :Servidor responde
{
"cmd":"set_resp",
"locate":"actuator_air_guarita",
"value":"off",
}
Alteração da temperatura do ar-condicionado da guarita:
• :Cliente envia
{
"cmd":"set_req",
"locate":"actuator_airtemp_guarita",
"value":23.0,
}
• :Servidor responde
{
"cmd":"set_resp",
"locate":"actuator_airtemp_guarita",
"value":23.0,
}
Somente é possível realizar a alteração de valores de dispositivos do tipo actuator. Os
dispositivos do tipo sensor .são de somente leitura
O software cliente deve ser capaz de ser configurado para enviar solicitações periódicas
( )período configurável pelo usuário de valores .para todos os equipamentos listados pela filial Além
,disso ele deve obrigatoriamente ter um ambiente gráfico para a visualização de dados e interação
.com o usuário
, . ,No caso do software do servidor a criação de uma interface gráfica é opcional No entanto
este deve carregar a lista de ambientes e valores padrão1 a partir de um arquivo de configuração no
, :formato JSON conforme o exemplo abaixo
{
"actuator_light_meetroom":"off",
"sensor_airtemp_meetroom":0.0,
"sensor_airhumid_meetroom":0.0,
"actuator_airtemp_guarita":23.0,
}
OBS:
• ;o desenvolvimento pode ser realizado em dupla
• ;poderá ser utilizada a linguagem de programação de sua preferência
• (a nota será individual e baseada na apresentação acerca do código fonte e lógica de progra-
) ;mação utilizada em sala de aula em data a ser agendada pelo professor
• :no momento da apresentação será solicitado
◦ ;a abertura e explicação do código fonte
◦ a execução e demonstração dos algoritmos;
1 Os valores padrão são definidos apenas para dispositivos do tipo actuator, para dispositivos do tipo sensor, o
valor é fornecido pelo sistema de aquisição de dados (abstraído neste trabalho).
Instituto Federal de Santa Catarina – Câmpus Lages
Rua: Heitor Vila Lobos, 225 | São Francisco | Lages / SC | CEP: 88.506-400
Fone: (49) 3221-4200 | www.ifsc.edu.br | CNPJ 11.402.887/0011-32
p. 5/5
