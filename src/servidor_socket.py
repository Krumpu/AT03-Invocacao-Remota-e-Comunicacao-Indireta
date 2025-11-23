import socket
import json
from calculadora import CalculadoraLogica


#Setup do servidor
HOST = '127.0.0.1'  
PORT = 5000         

def iniciar_servidor():
    calc = CalculadoraLogica()
    
    #Setup de servidor IPv4, indicação de protocolo TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Servidor Socket ouvindo em {HOST}:{PORT}...")

        while True:
            conn, addr = s.accept() 
            with conn:
                print(f"Conectado por: {addr}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    
                    
                    requisicao = json.loads(data.decode('utf-8'))
                    op = requisicao.get('operacao')
                    resp = None

                    #Setor que determina a operação realizada com base no recebido pelo servidor.
                    try:
                        if op == 'expressao':
                            resp = calc.resolver_expressao(requisicao['valor1'])
                        else:
                           
                            a = float(requisicao['valor1'])
                            b = float(requisicao['valor2'])
                            
                            if op == 'soma': resp = calc.somar(a, b)
                            elif op == 'subtracao': resp = calc.subtrair(a, b)
                            elif op == 'multiplicacao': resp = calc.multiplicar(a, b)
                            elif op == 'divisao': resp = calc.dividir(a, b)
                    except Exception as e:
                        resp = f"Erro no servidor: {str(e)}"

                    resposta_json = json.dumps({"resultado": resp})
                    conn.sendall(resposta_json.encode('utf-8'))

if __name__ == "__main__":
    iniciar_servidor()