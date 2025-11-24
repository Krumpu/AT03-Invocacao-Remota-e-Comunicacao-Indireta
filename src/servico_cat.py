import paho.mqtt.client as mqtt
import json
import time

# Configurações
BROKER = "localhost"
TOPICO_SENSOR = "industria/caldeira/sensor/+"
TOPICO_ALERTA = "industria/alertas"

# Memória para armazenar as leituras
historico = {}
ultima_media = None

def on_connect(client, userdata, flags, rc, properties=None):
    print(f"Conectado ao Broker com código {rc}")
    client.subscribe(TOPICO_SENSOR)

def on_message(client, userdata, msg):
    global ultima_media
    
    try:
        payload = json.loads(msg.payload.decode())
        sensor_id = payload['id']
        valor = float(payload['valor'])
        agora = time.time()
        
        # 1. Armazena a leitura
        if sensor_id not in historico: historico[sensor_id] = []
        historico[sensor_id].append({"valor": valor, "tempo": agora})
        
        # 2. Limpa dados velhos (> 120 segundos conforme roteiro)
        # Mantemos apenas leituras onde (agora - tempo_leitura) <= 120
        historico[sensor_id] = [L for L in historico[sensor_id] if (agora - L['tempo']) <= 120]
        
        # 3. Calcula Média Geral (de todos os sensores)
        todas_leituras = [L['valor'] for sensor in historico.values() for L in sensor]
        if not todas_leituras: return

        media_atual = sum(todas_leituras) / len(todas_leituras)
        print(f"[CAT] Média (120s): {media_atual:.2f}ºC | Leituras: {len(todas_leituras)}")
        
        # 4. Verifica Regras de Alarme
        
        # Regra A: Temperatura Alta (> 200 graus)
        if media_atual > 200:
            msg_alerta = f"PERIGO: Temperatura Crítica! Média: {media_atual:.2f}ºC"
            client.publish(f"{TOPICO_ALERTA}/critico", msg_alerta)
            print(">>> ALERTA CRÍTICO ENVIADO")

        # Regra B: Aumento Repentino (Diferença > 5 graus da última média)
        if ultima_media is not None:
            if abs(media_atual - ultima_media) > 5:
                msg_alerta = f"ATENÇÃO: Variação brusca detectada ({ultima_media:.2f} -> {media_atual:.2f})"
                client.publish(f"{TOPICO_ALERTA}/variacao", msg_alerta)
                print(">>> ALERTA VARIAÇÃO ENVIADO")
        
        ultima_media = media_atual

    except Exception as e:
        print(f"Erro ao processar mensagem: {e}")

client = mqtt.Client(protocol=mqtt.MQTTv5)
client.on_connect = on_connect
client.on_message = on_message

print("--- Serviço CAT (Cálculo de Média) Iniciado ---")
client.connect(BROKER, 1883, 60)
client.loop_forever()