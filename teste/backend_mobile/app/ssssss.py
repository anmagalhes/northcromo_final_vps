let
    // Conexão com a fonte
    Fonte = Sql.Database("nywwvmgpdgoulnv3u37zpwgnxq-dsjrssax5kfungsvyjtdpnl65u.datawarehouse.fabric.microsoft.com", "Frota_Lakehouse"),

    // Tabela 1: Ordem de Serviço
    OrdemServico = Fonte{[Schema="dbo", Item="tb_ordemservico"]}[Data],
    OrdemServicoComData = Table.TransformColumns(OrdemServico, {{"created_at", each DateTime.FromText(_, "pt-BR"), type datetime}}),

    // Tabela 2: Dados Rembolso com apenas colunas desejadas + distinct por os_codigoManutencaoOficina
    DadosRembolsoRaw = Fonte{[Schema="dbo", Item="tb_dadosrembolsodetalhado_1"]}[Data],
    DadosRembolsoTratado = Table.Distinct(
        Table.SelectColumns(
            Table.TransformColumns(DadosRembolsoRaw, {{"created_at", each DateTime.FromText(_, "pt-BR"), type datetime}}),
            {
                "codigoTitulo",
                "dataEmissao",
                "informacaoAdicional1_descricao",
                "notaFiscalFaturamento",
                "os_codigoManutencaoOficina",
                "os_veiculo_frota",
                "os_veiculo_informacaoAdicional2_descricao",
                "os_veiculo_informacaoAdicional3_descricao",
                "os_veiculo_informacaoAdicional4_descricao",
                "os_codigoTransacao"  // necessário para o join
            }
        ),
        {"os_codigoManutencaoOficina"}
    ),

    // JOIN entre OrdemServico e DadosRembolso
    MergeRembolso = Table.NestedJoin(
        OrdemServicoComData,
        {"ordem_codigoTransacao"},
        DadosRembolsoTratado,
        {"os_codigoTransacao"},
        "DadosRembolso",
        JoinKind.LeftOuter
    ),

    // Expande as colunas desejadas
    ExpandidoRembolso = Table.ExpandTableColumn(
        MergeRembolso,
        "DadosRembolso",
        {
            "codigoTitulo",
            "dataEmissao",
            "informacaoAdicional1_descricao",
            "notaFiscalFaturamento",
            "os_codigoManutencaoOficina",
            "os_veiculo_frota",
            "os_veiculo_informacaoAdicional2_descricao",
            "os_veiculo_informacaoAdicional3_descricao",
            "os_veiculo_informacaoAdicional4_descricao"
        }
    ),

    // Adiciona a coluna 'resposta_nova_coluna' baseada na presença de dados na tabela 'DadosRembolso'
    AddRespostaColuna = Table.AddColumn(ExpandidoRembolso, "resposta_nova_coluna", each if [codigoTitulo] <> null then "DETALHAMENTO_NOTA" else "VEICULOS"),
    #"Linhas Filtradas" = Table.SelectRows(AddRespostaColuna, each ([ordem_codigoAprovador] = "122108")),



    // Definindo a lista de status para evitar repetições
    StatusList = {"FINALIZADA", "UBSTITUÍD", "REPROVADA", "CANCELADA", "COBRADA"},

    // Adiciona a coluna 'STATUS_ORDEM_FINAL' com base na lista de status
    AddStatusFinal = Table.AddColumn(#"Linhas Filtradas", "STATUS_ORDEM_FINAL", each
        if List.AnyTrue(List.Transform(StatusList, (status) => Text.Contains(Text.Upper([ordem_statusOrdemServico]), status))) then "FINALIZADA"
        else "EM ABERTO"
    ),

    // Adiciona a coluna 'DESCONSIDERAR_ORDENDA' para desconsiderar ordens com status específicos
    AddDesconsiderar = Table.AddColumn(AddStatusFinal, "DESCONSIDERAR_ORDENDA", each
        if List.AnyTrue(List.Transform(StatusList, (status) => Text.Contains(Text.Upper([ordem_statusOrdemServico]), status))) then 1
        else 0
    ),


    // Calcula a data atual uma única vez e aplica a todas as linhas
    DataAtual = DateTime.LocalNow(),
    AddDataAtual = Table.AddColumn(AddDesconsiderar, "DATA_ATUAL", each DataAtual, type datetime),

    AddOrdemDataUltimaModificacao_DT = Table.AddColumn(
    AddDataAtual,
    "ordem_dataUltimaModificacao_DT",
    each try DateTimeZone.FromText(Text.From([ordem_dataUltimaModificacao])) otherwise null,
    type datetimezone
),
    #"Tipo Alterado" = Table.TransformColumnTypes(AddOrdemDataUltimaModificacao_DT,{{"ordem_dataUltimaModificacao_DT", type datetime}}),


    // Adiciona um índice sequencial
AddRowNum = Table.AddIndexColumn(#"Tipo Alterado", "RowNum", 1, 1, Int64.Type),

// Agrupa por ordem e data para pegar a última modificação
AgrupaMaxData = Table.Group(AddRowNum, {"ordem_codigoManutencaoOficina", "ordem_dataUltimaModificacao"}, {
    {"MaxData", each List.Max([ordem_dataUltimaModificacao]), type datetimezone}
}),

// Renomeia as colunas do agrupamento
RenomeiaAgrupamento = Table.RenameColumns(AgrupaMaxData, {
    {"ordem_codigoManutencaoOficina", "ordem_codigoManutencaoOficina_Max"},
    {"ordem_dataUltimaModificacao", "ordem_dataUltimaModificacao_Max"}
}),


// Faz o join com base na data máxima
MergeMaxData = Table.Join(
    AddRowNum,
    {"ordem_codigoManutencaoOficina", "ordem_dataUltimaModificacao"},
    RenomeiaAgrupamento,
    {"ordem_codigoManutencaoOficina_Max", "ordem_dataUltimaModificacao_Max"},
    JoinKind.LeftOuter
),

// Ordena os dados
TabelaOrdenada = Table.Sort(RemoveUnnecessaryColumns, {
    {"ordem_codigoManutencaoOficina", Order.Ascending},
    {"item_codigoManutencaoOficinaItem", Order.Ascending},
    {"ordem_dataUltimaModificacao", Order.Descending}
}),

// Adiciona índice geral
TabelaComIndice = Table.AddIndexColumn(TabelaOrdenada, "Index", 1, 1, Int64.Type),

// Cria versão deslocada (linha anterior)
TabelaAnterior = Table.RenameColumns(
    Table.SelectColumns(TabelaComIndice, {
        "ordem_codigoManutencaoOficina",
        "item_codigoManutencaoOficinaItem",
        "ordem_statusOrdemServico",
        "ordem_dataUltimaModificacao",
        "ordem_alcadaAprovacao",
        "Index"
    }),
    {
        {"ordem_statusOrdemServico", "ordem_statusOrdemServico_Penultima"},
        {"ordem_dataUltimaModificacao", "ordem_dataUltimaModificacao_Penultima"},
        {"ordem_alcadaAprovacao", "ordem_alcadaAprovacao_Penultima"},
        {"Index", "IndexAnterior"}
    }
),

// Junta com base na mesma ordem, item e índice anterior
MergePenultima = Table.NestedJoin(
    TabelaComIndice,
    {"ordem_codigoManutencaoOficina", "item_codigoManutencaoOficinaItem", "Index"},
    TabelaAnterior,
    {"ordem_codigoManutencaoOficina", "item_codigoManutencaoOficinaItem", "IndexAnterior"},
    "Penultima",
    JoinKind.LeftOuter
),

ExpandePenultima = Table.ExpandTableColumn(
    MergePenultima,
    "Penultima",
    {
        "ordem_statusOrdemServico_Penultima",
        "ordem_dataUltimaModificacao_Penultima",
        "ordem_alcadaAprovacao_Penultima"
    }
),

// Agora faz o merge ignorando o item
TabelaAnteriorOrdem = Table.RenameColumns(
    Table.SelectColumns(TabelaComIndice, {
        "ordem_codigoManutencaoOficina",
        "ordem_statusOrdemServico",
        "ordem_dataUltimaModificacao",
        "Index"
    }),
    {
        {"ordem_statusOrdemServico", "ordem_statusOrdemServico_Penultima"},
        {"ordem_dataUltimaModificacao", "ordem_dataUltimaModificacao_Penultima"},
        {"Index", "IndexAnterior_Ordem"}
    }
),

MergePenultimaOrdem = Table.NestedJoin(
    ExpandePenultima,
    {"ordem_codigoManutencaoOficina", "Index"},
    TabelaAnteriorOrdem,
    {"ordem_codigoManutencaoOficina", "IndexAnterior_Ordem"},
    "PenultimaOrdem",
    JoinKind.LeftOuter
),

ExpandePenultimaOrdem = Table.ExpandTableColumn(
    MergePenultimaOrdem,
    "PenultimaOrdem",
    {
        "ordem_statusOrdemServico_Penultima",
        "ordem_dataUltimaModificacao_Penultima"
    },
    {
        "ordem_statusOrdemServico_Penultima_ordem",
        "ordem_dataUltimaModificacao_Penultima_ordem"
    }
),

// Coluna auxiliar
AddAlcadaAprovacaoAnterior = Table.AddColumn(ExpandePenultimaOrdem, "ordem_alcadaAprovacao_Anterior", each [ordem_alcadaAprovacao]),

// Seleciona colunas finais, incluindo as colunas originais
SelecionaColunas = Table.SelectColumns(AddAlcadaAprovacaoAnterior,
    List.Combine({
        // Colunas originais
        Table.ColumnNames(AddDataAtual),
        // Colunas novas
        {
            "ordem_statusOrdemServico_Penultima",
            "ordem_statusOrdemServico_Penultima_ordem",
            "ordem_dataUltimaModificacao_Penultima",
            "ordem_dataUltimaModificacao_Penultima_ordem",
            "ordem_alcadaAprovacao_Penultima"
        }
    })
),






// Cria colunas temporárias com textos já formatados
AddColunasTemp = Table.AddColumn(SelecionaColunas, "status_atual", each Text.Upper(Text.Trim([ordem_statusOrdemServico]))),
AddColunasTemp2 = Table.AddColumn(AddColunasTemp, "status_penultimo", each Text.Upper(Text.Trim([ordem_statusOrdemServico_Penultima]))),

// Adiciona a coluna de análise
AddAnaliseItem = Table.AddColumn(AddColunasTemp2, "Analise_Item", each
    if [status_atual] <> "NÃO ENVIADAS AO CLIENTE" and [status_penultimo] = "NÃO ENVIADAS AO CLIENTE" then "DESATUALIZADO"
    else if [status_atual] = "NÃO ENVIADAS AO CLIENTE" and [status_penultimo] = "NÃO ENVIADAS AO CLIENTE" then "ATUALIZADO"
    else if [ordem_statusOrdemServico_Penultima] = null then "TESTE"
    else "ATUALIZADO"
),


// Garantir conversão correta para DateTime
AddOrdemDataHora = Table.AddColumn(AddAnaliseItem, "OrdemDataHora", each try DateTime.From([ordem_dataUltimaModificacao_DT]) otherwise null),

// Separar Data e Hora
AddDataSeparada = Table.AddColumn(AddOrdemDataHora, "dataUltimaModificacao_Data_v2", each try Date.From([ordem_dataUltimaModificacao_DT]) otherwise null),
AddHoraSeparada = Table.AddColumn(AddDataSeparada, "dataUltimaModificacao_Hora", each try Time.From([ordem_dataUltimaModificacao_DT]) otherwise null),

// Tempo de Espera (em dias)
AddTempoEspera = Table.AddColumn(AddHoraSeparada, "TEMPO_ESPERA", each
    let
        atual = [ordem_dataUltimaModificacao_DT],
        penultima = [ordem_dataUltimaModificacao_Penultima_ordem],
        status = Text.Upper(Text.Trim([ordem_statusOrdemServico]))
    in
        if status = "COBRADA" or status = "COBRADAS" or Text.Contains(status, "REPROVADA") or status = "SUBSTITUÍDA" or status = "SUSTITUIDA" then
            Duration.Days(DateTime.From(atual) - DateTime.From(penultima))
        else if penultima <> null then
            Duration.Days(DateTime.From(atual) - DateTime.From(penultima))
        else
            Duration.Days(DateTime.LocalNow() - DateTime.From(atual))
),

// Criar coluna com created_at convertido e 10h adicionadas
AddCreatedAtConverted = Table.AddColumn(AddTempoEspera, "created_at_converted", each try DateTime.FromText(Text.Middle([created_at], 6, 4) & "-" & Text.Middle([created_at], 3, 2) & "-" & Text.Start([created_at], 2)) otherwise null),
AddCreatedAt10h = Table.AddColumn(AddCreatedAtConverted, "created_at_10am", each try DateTime.AddHours([created_at_converted], 10) otherwise null),

// Ajustar fuso para ordem_dataUltimaModificacao
AddOrdemDataModifConvertida = Table.AddColumn(AddCreatedAt10h, "ordem_dataUltimaModificacao_converted", each try DateTimeZone.SwitchZone(DateTimeZone.From([ordem_dataUltimaModificacao]), -3) otherwise null),

// TEMPO_ESPERA_TESTE (em segundos)
AddTempoEsperaTeste = Table.AddColumn(AddOrdemDataModifConvertida, "TEMPO_ESPERA_TESTE", each
    let
        atual = [ordem_dataUltimaModificacao_converted],
        penultima = [ordem_dataUltimaModificacao_Penultima],
        created = [created_at_10am],
        hoje = DateTime.LocalNow(),
        hoje_1520 = DateTime.From(Date.From(hoje) & " 15:20:00")
    in
        if Date.From(atual) = Date.From(penultima) then
            Duration.Seconds(atual - penultima)
        else if Date.From(atual) = Date.From(hoje) and DateTime.Hour(atual) >= 10 then
            Duration.Seconds(hoje_1520 - atual)
        else if created <> null and atual <> null then
            Duration.Seconds(atual - created)
        else
            null
),

// DATA_TRANSACAO
AddDataTransacao = Table.AddColumn(AddTempoEsperaTeste, "DATA_TRANSACAO", each
    if Text.Upper(Text.Trim([ordem_statusOrdemServico])) = "COBRADAS" then [dataUltimaModificacao_Data_v2]
    else null)
in
    AddDataTransacao
