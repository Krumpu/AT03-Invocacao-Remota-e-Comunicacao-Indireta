import socket
import json
import time

HOST = '127.0.0.1'
PORT = 5000

def enviar_requisicao(dados):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
            # Serializa o dicionário python para texto JSON e envia bytes
            msg = json.dumps(dados)
            s.sendall(msg.encode('utf-8'))
            
            data = s.recv(1024)
            resposta = json.loads(data.decode('utf-8'))
            return resposta['resultado']
        except ConnectionRefusedError:
            return "Erro: Não foi possível conectar ao servidor."

def menu():
    while True:
        print("\n--- CALCULADORA DISTRIBUÍDA (SOCKET) ---")
        print("1. Soma (+)")
        print("2. Subtração (-)")
        print("3. Multiplicação (*)")
        print("4. Divisão (/)")
        print("5. Enviar Expressão Completa (Ex: (10+5)*2)")
        print("0. Sair")
        
        escolha = input("Escolha uma opção: ")
        
        if escolha == '0': break
        
        req = {}
        
        if escolha in ['1', '2', '3', '4']:
            try:
                v1 = float(input("Valor 1: "))
                v2 = float(input("Valor 2: "))
                op_map = {'1': 'soma', '2': 'subtracao', '3': 'multiplicacao', '4': 'divisao'}
                req = {"operacao": op_map[escolha], "valor1": v1, "valor2": v2}
            except ValueError:
                print("Por favor, digite números válidos.")
                continue
                
        elif escolha == '5':
            expr = input("Digite a expressão matemática: ")
            req = {"operacao": "expressao", "valor1": expr, "valor2": 0} # valor2 ignorado
        else:
            print("Opção inválida.")
            continue

        # Envia para o servidor e mede tempo (útil para o relatório depois)
        inicio = time.time()
        resultado = enviar_requisicao(req)
        fim = time.time()
        
        print(f"\n>> RESULTADO: {resultado}")
        print(f">> Tempo de resposta: {(fim-inicio)*1000:.2f} ms")

if __name__ == "__main__":
    menu()