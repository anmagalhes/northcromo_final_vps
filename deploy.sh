#!/bin/bash

# Caminho do seu diretório de backend (especificamente para o backend)
PROJECT_DIR="/var/www/northcromo_final_vps"
BACKEND_DIR="$PROJECT_DIR/backend"

# Caminho do ambiente virtual (corrigido para o diretório correto dentro do backend)
VENV_DIR="$BACKEND_DIR/venv"

# Caminho do Gunicorn
GUNICORN_SERVICE="/etc/systemd/system/gunicorn.service"

# Passo 1: Navegar até o diretório do backend
echo "Navegando até o diretório do backend: $BACKEND_DIR"
cd $BACKEND_DIR || { echo "Erro: Não foi possível acessar o diretório $BACKEND_DIR"; exit 1; }

# Passo 2: Verificar se há alterações locais
echo "Verificando alterações locais..."
git status --porcelain | grep '^[^?]' > /dev/null
if [ $? -eq 0 ]; then
  echo "Alterações locais detectadas. Realizando stash das mudanças..."
  git stash || { echo "Erro: Falha ao fazer o stash das mudanças locais."; exit 1; }
else
  echo "Nenhuma alteração local detectada."
fi

# Passo 3: Puxar as últimas alterações do Git
echo "Puxando as últimas alterações do Git..."
git pull origin main || { echo "Erro: Falha ao puxar do Git. Verifique se o repositório remoto está configurado corretamente."; exit 1; }

# Passo 4: Verificar e ativar o ambiente virtual
echo "Verificando o ambiente virtual em: $VENV_DIR"
if [ -f "$VENV_DIR/bin/activate" ]; then
    echo "Ambiente virtual encontrado. Ativando..."
    source $VENV_DIR/bin/activate || { echo "Erro: Não foi possível ativar o ambiente virtual."; exit 1; }
else
    echo "Erro: Ambiente virtual não encontrado em $VENV_DIR"
    exit 1
fi

# Passo 5: Instalar as dependências
echo "Instalando as dependências do projeto..."
pip install -r $BACKEND_DIR/requirements.txt || { echo "Erro: Falha ao instalar as dependências."; exit 1; }

# Passo 6: Reiniciar o Gunicorn
echo "Reiniciando o Gunicorn..."
systemctl restart gunicorn || { echo "Erro: Falha ao reiniciar o Gunicorn."; exit 1; }

# Passo 7: Confirmar se o Gunicorn foi reiniciado corretamente
echo "Verificando o status do Gunicorn..."
systemctl status gunicorn --no-pager || { echo "Erro: Gunicorn não está funcionando corretamente."; exit 1; }

echo "Deploy realizado com sucesso!"
