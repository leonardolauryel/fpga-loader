from flask import Flask, request, make_response
import logging
import serial
import serial.tools.list_ports
import time
import sys
import os

# IDs do fornecedor (Vendor ID) e do produto (Product ID) do dispositivo USB Conectado (Arduino)
id_vendor = int(os.environ.get("ID_VENDOR_ARDUINO"), 16)
id_product = int(os.environ.get("ID_PRODUCT_ARDUINO"), 16)

# Configuração básica de log
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Função para encontrar um dispositivo USB
def search_usb_device(id_vendor, id_product):
    for port in serial.tools.list_ports.comports():
        if id_vendor == port.vid and id_product == port.pid:
            return port.device
    return None

# Configuração da porta serial do Arduino

# Procurar o dispositivo USB e obter a porta serial associada
porta_serial = search_usb_device(id_vendor, id_product)

if porta_serial is not None:
    logging.info(f"Dispositivo USB {id_vendor}:{id_product} encontrado na porta {porta_serial}.")
    velocidade_serial = 9600
    
    # Inicializa a conexão serial
    ser = serial.Serial(porta_serial, velocidade_serial)
    time.sleep(2)  # Aguarda 2 segundos para a inicialização do Arduino
    app = Flask(__name__)
else:
    logging.error(f"Dispositivo USB {id_vendor}:{id_product}  não encontrado.")
    sys.exit(1)


@app.route('/manage_usb_power', methods=['POST'])
def manageUSBPower():
    logging.info("Comando recebido")

    # Recebe a ação (on ou off) e a porta USB
    action = request.form.get('action')
    usbPort = request.form.get('usbPort')
    timeSleep = int(request.form.get('timeSleep'))

    try:
        sendCommand(action + "_" + usbPort)
        logging.info(f"Enviando comando {action} para a porta USB {usbPort}")

        resposta = ser.readline().decode().strip()
        logging.info(f"Resposta recebida: {resposta}")
        time.sleep(timeSleep)
    except ValueError as err:
        logging.error("Erro: %s", err)
        response = make_response(str(err), 500)  # Status code 500 - Internal Server Error
        return response

    return resposta

# Função para enviar comandos para o Arduino
def sendCommand(comando):
    try:
        ser.write(comando.encode())
    except Exception as e:
        raise ValueError(f"Erro ao enviar comando para o arduino: {str(e)}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
