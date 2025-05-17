MEDIA LITROS CONSUMIDO =

VAR _DataLimite = [DATA LIMITE]  -- Defina a data limite aqui

-- Filtro de datas anteriores à data limite
VAR _FiltroDataAnterior =
    FILTER(
        ALLSELECTED(dcalendario[Data]),
        dcalendario[Data] < _DataLimite  -- Filtra apenas as datas anteriores a 13/01/2025
    )

-- Filtro de datas posteriores ou iguais à data limite
VAR _FiltroDataPosterior =
    FILTER(
        ALLSELECTED(dcalendario[Data]),
        dcalendario[Data] >= _DataLimite  -- Filtra apenas as datas posteriores ou iguais à data limite
    )

-- Filtro para as transações anteriores à data limite, com a modalidade COMBUSTIVEL
VAR _ModalidadeMotoFiltro_Anterior =
    CALCULATETABLE(
        FILTER(
            'FAT_TRANSACOES_VEICULOS_ABASTECIMENTO ',
            'FAT_TRANSACOES_VEICULOS_ABASTECIMENTO '[GRUPO VEICULO] = "FUNCIONAL" &&
            'FAT_TRANSACOES_VEICULOS_ABASTECIMENTO '[PARA_TRANSACIONADO] IN {"COMBUSTIVEL"}
        ),
        _FiltroDataAnterior  -- Aplica o filtro de data anterior
    )

-- Filtro para as transações posteriores ou iguais à data limite, com a modalidade COMBUSTIVEL
VAR _ModalidadeMotoFiltro_Posterior =
    CALCULATETABLE(
        FILTER(
            'vw_transacoes_veiculos',
            'vw_transacoes_veiculos'[GRUPO VEICULO] = "FUNCIONAL" &&
            'vw_transacoes_veiculos'[PARA_TRANSCIONADO] IN {"COMBUSTIVEL"}
        ),
        _FiltroDataPosterior  -- Aplica o filtro de data posterior
    )

-- Unifica as transações de ambas as tabelas e garante que estamos pegando os códigos de transação corretos
VAR _TransacoesUnificadas =
    UNION(
        SELECTCOLUMNS(
            _ModalidadeMotoFiltro_Anterior,
            "CODIGO_TRANSACAO", 'FAT_TRANSACOES_VEICULOS_ABASTECIMENTO '[NºIDENT.VEÍCULO_PRINCIPAL]
        ),
        SELECTCOLUMNS(
            _ModalidadeMotoFiltro_Posterior,
            "CODIGO_TRANSACAO", 'vw_transacoes_veiculos'[NºIDENT_VEÍCULO]
        )
    )

-- Calcula o número total de transações distintas
VAR _PlacasDistintasTotal = DISTINCT(_TransacoesUnificadas)



// Calcula a soma dos quilômetros rodados apenas para os registros filtrados
VAR _LitrosConsumidosAnterior=
    SUMX(
         _ModalidadeMotoFiltro_Anterior,
        'FAT_TRANSACOES_VEICULOS_ABASTECIMENTO '[LITROS]
    )

VAR _LitrosConsumidosPosterior=
    SUMX(
         _ModalidadeMotoFiltro_Posterior,
        'vw_transacoes_veiculos'[LITROS]
    )

-- TOTAL LITROS
VAR _RESULTADO =
 _LitrosConsumidosAnterior +  _LitrosConsumidosPosterior

-- Total de veiculos
VAR  _NumeroRegistros =
COUNTROWS(_PlacasDistintasTotal)

VAR _RESULTADO_FINAL =
CALCULATE(
        DIVIDE(_RESULTADO, _NumeroRegistros, 0)
    )

RETURN
_RESULTADO_FINAL
