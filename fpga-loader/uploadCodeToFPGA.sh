#!/bin/bash

# Salvando nome do arquivo
nameFile="$1"
serialNumber="$2"

# Enviar .bit para a FPGA
echo "Enviando arquivo $nameFile para FPGA"
echo "Y" | djtgcfg prog -d SN:$serialNumber -i 0 -f ./$nameFile
