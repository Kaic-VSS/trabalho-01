from enum import Enum
import random
import json
import os

ARQUIVO_CONFIG = "config.json"

class TipoAtivo(Enum):
    SOFTWARE = 1
    HARDWARE = 2
    NUVEM = 3
    DADOS = 4

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

def carregar_config():
    # Padrão inicial caso o arquivo não exista
    config_padrao = {
        "responsaveis": ["kaic", "camile", "igor"],
        "setores": [
            "data center / sala de servidores",
            "nuvem (local virtual)",
            "salas de reunião e diretoria",
            "recepção e portaria",
            "estoques e laboratório"
        ]
    }
    if not os.path.exists(ARQUIVO_CONFIG):
        salvar_config(config_padrao)
        return config_padrao
    try:
        with open(ARQUIVO_CONFIG, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return config_padrao

def salvar_config(config):
    with open(ARQUIVO_CONFIG, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=4)

def ID_unico(dicionario_ativos):
    while True:
        novo_id = random.randint(100000, 999999)
        if novo_id not in dicionario_ativos:
            return novo_id