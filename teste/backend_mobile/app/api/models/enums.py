import enum


class SimNaoEnum(enum.Enum):
    SIM = "SIM"
    NAO = "NAO"


class TipoOrdemEnum(enum.Enum):
    NOVO = "NOVO"
    NAO = "NAO"
    SIM = "SIM"


class StatusOrdem(enum.Enum):
    PENDENTE = "PENDENTE"
    FINALIZADO = "FINALIZADO"
    CANCELADO = "CANCELADO"
    EM_ANDAMENTO = "EM_ANDAMENTO"


class StatusTarefaEnum(enum.Enum):
    PENDENTE = "PENDENTE"
    EM_ANDAMENTO = "EM_ANDAMENTO"
    FINALIZADO = "FINALIZADO"
