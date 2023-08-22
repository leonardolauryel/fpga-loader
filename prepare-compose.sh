#!/bin/bash

# devices=""

# # Encontre dispositivos ttyACM* existentes no sistema
# for device in /dev/ttyACM*; do
#   if ["$device" != "/dev/ttyACM*"]; then
#     devices="${devices}      - ${device}:${device}\n"
#   fi
# done

# for device in /dev/ttyUSB*; do
#   if ["$device" != "/dev/ttyUSB*"]; then
#     devices="${devices}      - ${device}:${device}\n"
#   fi
# done

# # Preencha o arquivo docker-compose.yml.template
# sed "s|%ARDUINO-DEVICE%|${devices}|" docker-compose.yml.template > docker-compose.yml

# Execute o docker-compose com o arquivo atualizado
docker compose up
