#!/bin/bash

# Não cria corretamente as vars de ambiente
export MANAGE_USB_POWER=true
export RUPCON_HOST=localhost
export RUPCON_PORT=8001

echo "Variáveis de ambiente definidas:"
echo "MANAGE_USB_POWER: $MANAGE_USB_POWER"
echo "RUPCON_HOST: $RUPCON_HOST"
echo "RUPCON_PORT: $RUPCON_PORT"