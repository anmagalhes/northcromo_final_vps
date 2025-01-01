import asyncio
import asyncpg


# Função para listar tabelas e colunas
async def listar_tabelas_e_colunas():
    # Conectar ao banco de dados PostgreSQL
    conn = await asyncpg.connect(
        "postgresql://flask_user:tonyteste@147.93.12.171:5432/northcromo"
    )

    # Consulta para listar todas as tabelas no banco de dados
    tabelas_result = await conn.fetch(
        "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"
    )

    # Exibe todas as tabelas
    print("Tabelas no banco de dados:")

    for row in tabelas_result:
        tabela_nome = row["table_name"]
        print(f"\nTabela: {tabela_nome}")

        # Consulta para listar todas as colunas da tabela
        colunas_result = await conn.fetch(
            """
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_name = $1;
            """,
            tabela_nome,
        )

        # Exibe todas as colunas da tabela
        if colunas_result:
            print(f"Colunas de {tabela_nome}:")
            for coluna in colunas_result:
                print(f"- {coluna['column_name']} ({coluna['data_type']})")
        else:
            print(f"Sem colunas encontradas para a tabela {tabela_nome}")

    await conn.close()


# Executa a função de listagem de tabelas e colunas
asyncio.run(listar_tabelas_e_colunas())
