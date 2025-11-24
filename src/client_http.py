import requests
import time
import sys

# URL do servidor (Porta 5001)
URL = "http://localhost:5001/calcular"

def enviar_requisicao(payload):
    """
    Envia POST com política de RETRY (Wait Ts and Retry).
    Se falhar, espera 3 segundos e tenta de novo, até 3 vezes.
    """
    MAX_TENTATIVAS = 3
    TEMPO_ESPERA = 3  # segundos (Ts)

    for tentativa in range(1, MAX_TENTATIVAS + 1):
        try:
            print(f"Disparando requisição (Tentativa {tentativa}/{MAX_TENTATIVAS})...")
            
            # Timeout curto para não travar se o servidor estiver lento
            resposta = requests.post(URL, json=payload, timeout=5)
            
            # Se conectou, verifica se deu 200 OK
            if resposta.status_code == 200:
                dados = resposta.json()
                return dados.get("resultado")
            else:
                return f"Erro do Servidor: {resposta.status_code} - {resposta.text}"

        except requests.exceptions.ConnectionError:
            print(f"[!] Falha de conexão na tentativa {tentativa}.")
            if tentativa < MAX_TENTATIVAS:
                print(f"[!] Servidor indisponível. Esperando {TEMPO_ESPERA}s para tentar novamente...")
                time.sleep(TEMPO_ESPERA)
            else:
                return "ERRO FATAL: Servidor inalcançável após várias tentativas."
        except Exception as e:
            return f"Erro desconhecido: {e}"

def menu():
    while True:
        print("\n--- CALCULADORA HTTP (REST + Retry) ---")
        print("1. Soma (+)")
        print("2. Subtração (-)")
        print("3. Multiplicação (*)")
        print("4. Divisão (/)")
        print("5. Expressão")
        print("0. Sair")

        opcao = input("Opção: ")
        if opcao == '0': break

        payload = {}
        
        # Monta o JSON baseada na escolha
        if opcao in ['1', '2', '3', '4']:
            try:
                v1 = float(input("Valor 1: "))
                v2 = float(input("Valor 2: "))
                mapa = {'1': 'soma', '2': 'subtracao', '3': 'multiplicacao', '4': 'divisao'}
                payload = {"operacao": mapa[opcao], "valor1": v1, "valor2": v2}
            except ValueError:
                print("Valores inválidos.")
                continue
        elif opcao == '5':
            expr = input("Expressão: ")
            payload = {"operacao": "expressao", "valor1": expr}
        else:
            continue

        # Chama a função com Retry
        resultado = enviar_requisicao(payload)
        print(f"\n>> RESULTADO FINAL: {resultado}")

if __name__ == "__main__":
    menu()