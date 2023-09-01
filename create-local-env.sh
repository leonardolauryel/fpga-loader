#!/bin/bash

# Não cria corretamente as vars de ambiente
export POWER_SUPPLY_CONTROL=true
export RUPCON_HOST=localhost
export RUPCON_PORT=8001

echo "Variáveis de ambiente definidas:"
echo "POWER_SUPPLY_CONTROL: $POWER_SUPPLY_CONTROL"
echo "RUPCON_HOST: $RUPCON_HOST"
echo "RUPCON_PORT: $RUPCON_PORT"