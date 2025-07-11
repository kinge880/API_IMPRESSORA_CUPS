#!/bin/bash

echo "Instalando serviço API CUPS..."

# Verificar se está rodando como root
if [ "$EUID" -ne 0 ]; then
    echo "Este script precisa ser executado como root (sudo)"
    exit 1
fi

# Obter o diretório atual
CURRENT_DIR=$(pwd)
echo "Diretório da aplicação: $CURRENT_DIR"

# Atualizar o arquivo de serviço com o caminho correto
sed -i "s|WorkingDirectory=.*|WorkingDirectory=$CURRENT_DIR|g" api-cups.service
sed -i "s|Environment=PATH=.*|Environment=PATH=$CURRENT_DIR/impressao/bin|g" api-cups.service
sed -i "s|ExecStart=.*|ExecStart=$CURRENT_DIR/impressao/bin/python manage.py runserver 0.0.0.0:8000|g" api-cups.service

# Copiar o arquivo de serviço para o systemd
cp api-cups.service /etc/systemd/system/

# Recarregar o systemd
systemctl daemon-reload

# Habilitar o serviço para iniciar com o sistema
systemctl enable api-cups.service

echo "Serviço instalado com sucesso!"
echo ""
echo "Comandos úteis:"
echo "  Iniciar o serviço: sudo systemctl start api-cups"
echo "  Parar o serviço: sudo systemctl stop api-cups"
echo "  Reiniciar o serviço: sudo systemctl restart api-cups"
echo "  Ver status: sudo systemctl status api-cups"
echo "  Ver logs: sudo journalctl -u api-cups -f"
echo ""
echo "Para iniciar agora, execute: sudo systemctl start api-cups" 