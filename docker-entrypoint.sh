#!/bin/bash

# Iniciar o daemon do CUPS
service cups start

# Aguardar um momento para o CUPS inicializar
sleep 2

# Executar migrações do Django (se necessário)
python manage.py migrate --noinput

# Executar o comando passado como argumento
exec "$@" 