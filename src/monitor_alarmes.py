import paho.mqtt.client as mqtt
import tkinter as tk
from threading import Thread
import queue

# Configurações MQTT
BROKER = "localhost" 
TOPICO_ALERTA = "industria/alertas/#"

# Fila para comunicação entre Threads
fila_ui = queue.Queue()

# Variáveis da Interface
janela = tk.Tk()
janela.title("Monitor de Alarmes Industrial")
janela.geometry("400x300")
janela.configure(bg="green")

texto_status = tk.Label(janela, text="SISTEMA NORMAL", font=("Arial", 16, "bold"), bg="green", fg="white")
texto_status.pack(expand=True)

lista_log = tk.Listbox(janela, height=8)
lista_log.pack(fill="x", padx=10, pady=10)

def atualizar_gui_pela_fila():
    try:
        # 
        while True:
            tipo, mensagem = fila_ui.get_nowait()
            
            
            lista_log.insert(0, f"[{tipo}] {mensagem}")
            
            
            if "critico" in tipo:
                janela.configure(bg="red")
                texto_status.config(text="ALERTA CRÍTICO!", bg="red")
            elif "variacao" in tipo:
                # Só muda para laranja se não estiver vermelho (crítico tem prioridade)
                if janela.cget("bg") != "red":
                    janela.configure(bg="orange")
                    texto_status.config(text="Atenção: Variação", bg="orange")
                    
    except queue.Empty:
        pass

    janela.after(100, atualizar_gui_pela_fila)

# Callbacks MQTT
def on_message(client, userdata, msg):
    mensagem = msg.payload.decode()
    topico = msg.topic
    print(f"Alarme recebido: {mensagem}")
    
    # Define o tipo
    tipo = "critico" if "critico" in topico else "variacao"
    
    # EM VEZ DE ATUALIZAR DIRETO, COLOCA NA FILA
    fila_ui.put((tipo, mensagem))

def iniciar_mqtt():
    # Adicionei CallbackAPIVersion para sumir o aviso amarelo
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
    client.on_message = on_message
    
    try:
        client.connect(BROKER, 1883, 60)
        client.subscribe(TOPICO_ALERTA)
        client.loop_forever()
    except Exception as e:
        print(f"Erro na conexão MQTT: {e}")

# Inicia o MQTT em uma thread separada
t = Thread(target=iniciar_mqtt)
t.daemon = True
t.start()

# Inicia o loop de verificação da fila
atualizar_gui_pela_fila()

print("--- Monitor de Alarmes (GUI) Iniciado ---")
janela.mainloop()