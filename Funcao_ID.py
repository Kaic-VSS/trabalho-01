from enum import Enum
import random

class TipoAtivo(Enum):
    Software = 1
    Hardware = 2
    Nuvem = 3
    Dados = 4

class StatusVulnerabilidade(Enum):
    ABERTA = "aberta"
    EM_TRATAMENTO = "em tratamento"
    CORRIGIDA = "corrigida"
    ACEITA_COMO_RISCO = "aceita como risco"

class SeveridadeVulnerabilidade(Enum):
    BAIXA = "baixa"
    MEDIA = "media"
    ALTA = "alta"
    CRITICA = "critica"

def ID_unico(dicionario_ativos):
    while True:
        novo_id = random.randint(100000, 999999)
        if novo_id not in dicionario_ativos:
            return novo_id