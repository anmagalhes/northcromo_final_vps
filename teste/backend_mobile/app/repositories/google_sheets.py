import pygsheets
from typing import List


class GoogleSheetsRepository:
    def __init__(self, sheet_id: str, service_account_file: str):
        # Autoriza e abre a planilha
        self.gc = pygsheets.authorize(service_file=service_account_file)
        self.sheet = self.gc.open_by_key(sheet_id)

    def add_grupo_produto(self, grupo_produto_data: List[str]) -> None:
        grupo_produto_sheet = self.sheet.worksheet(
            "title", "Grupo Produto"
        )  # Aba 'Grupo Produto'
        grupo_produto_sheet.append_table(grupo_produto_data)

    def add_componente(self, componente_data: List[str]) -> None:
        componente_sheet = self.sheet.worksheet(
            "title", "Componente"
        )  # Aba 'Componente'
        componente_sheet.append_table(componente_data)

    def add_operacao(self, operacao_data: List[str]) -> None:
        operacao_sheet = self.sheet.worksheet("title", "Operacao")  # Aba 'Operacao'
        operacao_sheet.append_table(operacao_data)

    def add_posto_trabalho(self, posto_trabalho_data: List[str]) -> None:
        posto_trabalho_sheet = self.sheet.worksheet(
            "title", "PostoTrabalho"
        )  # Aba 'PostoTrabalho'
        posto_trabalho_sheet.append_table(posto_trabalho_data)

    def add_defeito(self, defeito_data: List[str]) -> None:
        defeito_sheet = self.sheet.worksheet("title", "Defeito")  # Aba 'Defeito'
        defeito_sheet.append_table(defeito_data)

    def add_funcionario(self, funcionario_data: List[str]) -> None:
        funcionario_sheet = self.sheet.worksheet(
            "title", "Funcionario"
        )  # Aba 'Funcionario'
        funcionario_sheet.append_table(funcionario_data)

    def add_produto_tarefas(self, produto_tarefas_data: List[str]) -> None:
        produto_tarefas_sheet = self.sheet.worksheet(
            "title", "Produto_tarefas"
        )  # Aba 'Produto_tarefas'
        produto_tarefas_sheet.append_table(produto_tarefas_data)

    def add_produto(self, produto_data: List[str]) -> None:
        produto_sheet = self.sheet.worksheet("title", "Produto")  # Aba 'Produto'
        produto_sheet.append_table(produto_data)

    def add_cliente(self, cliente_data: List[str]) -> None:
        cliente_sheet = self.sheet.worksheet("title", "Cliente")  # Aba 'Cliente'
        cliente_sheet.append_table(cliente_data)

    # Aqui, você pode adicionar mais funções conforme necessário para leitura e atualização
