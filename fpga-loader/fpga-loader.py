from flask import Flask, request, make_response, jsonify
import serial.tools.list_ports
import os
import subprocess
import threading
import re
import logging
import requests
import queue

def getUSBSerialPorts():
    usb_ports = list(serial.tools.list_ports.comports())
    usb_ports = [port.device for port in usb_ports if "USB" in port.device]

    return usb_ports

# Configuração básica de log
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def uploadFile():
    logging.info("\n\n\nArquivo recebido via POST")
    file = request.files['file']
    filepath = os.path.join("./", file.filename)
    file.save(filepath)

    # Recebe o serial number da placa a ser programada
    serialNumber = request.form.get('serialNumber')
    serialReadTime = request.form.get('serialReadTime')
    baudRate = request.form.get('baudRate')

    logging.info(f"serialNumber: {serialNumber}")
    logging.info(f"serialReadTime: {serialReadTime}")
    logging.info(f"baudRate: {baudRate}")

    usbSerialPorts = getUSBSerialPorts()

    # Obtem os dados da FPGA a ser programada
    fpgaData = getFPGADataBySerialNumber(serialNumber)[0]

    # Obtem as portas que a FPGA e o coletor de dados serial está conectado
    targetPorts = getPowerSupplyPorts(fpgaData)

    err = turnOnTargetPowerSupply(targetPorts, fpgaData['startup_time'])
    if err:
        logging.error(f"error: {err}")
        return jsonify({f"error: {err}"}), 500


    # Salva a porta serial que foi conectada
    connectedSerialPort, err = identifyConnectedSerialPort(usbSerialPorts)
    if err:
        logging.error(err)
        response = make_response(err, 500)
        return response
    
    q = queue.Queue()

    # Cria a thread
    thread = threading.Thread(target=getFPGASerialData, args=(connectedSerialPort, serialReadTime, baudRate, q))

    # Inicia a thread
    thread.start()

    try:
        result = uploadCodeToFPGA(file.filename, serialNumber)
        output = result.stdout.strip().decode("utf-8")
    except ValueError as err:
        logging.error("Ocorreu um erro: %s", err)
        turnOnOffPowerSupply("off", "all", 0)
        response = make_response(str(err), 500)
        return response

    # Aguarda o término da thread para sincronizar a execução
    thread.join()

    # Obtêm o resultado da execução da thread
    collectedFPGASerialData= q.get()

    err = turnOffTargetPowerSupply(targetPorts)
    if err:
        logging.error(f"error: {err}")
        return jsonify({f"error: {err}"}), 500

    if collectedFPGASerialData is None:
        err = "ERRO: Não foi possível coletar os dados da serial"
        logging.error(err)
        response = make_response(err, 500)
        return response
    
    return collectedFPGASerialData

@app.route('/getResults', methods=['GET'])
def getResults():
    with open('results.txt', 'r') as file:
        conteudo = file.read()
    
    return conteudo

@app.route('/getConnectedFPGA', methods=['GET'])
def getConnectedFPGA():
    print(turnOnOffPowerSupply("on", "all", 4))
    output = subprocess.check_output(['djtgcfg', 'enum'], universal_newlines=True, encoding='latin1')
    print(turnOnOffPowerSupply("off", "all", 0))
    return output


def uploadCodeToFPGA(filename, serialNumber):
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

def getFPGASerialData(serialPort, serialReadTime, baudRate, q):
    data = {'serialPort': serialPort, 'serialReadTime': serialReadTime}

    if baudRate is not None:
        data['baudRate'] = baudRate

    try:
        fserdacHost = os.environ.get("FSERDAC_HOST")
        response = requests.post(f'http://{fserdacHost}:8000/get_fpga_serial_data', data=data)

        if response.status_code == 200:
            logging.info(f'Resposta da API get_fpga_serial_data: {response.text}')
            q.put(response.text)
            return
        else:
            logging.info(f'Erro na requisição: {response.status_code}')
            q.put(None)
            return
    except requests.exceptions.RequestException as e:
        logging.info(f'Erro na requisição: {e}')
        q.put(None)
        return

def turnOnTargetPowerSupply(ports, startup_time):
    delay = 0
    for index, port in enumerate(ports):
        # Faz com que seja aplicado um delay na ultima porta ligada
        # para que a FPGA tenha tempo de inicializar
        if index == (len(ports) - 1):
            delay = startup_time

        err = turnOnOffPowerSupply("on", port, delay)
        if err:
            return f"Não foi possível ligar a USB {port}"
    
    return 0

def turnOffTargetPowerSupply(ports):
    delay = 0
    for port in ports:
        err = turnOnOffPowerSupply("off", port, delay)
        if err:
            return f"Não foi possível desligar a USB {port}"

    return 0

def turnOnOffPowerSupply(action, powerSupplyPort, timeSleep=0):
    data = {'action': action, 'powerSupplyPort': powerSupplyPort, 'timeSleep': timeSleep}

    try:
        rpsconHost = os.environ.get("RPSCON_HOST")

        response = requests.post(f'http://{rpsconHost}:8000/power_supply_control', data=data)

        if response.status_code == 200:
            logging.info(f'Resposta da API power_supply_control: {response.text}')
            return 0
        else:
            logging.info(f'Erro na requisição: {response.status_code}')
            return 1
    except requests.exceptions.RequestException as e:
        logging.info(f'Erro na requisição: {e}')
        return 1

def getFPGADataBySerialNumber(serialNumber):
    deviceManagerHost = os.environ.get("DEVICE_MANAGER_HOST")
 
    response = requests.get(f'http://{deviceManagerHost}:8000/devices/fpgas/?serial_number={serialNumber}')

    if response.status_code != 200:
        return jsonify({"error": "Não foi possível obter dados da API"}), response.status_code
    
    data = response.json()
    return data

def getPowerSupplyPorts(data):
    ports = []

    fpgaPowerSupplyPort = data['connected_power_supply']['num']
    ports.append(fpgaPowerSupplyPort)

    serialCollectorPowerSupply = data['connected_serial_collector']['connected_power_supply']
    
    if serialCollectorPowerSupply is not None:
        serialCollectorPowerSupplyPort = serialCollectorPowerSupply['num']
        ports.append(serialCollectorPowerSupplyPort)

    return ports

def identifyConnectedSerialPort(usbSerialPorts):
    connectedSerialPort = list(set(getUSBSerialPorts()) - set(usbSerialPorts))
    err = None

    if len(connectedSerialPort) != 1:
        if(len(connectedSerialPort) == 0):
            err = "Nenhuma porta serial foi conectada. Tente novamente"
        else:
            err = "Muitas portas seriais conectadas. Não foi possível identifcar a porta que os dados devem ser capturados. Tente novamente"

        turnOnOffPowerSupply("off", "all", 0)
        return None, err
        

    connectedSerialPort = connectedSerialPort[0]

    logging.info(f"A porta serial conectada foi {connectedSerialPort}")

    return connectedSerialPort, err

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)