from flask import Flask, request, jsonify
import sys
from calculadora import CalculadoraLogica

app = Flask(__name__)
calc = CalculadoraLogica()

@app.route('/calcular', methods=['POST'])
def calcular():
    # Pega o JSON enviado pelo cliente
    dados = request.get_json()
    
    if not dados:
        return jsonify({"erro": "Nenhum dado enviado"}), 400

    op = dados.get('operacao')
    resp = None

    try:
        # Lógica de despacho (igual ao Socket)
        if op == 'expressao':
            resp = calc.resolver_expressao(dados['valor1'])
        else:
            v1 = float(dados['valor1'])
            v2 = float(dados['valor2'])
            
            if op == 'soma': resp = calc.somar(v1, v2)
            elif op == 'subtracao': resp = calc.subtrair(v1, v2)
            elif op == 'multiplicacao': resp = calc.multiplicar(v1, v2)
            elif op == 'divisao': resp = calc.dividir(v1, v2)
            else:
                return jsonify({"erro": "Operacao desconhecida"}), 400
        
        return jsonify({"resultado": resp})

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == '__main__':
    print("--- Servidor HTTP Rodando na porta 5001 ---")
    # Host '0.0.0.0' permite acesso externo se precisar
    app.run(host='0.0.0.0', port=5001)