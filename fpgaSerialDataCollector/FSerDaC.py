from flask import Flask, request, make_response, jsonify
import logging
import serial
import serial.tools.list_ports
import time
import sys

# Configuração básica de log
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
BAUD_RATE_DEFAULT = 115200

app = Flask(__name__)

@app.route('/get_fpga_serial_data', methods=['POST'])
def getFPGASerialData():
    # Recebe a porta serial e o tempo de leitura
    serialPort = request.form.get('serialPort')
    serialReadTime = request.form.get('serialReadTime')
    baudRate = request.form.get('baudRate')

    logging.info(f"A porta serial recebida foi: {serialPort}")
    logging.info(f"O tempo de leitura recebido foi: {serialReadTime}")

    if baudRate is None:
        baudRate = BAUD_RATE_DEFAULT
        logging.info(f"baudRate não foi fornecido. Setando para o valor padão {BAUD_RATE_DEFAULT}")
    else:
        baudRate = int(baudRate)
        logging.info(f"O Baud Rate recebido foi: {baudRate}")

    if serialPort is None or serialReadTime is None:
        err = "serialPort e o serialReadTime devem ser enviados"
        logging.error("Erro: %s", err)
        response = make_response(str(err), 500)
        return response
    
    serialPort = str(serialPort)
    serialReadTime = int(serialReadTime)

    # Configura a conexão serial
    try:
        ser = serial.Serial(serialPort, baudRate, timeout=serialReadTime)
    except Exception as e:
        errMsg = f"Não foi possível conectar com a porta serial {serialPort}"
        logging.error("Erro: %s (%s)", errMsg, str(e))
        response = make_response(str(errMsg), 500)
        return response

    # Nome do arquivo para salvar os dados
    fileName = 'collectedData.txt'

    try:
        startTime = time.time()
        with open(fileName, 'w') as file:
            while (time.time() - startTime) < serialReadTime:
                serialData = ser.readline()
                runTime = time.time() - startTime
                runTime = f"{runTime:.6f}"
                decodedData = serialData.decode().strip()
                logging.info(decodedData)
                file.write(f"[{str(runTime)}]\t\t{decodedData}\n")
                
            logging.info("Dados coletados da serial com sucesso")
    except Exception as e:
        errMsg = "Houve um erro ao ler os dados da porta serial"
        logging.error("Erro: %s (%s)", errMsg, str(e))
        response = make_response(str(errMsg), 500)
        return response
    finally:
        ser.close()

    with open('collectedData.txt', 'r') as file:
        conteudo = file.read()
    
    return jsonify(conteudo)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
