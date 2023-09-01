#!/bin/bash

# Não cria corretamente as vars de ambiente
export POWER_SUPPLY_CONTROL=true
export RPSCON_HOST=localhost
export RPSCON_PORT=8001

echo "Variáveis de ambiente definidas:"
echo "POWER_SUPPLY_CONTROL: $POWER_SUPPLY_CONTROL"
echo "RPSCON_HOST: $RPSCON_HOST"
echo "RPSCON_PORT: $RPSCON_PORT"