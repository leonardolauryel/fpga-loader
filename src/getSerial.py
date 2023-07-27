import serial
import time

porta_serial = '/dev/ttyUSB0'  # Altere para a porta serial correta do seu sistema (por exemplo, 'COM1' no Windows)
velocidade_transmissao = 115200 # Verifique a velocidade de transmissão adequada para o seu dispositivo

ser = serial.Serial(porta_serial, velocidade_transmissao)


# Nome do arquivo para salvar os dados
nome_arquivo = 'results.txt'

tempo_leitura = 10  # Tempo de leitura em segundos

try:
    tempo_inicio = time.time()
    with open(nome_arquivo, 'w') as arquivo:
        arquivo.write('Resultados da exucução:\n')
        while (time.time() - tempo_inicio) < tempo_leitura:
            dado_serial = ser.readline()
            dado_decodificado = dado_serial.decode().strip()
            arquivo.write(dado_decodificado + '\n')
            print(dado_decodificado)
except KeyboardInterrupt:
    pass  # Se interrompermos manualmente, apenas passamos
finally:
    ser.close()
