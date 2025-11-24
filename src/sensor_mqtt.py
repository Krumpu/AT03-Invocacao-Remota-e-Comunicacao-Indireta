import paho.mqtt.client as mqtt
import time
import random
import json

client = mqtt.Client(protocol=mqtt.MQTTv5)
client.connect("localhost", 1883, 60)

print("--- Sensor Iniciado ---")
while True:
    # Gera temperatura.
    temp = round(random.uniform(180.0, 220.0), 2) 
    
    payload = json.dumps({"id": "sensor_1", "valor": temp})
    client.publish("industria/caldeira/sensor/1", payload)
    print(f"Enviado: {temp}ºC")
    time.sleep(5) # Envia a cada 5s para testar rápido