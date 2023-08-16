#!/bin/bash

devices=""

# Encontre dispositivos ttyACM* existentes no sistema
for device in /dev/ttyACM*; do
  devices="${devices}- ${device}:${device}\n"
done

# Preencha o arquivo docker-compose.yml.template
sed "s|%ARDUINO-DEVICE%|${devices}|" docker-compose.yml.template > docker-compose.yml

# Execute o docker-compose com o arquivo atualizado
docker compose up --build
