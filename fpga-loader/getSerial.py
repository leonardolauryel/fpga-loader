import serial.tools.list_ports
import serial
import time
import sys

# Recebe por argumento a porta serial e o tempo de leitura
if len(sys.argv) == 3:
    porta_serial = str(sys.argv[1])
    tempo_leitura = int(sys.argv[2])
    print(f"A porta serial recebida foi: {porta_serial}")
    print(f"O tempo de leitura foi: {tempo_leitura}")
else:
    print("A porta serial e o tempo de leitura devem ser enviados por argumento")
    print("Ex.: python3 getSerial.py /dev/ttyUSB0 5")
    sys.exit(1)

velocidade_transmissao = 115200 # Verifique a velocidade de transmissão adequada para o seu dispositivo

ser = serial.Serial(porta_serial, velocidade_transmissao, timeout=tempo_leitura)


# Nome do arquivo para salvar os dados
nome_arquivo = 'results.txt'

try:
    tempo_inicio = time.time()
    with open(nome_arquivo, 'w') as arquivo:
        arquivo.write('Resultados da exucução:\n')
        while (time.time() - tempo_inicio) < tempo_leitura:
            # dado_serial = ser.read()
            # dado_decodificado = dado_serial
            # arquivo.write(str(dado_decodificado) + '\n')

            dado_serial = ser.readline()
            dado_decodificado = dado_serial.decode().strip()
            arquivo.write(dado_decodificado + '\n')
            
        print("Dados coletados da serial com sucesso")
except KeyboardInterrupt:
    pass  # Se interrompermos manualmente, apenas passamos
finally:
    ser.close()
