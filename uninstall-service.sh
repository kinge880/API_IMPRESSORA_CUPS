#!/bin/bash

echo "Desinstalando serviço API CUPS..."

# Verificar se está rodando como root
if [ "$EUID" -ne 0 ]; then
    echo "Este script precisa ser executado como root (sudo)"
    exit 1
fi

# Parar o serviço se estiver rodando
systemctl stop api-cups.service 2>/dev/null

# Desabilitar o serviço
systemctl disable api-cups.service 2>/dev/null

# Remover o arquivo de serviço
rm -f /etc/systemd/system/api-cups.service

# Recarregar o systemd
systemctl daemon-reload

echo "Serviço desinstalado com sucesso!" 