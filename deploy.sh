#!/bin/bash

# Caminho do seu diretório de projeto
PROJECT_DIR="/var/www/northcromo_final_vps"

# Caminho do ambiente virtual
VENV_DIR="$PROJECT_DIR/venv"

# Caminho do Gunicorn
GUNICORN_SERVICE="/etc/systemd/system/gunicorn.service"

# Caminho do diretório do backend
BACKEND_DIR="$PROJECT_DIR/backend"

# Passo 1: Navegar até o diretório do projeto
cd $PROJECT_DIR

# Passo 2: Puxar as últimas alterações do Git
git pull origin main

# Passo 3: Ativar o ambiente virtual automaticamente
if [ -f "$VENV_DIR/bin/activate" ]; then
    source $VENV_DIR/bin/activate
else
    echo "Erro: Ambiente virtual não encontrado em $VENV_DIR"
    exit 1
fi

# Passo 4: Instalar as dependências
pip install -r $BACKEND_DIR/requirements.txt

# Passo 5: Reiniciar o Gunicorn (caso você esteja utilizando o systemd)
# Se você estiver usando Gunicorn com systemd, reinicie o serviço
echo "Reiniciando o Gunicorn..."
systemctl restart gunicorn

# Passo 6: Confirmar se o Gunicorn foi reiniciado corretamente
systemctl status gunicorn
