import Pyro4
# IMPORTANTE: Verifique se o nome do seu arquivo é calculadora_core ou calculadora
from calculadora import CalculadoraLogica

# 1. Configuração OBRIGATÓRIA para ambos (Cliente e Servidor)
Pyro4.config.SERIALIZER = "pickle"
Pyro4.config.SERIALIZERS_ACCEPTED.add("pickle")

@Pyro4.expose
class CalculadoraRemota(CalculadoraLogica):
    # Se a herança falhar, isso garante que funciona:
    def somar(self, a, b): return super().somar(a, b)
    def subtrair(self, a, b): return super().subtrair(a, b)
    def multiplicar(self, a, b): return super().multiplicar(a, b)
    def dividir(self, a, b): return super().dividir(a, b)
    def resolver_expressao(self, expressao): return super().resolver_expressao(expressao)

def iniciar_servidor():
    daemon = Pyro4.Daemon(host="localhost", port=9090)
    uri = daemon.register(CalculadoraRemota, "calculadora")
    print("--- Servidor RMI Rodando (Pickle Ativado) ---")
    print(f"URI: {uri}")
    daemon.requestLoop()

if __name__ == "__main__":
    iniciar_servidor()