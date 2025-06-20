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

# Aqui você adiciona seus enums novos para o projeto

class CargoFuncionario(enum.Enum):
    ADMIN = "ADMIN"
    DESENVOLVEDOR = "DESENVOLVEDOR"
    VENDEDOR = "VENDEDOR"
    MECANICO = "MECANICO"
    INSPETOR = "INSPETOR"

class NivelAcesso(enum.Enum):
    ADMIN = "ADMIN"
    GERENTE = "GERENTE"
    COMUM = "COMUM"

class StatusEnum(enum.Enum):
    ATIVO = "ATIVO"
    INATIVO = "INATIVO"
