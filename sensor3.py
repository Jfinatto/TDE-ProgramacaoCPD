import requests
import random
import time

# -----------------------------------------------------------------
# 1. CONFIGURAÇÕES GLOBAIS
# -----------------------------------------------------------------
# **ATENÇÃO: SUBSTITUA APENAS ESTE TOKEN EM CADA UMA DAS 4 CÓPIAS**
DEVICE_TOKEN = "4fd08dfa-eb7c-48bd-8bc0-9f00e03c89e1" 

# Endpoint da API HTTP do TagoIO
URL = "https://api.tago.io/data"

HEADERS = {
    "Content-Type": "application/json",
    "Device-Token": DEVICE_TOKEN
}

# -----------------------------------------------------------------
# 2. FUNÇÃO DE SIMULAÇÃO E PROCESSAMENTO (REQUISITO B)
# -----------------------------------------------------------------
def send_tago_data():
    # 1. Geração de dados simulados
    # Valores normais de operação: Temp (18-32 C), Umid (35-70 %)
    temp = random.uniform(18.0, 32.0)
    umid = random.uniform(35.0, 70.0)

    # --- Simulação de Outlier (Para demonstração do filtro) ---
    # 1 em cada 10 vezes, gera um valor irreal para testar o filtro.
    if random.randint(1, 10) == 1:
        # Força temperatura para um valor irreal (ex: 100C a 200C)
        temp = random.uniform(100.0, 200.0) 
        print("!!! Outlier de Temperatura FORÇADO para teste")

    # 2. IMPLEMENTAÇÃO DO ALGORITMO DE OUTLIER (REQUISITO B)
    # Rejeita dados que estão fora de um intervalo fisicamente possível.
    # Ex: Temp < 0C ou > 50C. Umidade < 0% ou > 100%.
    if temp < 0.0 or temp > 50.0 or umid < 0.0 or umid > 100.0:
        print("----------------------------------------")
        print(f"OUTLIER DETECTADO. Temp={temp:.1f}C, Umid={umid:.1f}%. DADO DESCARTADO.")
        print("----------------------------------------")
        return  # O 'return' impede a continuação da função (não envia o dado).
    
    # 3. Montagem do Payload JSON (Formato TagoIO)
    payload = [
        {"variable": "temperatura", "value": temp},
        {"variable": "umidade", "value": umid}
    ]

    # 4. Envio via API HTTP (Requisito A)
    response = requests.post(URL, headers=HEADERS, json=payload)

    if response.status_code == 200:
        print(f"Dados enviados com sucesso: Temp={temp:.1f}C, Umid={umid:.1f}%.")
    else:
        print(f"Erro ao enviar dados: {response.text}")


# -----------------------------------------------------------------
# 3. LOOP PRINCIPAL
# -----------------------------------------------------------------
if __name__ == "__main__":
    print("Iniciando simulação de envio de dados (CTRL+C para parar)...")
    
    # Verifica dependência (necessário instalar: pip install requests)


    while True:
        try:
            send_tago_data()
            time.sleep(10)  # Envia dados a cada 10 segundos
        except KeyboardInterrupt:
            print("\nSimulação encerrada.")
            break
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            time.sleep(5)