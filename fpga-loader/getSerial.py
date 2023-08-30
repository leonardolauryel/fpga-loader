import serial.tools.list_ports
import serial
import time
import sys

# Recebe por argumento a porta serial e o tempo de leitura
if len(sys.argv) == 3:
    serialPort = str(sys.argv[1])
    readTime = int(sys.argv[2])
    print(f"A porta serial recebida foi: {serialPort}")
    print(f"O tempo de leitura foi: {readTime}")
else:
    print("A porta serial e o tempo de leitura devem ser enviados por argumento")
    print("Ex.: python3 getSerial.py /dev/ttyUSB0 5")
    sys.exit(1)

baudRate = 115200

ser = serial.Serial(serialPort, baudRate, timeout=readTime)


# Nome do arquivo para salvar os dados
fileName = 'results.txt'

try:
    tempo_inicio = time.time()
    with open(fileName, 'w') as file:
        while (time.time() - tempo_inicio) < readTime:
            # serialData = ser.read()
            # decodedData = serialData
            # file.write(str(decodedData) + '\n')

            serialData = ser.readline()
            decodedData = serialData.decode().strip()
            file.write(decodedData + '\n')
            
        print("Dados coletados da serial com sucesso")
except KeyboardInterrupt:
    pass  # Se interrompermos manualmente, apenas passamos
finally:
    ser.close()
