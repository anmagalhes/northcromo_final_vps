from enum import Enum


# Enum para tipo de ordem
class TipoOrdemEnum(str, Enum):
    NOVO = "NOVO"
    NAO = "NAO"


# Enum para Sim/Não
class SimNaoEnum(str, Enum):
    SIM = "SIM"
    NAO = "NAO"


# Enum para status dos processos
class ProcessosOrdemEnum(str, Enum):
    INICIADO = "iniciado"
    FINALIZADO = "finalizado"
    PENDENTE = "pendente"


class StatusOrdemEnum(str, Enum):
    PENDENTE = "PENDENTE"  # Status 1 - Pendente
    FINALIZADO = "FINALIZADO"  # Status 5 - Finalizado
    CANCELADO = "CANCELADO"  # Status 3 - Cancelado
    EM_ANDAMENTO = "EM_ANDAMENTO"
