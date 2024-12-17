#!/bin/bash

# Caminho do seu diretório de projeto
PROJECT_DIR="/var/www/northcromo_final_vps"

# Caminho do ambiente virtual
VENV_DIR="$PROJECT_DIR/backend/venv"

# Caminho do Gunicorn
GUNICORN_SERVICE="/etc/systemd/system/gunicorn.service"

# Caminho do diretório do backend
BACKEND_DIR="$PROJECT_DIR/backend"

# Passo 1: Navegar até o diretório do projeto
echo "Navegando até o diretório do projeto: $PROJECT_DIR"
cd $PROJECT_DIR || { echo "Erro: Não foi possível acessar o diretório $PROJECT_DIR"; exit 1; }

# Passo 2: Puxar as últimas alterações do Git
echo "Puxando as últimas alterações do Git..."
git pull origin main || { echo "Erro: Falha ao puxar do Git. Verifique se o repositório remoto está configurado corretamente."; exit 1; }

# Passo 3: Verificar e ativar o ambiente virtual
if [ -f "$VENV_DIR/bin/activate" ]; then
    echo "Ativando o ambiente virtual..."
    source $VENV_DIR/bin/activate
else
    echo "Erro: Ambiente virtual não encontrado em $VENV_DIR"
    exit 1
fi

# Passo 4: Instalar as dependências
echo "Instalando as dependências do projeto..."
pip install -r $BACKEND_DIR/requirements.txt || { echo "Erro: Falha ao instalar as dependências."; exit 1; }

# Passo 5: Reiniciar o Gunicorn (caso você esteja utilizando o systemd)
echo "Reiniciando o Gunicorn..."
systemctl restart gunicorn || { echo "Erro: Falha ao reiniciar o Gunicorn."; exit 1; }

# Passo 6: Confirmar se o Gunicorn foi reiniciado corretamente
echo "Verificando o status do Gunicorn..."
systemctl status gunicorn --no-pager || { echo "Erro: Gunicorn não está funcionando corretamente."; exit 1; }

echo "Deploy realizado com sucesso!"

