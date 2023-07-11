from flask import Flask, request, make_response
import os
import subprocess
import re
import logging

# Configuração básica de log
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    logging.info("Arquivo recebido via POST")
    file = request.files['file']
    filepath = os.path.join("./", file.filename)
    file.save(filepath)

    try:
        result = upload_code_to_FPGA(file.filename)
        output = result.stdout.strip().decode("utf-8")
    except ValueError as err:
        logging.error("Ocorreu um erro: %s", err)
        response = make_response(str(err), 500)  # Status code 500 - Internal Server Error
        return response

    return 'FPGA programada com sucesso!\n\nLogs do adept:\n' + str(output) 

def upload_code_to_FPGA(filename):
    serialNumber = get_serial_number()

    if serialNumber == None:
        raise ValueError("Não foi possível obter o Serial Number da FPGA")

    try:
        logging.info("Fazendo upload do arquivo '%s' para a FPGA", filename)
        output = subprocess.run(["./uploadCodeToFPGA.sh", filename, serialNumber], check=True, capture_output=True)
    except:
        raise ValueError("Erro ao enviar o código para FPGA")
    
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)