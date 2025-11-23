import math

class CalculadoraLogica:
    def somar(self,a,b):
        return a + b
    def subtrair(self,a,b):
        return a - b
    def multiplicar(self,a,b):
        return a * b
    def dividir(self,a,b):
        if b==0:
            print("erro, não é possivel divir por zero")
        return a / b
    
    def resolver_expressao(self, expressao):
        
        try:
            permitidos =set("0123456780+-*/(). ")
            if not set(expressao.issubset(permitidos)):
                return "Erro: caracteres inválidos na expressão"
            
            return eval(expressao)
        except Exception as e:
            return f"Erro ao calcular a expressao: {str(e)}"