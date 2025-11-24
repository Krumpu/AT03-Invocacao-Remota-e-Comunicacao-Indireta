# cliente_rmi.py
import Pyro4
import sys

Pyro4.config.SERIALIZER = "pickle"

def menu():
    # 1. Conecta ao objeto remoto usando o URI fixo que definimos no servidor
    try:
        calc = Pyro4.Proxy("PYRO:calculadora@localhost:9090")
        calc._pyroBind() 
    except Exception as e:
        print(f"Erro ao conectar no servidor RMI: {e}")
        return

    while True:
        print("\n--- CALCULADORA DISTRIBUÍDA (RMI/Pyro4) ---")
        print("1. Soma (+)")
        print("2. Subtração (-)")
        print("3. Multiplicação (*)")
        print("4. Divisão (/)")
        print("5. Expressão (Server-side)")
        print("0. Sair")
        
        escolha = input("Escolha: ")
        if escolha == '0': break

        try:
            # Lógica para pegar os inputs
            if escolha in ['1', '2', '3', '4']:
                v1 = float(input("Valor 1: "))
                v2 = float(input("Valor 2: "))
                
                resultado = 0
                #executa no servidor_rmi.py
                if escolha == '1': resultado = calc.somar(v1, v2)
                elif escolha == '2': resultado = calc.subtrair(v1, v2)
                elif escolha == '3': resultado = calc.multiplicar(v1, v2)
                elif escolha == '4': resultado = calc.dividir(v1, v2)
                
                print(f">> Resultado RMI: {resultado}")

            elif escolha == '5':
                expr = input("Digite a expressão: ")
                # Envia a string direto pro servidor calcular
                resultado = calc.resolver_expressao(expr)
                print(f">> Resultado Expressão: {resultado}")

        except Pyro4.errors.CommunicationError:
            print("ERRO: O servidor caiu ou não está acessível.")
            break
        except Exception as e:
            print(f"Erro na operação: {e}")

if __name__ == "__main__":
    menu()