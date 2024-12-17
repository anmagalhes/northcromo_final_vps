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

# Passo 2: Garantir que estamos no branch correto (main)
current_branch=$(git symbolic-ref --short HEAD)
if [ "$current_branch" != "main" ]; then
    echo "Mudando para o branch main..."
    git checkout main || { echo "Erro: Não foi possível mudar para o branch main"; exit 1; }
fi

# Passo 3: Garantir que não há alterações locais
echo "Descartando alterações locais (se houver)..."
git reset --hard HEAD || { echo "Erro: Falha ao descartar alterações locais"; exit 1; }

# Passo 4: Garantir que o repositório está atualizado com o remoto
echo "Puxando as últimas alterações do Git..."
git fetch origin || { echo "Erro: Falha ao buscar atualizações do repositório."; exit 1; }
git reset --hard origin/main || { echo "Erro: Não foi possível alinhar o repositório com o remoto."; exit 1; }

# Passo 5: Verificar e ativar o ambiente virtual
echo "Verificando o ambiente virtual em: $VENV_DIR"
if [ -f "$VENV_DIR/bin/activate" ]; then
    echo "Ambiente virtual encontrado. Ativando..."
    source $VENV_DIR/bin/activate || { echo "Erro: Não foi possível ativar o ambiente virtual."; exit 1; }
else
    echo "Erro: Ambiente virtual não encontrado em $VENV_DIR"
    exit 1
fi

# Passo 6: Instalar as dependências
echo "Instalando as dependências do projeto..."
pip install -r $BACKEND_DIR/requirements.txt || { echo "Erro: Falha ao instalar as dependências."; exit 1; }

# Passo 7: Reiniciar o Gunicorn
echo "Reiniciando o Gunicorn..."
systemctl restart gunicorn || { echo "Erro: Falha ao reiniciar o Gunicorn."; exit 1; }

# Passo 8: Confirmar se o Gunicorn foi reiniciado corretamente
echo "Verificando o status do Gunicorn..."
systemctl status gunicorn --no-pager || { echo "Erro: Gunicorn não está funcionando corretamente."; exit 1; }

echo "Deploy realizado com sucesso!"
