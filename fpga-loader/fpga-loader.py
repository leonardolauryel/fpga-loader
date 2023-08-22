from flask import Flask, request, make_response
import serial.tools.list_ports
import os
import subprocess
import threading
import re
import logging
import requests

def get_usb_serial_ports():
    usb_ports = list(serial.tools.list_ports.comports())
    usb_ports = [port.device for port in usb_ports if "USB" in port.device]

    return usb_ports

# Configuração básica de log
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    logging.info("\n\n\nArquivo recebido via POST")
    file = request.files['file']
    filepath = os.path.join("./", file.filename)
    file.save(filepath)

    # Recebe o serial number da placa a ser programada
    serialNumber = request.form.get('serialNumber')
    serial_read_time = request.form.get('serialReadTime')

    logging.info(f"serialNumber: {serialNumber}")
    logging.info(f"serial_read_time: {serial_read_time}")

    usb_serial_ports = get_usb_serial_ports()

    err = turnOnOffUSBPort("on", "0", 0)
    if err:
        return jsonify({"error": "Não foi possível ligar a USB 0"}), 500

    err = turnOnOffUSBPort("on", "1", 2)
    if err:
        return jsonify({"error": "Não foi possível ligar a USB 1"}), 500

    # Salva a porta serial que foi conectada
    connected_serial_port = list(set(get_usb_serial_ports()) - set(usb_serial_ports))[0]
    logging.info(f"A porta serial conectada foi {connected_serial_port}")

    # Cria a thread
    thread = threading.Thread(target=get_data_from_serial, args=(connected_serial_port, serial_read_time))

    # Inicia a thread
    thread.start()

    try:
        result = upload_code_to_FPGA(file.filename, serialNumber)
        output = result.stdout.strip().decode("utf-8")
    except ValueError as err:
        logging.error("Ocorreu um erro: %s", err)
        response = make_response(str(err), 500)  # Status code 500 - Internal Server Error
        return response

    # Aguarda o término da thread, caso deseje sincronizar a execução
    thread.join()

    err = turnOnOffUSBPort("off", "0", 0)
    if err:
        logging.info("Não foi possível desligar a USB 0")

    err = turnOnOffUSBPort("off", "1", 0)
    if err:
        logging.info("Não foi possível desligar a USB 1")

    with open('results.txt', 'r') as file:
        conteudo = file.read()
    
    return conteudo

    

    #return 'FPGA programada com sucesso!\n\nLogs do adept:\n' + str(output)

@app.route('/getResults', methods=['GET'])
def getResults():
    with open('results.txt', 'r') as file:
        conteudo = file.read()
    
    return conteudo

@app.route('/getConnectedFPGA', methods=['GET'])
def getConnectedFPGA():
    print(turnOnOffUSBPort("on", "all", 4))
    output = subprocess.check_output(['djtgcfg', 'enum'], universal_newlines=True, encoding='latin1')
    print(turnOnOffUSBPort("off", "all", 0))
    return output


def upload_code_to_FPGA(filename, serialNumber):
    if serialNumber == None:
        raise ValueError("Não foi possível obter o Serial Number da FPGA")

    try:
        logging.info("Fazendo upload do arquivo '%s' para a FPGA", filename)
        output = subprocess.run(["./uploadCodeToFPGA.sh", filename, serialNumber], check=True, capture_output=True)
    except Exception as e:
        raise ValueError(f"Erro ao enviar o código para FPGA: {str(e)}")
    
    return output


def get_serial_number():
    try:
        logging.info("Obtendo serial number da FPGA")
        output = subprocess.check_output(['djtgcfg', 'enum'], universal_newlines=True, encoding='latin1')
        serialNumber = re.search(r'Serial Number:\s+(\d+)', output)

        if serialNumber:
            return serialNumber.group(1)
        else:
            return None

    except subprocess.CalledProcessError:
        return None

def get_data_from_serial(connected_serial_port, serial_read_time):
    try:
        logging.info("Iniciando processo para obter dados da Serial")
        result = subprocess.run(["python3", "getSerial.py", str(connected_serial_port), str(serial_read_time)], 
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.PIPE, 
                                text=True,
                                check=True)
        logging.info(f"Resultado da coleta de dados via Serial: {result.stdout}")
    except subprocess.CalledProcessError as e:
        # Se ocorrer um erro ao executar o processo, o subprocess.CalledProcessError será capturado aqui
        logging.error("Erro ao executar o processo de coletar dados da serial:", e)
    except Exception as e:
        logging.error("Erro ao coletar dados da serial:", e)

def turnOnOffUSBPort(action, usbPort, timeSleep=0):
    data = {'action': action, 'usbPort': usbPort, 'timeSleep': timeSleep}

    try:
        rupconHost = os.environ.get("RUPCON_HOST")
        rupconPort = os.environ.get("RUPCON_PORT")

        response = requests.post(f'http://{rupconHost}:{rupconPort}/manage_usb_power', data=data)

        if response.status_code == 200:
            logging.info(f'Resposta da API manage_usb_power: {response.text}')
            return 0
        else:
            logging.info(f'Erro na requisição: {response.status_code}')
            return 1
    except requests.exceptions.RequestException as e:
        logging.info(f'Erro na requisição: {e}')
        return 1


if __name__ == '__main__':
    fpgaLoaderPort = os.environ.get("FPGA_LOADER")
    app.run(host='0.0.0.0', port=fpgaLoaderPort)