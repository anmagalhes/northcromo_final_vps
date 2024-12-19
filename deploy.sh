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

# Passo 2: Garantir que o repositório está atualizado com o remoto
echo "Puxando as últimas alterações do Git..."
git pull origin main || { echo "Erro: Falha ao puxar do Git. Verifique se o repositório remoto está configurado corretamente."; exit 1; }

# Passo 3: Verificar e ativar o ambiente virtual ou criar se não existir
echo "Verificando o ambiente virtual em: $VENV_DIR"
if [ -f "$VENV_DIR/bin/activate" ]; then
    echo "Ambiente virtual encontrado. Ativando..."
    source $VENV_DIR/bin/activate || { echo "Erro: Não foi possível ativar o ambiente virtual."; exit 1; }
else
    echo "Ambiente virtual não encontrado em $VENV_DIR. Criando um novo ambiente virtual..."
    python3 -m venv $VENV_DIR || { echo "Erro: Não foi possível criar o ambiente virtual."; exit 1; }
    echo "Ambiente virtual criado com sucesso. Ativando..."
    source $VENV_DIR/bin/activate || { echo "Erro: Não foi possível ativar o ambiente virtual."; exit 1; }
fi

# Passo 4: Instalar as dependências
echo "Instalando as dependências do projeto..."
pip install -r $BACKEND_DIR/requirements.txt || { echo "Erro: Falha ao instalar as dependências."; exit 1; }

# Passo 5: Reiniciar o Gunicorn
echo "Reiniciando o Gunicorn..."
systemctl restart gunicorn || { echo "Erro: Falha ao reiniciar o Gunicorn."; exit 1; }

# Passo 6: Confirmar se o Gunicorn foi reiniciado corretamente
echo "Verificando o status do Gunicorn..."
systemctl status gunicorn --no-pager || { echo "Erro: Gunicorn não está funcionando corretamente."; exit 1; }

# Passo 7: Reiniciar o Nginx
echo "Reiniciando o Nginx..."
systemctl restart nginx || { echo "Erro: Falha ao reiniciar o Nginx."; exit 1; }

# Passo 8: Verificar se o Nginx está funcionando corretamente
echo "Verificando o status do Nginx..."
systemctl status nginx --no-pager || { echo "Erro: Nginx não está funcionando corretamente."; exit 1; }

# Passo 9: Monitorar os logs do Gunicorn
echo "Monitorando os logs do Gunicorn..."
tail -f /var/log/gunicorn/gunicorn.log &  # Rodar o monitoramento em segundo plano

# Passo 10: Concluir
echo "Deploy realizado com sucesso! A aplicação está rodando. O monitoramento dos logs do Gunicorn está ativo."

# Reiniciar o Gunicorn e Habilitar para Iniciar no Boot
sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn

echo "Habilitado tudo ! ."
