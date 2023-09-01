from flask import Flask, request, make_response
import logging
import serial
import serial.tools.list_ports
import time
import sys
import os

# IDs do fornecedor (Vendor ID) e do produto (Product ID) do dispositivo USB Conectado (Arduino)
idVendor = int(os.environ.get("ID_VENDOR_ARDUINO"), 16)
idProduct = int(os.environ.get("ID_PRODUCT_ARDUINO"), 16)

# Configuração básica de log
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Função para encontrar um dispositivo USB
def searchUSBDdevice(idVendor, idProduct):
    for port in serial.tools.list_ports.comports():
        if idVendor == port.vid and idProduct == port.pid:
            return port.device
    return None

# Configuração da porta serial do Arduino

# Procurar o dispositivo USB e obter a porta serial associada
serialPort = searchUSBDdevice(idVendor, idProduct)

if serialPort is not None:
    logging.info(f"Dispositivo USB {idVendor}:{idProduct} encontrado na porta {serialPort}.")
    baudRate = 9600
    
    # Inicializa a conexão serial
    ser = serial.Serial(serialPort, baudRate)
    time.sleep(2)  # Aguarda 2 segundos para a inicialização do Arduino
    app = Flask(__name__)
else:
    logging.error(f"Dispositivo USB {idVendor}:{idProduct}  não encontrado.")
    sys.exit(1)


@app.route('/power_supply_control', methods=['POST'])
def powerSupplyControl():
    logging.info("Comando recebido")

    # Recebe a ação (on ou off) e a porta de fornecimento de energia
    action = request.form.get('action')
    powerSupplyPort = request.form.get('powerSupplyPort')
    timeSleep = int(request.form.get('timeSleep'))

    try:
        sendCommand(action + "_" + powerSupplyPort)
        logging.info(f"Enviando comando {action} para a porta de fornecimento de energia {powerSupplyPort}")

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
