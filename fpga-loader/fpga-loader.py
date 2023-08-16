from flask import Flask, request, make_response
import os
import subprocess
import threading
import re
import logging
import requests

# Configuração básica de log
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    logging.info("Arquivo recebido via POST")
    file = request.files['file']
    filepath = os.path.join("./", file.filename)
    file.save(filepath)

    # Recebe o serial number da placa a ser programada
    serialNumber = request.form.get('serialNumber')

    print(turnOnOffUSBPort("on", "0", 0))
    print(turnOnOffUSBPort("on", "1", 2))

    # # Cria a thread
    thread = threading.Thread(target=get_data_from_serial)

    # # Inicia a thread
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

    print(turnOnOffUSBPort("off", "0", 0))
    print(turnOnOffUSBPort("off", "1", 0))

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

def get_data_from_serial():
    try:
        subprocess.run(["python3", "getSerial.py"])
    except FileNotFoundError:
        print("Arquivo 'getSerial.py' não encontrado ou erro ao executar o comando.")

def turnOnOffUSBPort(action, usbPort, timeSleep=0):
    data = {'action': action, 'usbPort': usbPort, 'timeSleep': timeSleep}

    try:
        rupconHost = os.environ.get("RUPCON_HOST")
        rupconPort = os.environ.get("RUPCON_PORT")

        response = requests.post(f'http://{rupconHost}:{rupconPort}/manage_usb_power', data=data)

        if response.status_code == 200:
            return f'Resposta da API manage_usb_power: {response.text}'
        else:
            return f'Erro na requisição: {response.status_code}'
    except requests.exceptions.RequestException as e:
        return f'Erro na requisição: {e}'


if __name__ == '__main__':
    fpgaLoaderPort = os.environ.get("FPGA_LOADER")
    app.run(host='0.0.0.0', port=fpgaLoaderPort)