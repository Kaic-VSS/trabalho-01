from Funcao_ID import TipoAtivo, ID_unico, carregar_config, salvar_config
import json

ARQUIVO_DADOS = "dados.json"
ARQUIVO_VULS = "vulnerabilidades.json"

def carregar_dados():
    try:
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as arquivo:
            dados_lista = json.load(arquivo)
            return {item["ID"]: item for item in dados_lista}
    except FileNotFoundError:
        return {}

def salvar_dados(dicionario_ativos):
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as arquivo:
        json.dump(list(dicionario_ativos.values()), arquivo, ensure_ascii=False, indent=4)

def gerenciar_responsaveis_setores():
    config = carregar_config()
    while True:
        print("\n=== GERENCIAR RESPONSÁVEIS E SETORES ===")
        print("1 - Listar Responsáveis e Setores")
        print("2 - Adicionar novo Responsável")
        print("3 - Remover Responsável")
        print("4 - Adicionar novo Setor")
        print("5 - Remover Setor")
        print("6 - Voltar ao Menu de Ativos")
        
        op = input("Escolha uma opção: ").strip()
        
        if op == "1":
            print("\n--- Responsáveis ---")
            for i, r in enumerate(config["responsaveis"], 1):
                print(f"{i} - {r.title()}")
            print("\n--- Setores ---")
            for i, s in enumerate(config["setores"], 1):
                print(f"{i} - {s.title()}")
                
        elif op == "2":
            novo_r = input("Nome do novo responsável: ").strip().lower()
            if novo_r and novo_r not in config["responsaveis"]:
                config["responsaveis"].append(novo_r)
                salvar_config(config)
                print(f"Responsável '{novo_r.title}' adicionado com sucesso!")
            else:
                print("Nome inválido ou já existente.")
                
        elif op == "3":
            print("\nResponsáveis atuais:")
            for i, r in enumerate(config["responsaveis"], 1):
                print(f"{i} - {r.title()}")
            try:
                idx = int(input("Número do responsável para remover: ")) - 1
                if 0 <= idx < len(config["responsaveis"]):
                    removido = config["responsaveis"].pop(idx)
                    salvar_config(config)
                    print(f"Responsável '{removido.title}' removido com sucesso!")
                else:
                    print("Opção inválida.")
            except ValueError:
                print("Entrada inválida.")
                
        elif op == "4":
            novo_s = input("Nome do novo setor: ").strip().lower()
            if novo_s and novo_s not in config["setores"]:
                config["setores"].append(novo_s)
                salvar_config(config)
                print(f"Setor '{novo_s.title}' adicionado com sucesso!")
            else:
                print("Setor inválido ou já existente.")
                
        elif op == "5":
            print("\nSetores atuais:")
            for i, s in enumerate(config["setores"], 1):
                print(f"{i} - {s.title()}")
            try:
                idx = int(input("Número do setor para remover: ")) - 1
                if 0 <= idx < len(config["setores"]):
                    removido = config["setores"].pop(idx)
                    salvar_config(config)
                    print(f"Setor '{removido.title}' removido com sucesso!")
                else:
                    print("Opção inválida.")
            except ValueError:
                print("Entrada inválida.")
                
        elif op == "6":
            break
        else:
            print("Opção inválida!")

def cadastro_At():
    print("\n=== CADASTRO DE ATIVO ===")
    nome = input("Nome/Hostname do ativo: ").strip().lower()
    
    config = carregar_config()
    
    # Seleção de Responsável
    print("\nSelecione o Responsável:")
    for i, r in enumerate(config["responsaveis"], 1):
        print(f"{i} - {r.title()}")
    print(f"{len(config['responsaveis']) + 1} - [Cadastrar novo responsável]")
    
    try:
        esc_resp = int(input("Escolha o número correspondente: "))
        if esc_resp == len(config["responsaveis"]) + 1:
            resp = input("Digite o nome do novo responsável: ").strip().lower()
            if resp and resp not in config["responsaveis"]:
                config["responsaveis"].append(resp)
                salvar_config(config)
        elif 1 <= esc_resp <= len(config["responsaveis"]):
            resp = config["responsaveis"][esc_resp - 1]
        else:
            print("Opção inválida. Cadastro cancelado.")
            return
    except ValueError:
        print("Entrada inválida. Cadastro cancelado.")
        return

    # Seleção de Setor
    print("\nSelecione o Setor ou Localização:")
    for i, s in enumerate(config["setores"], 1):
        print(f"{i} - {s.title()}")
    print(f"{len(config['setores']) + 1} - [Cadastrar novo setor]")
    
    try:
        esc_setor = int(input("Escolha o número correspondente: "))
        if esc_setor == len(config["setores"]) + 1:
            local = input("Digite o nome do novo setor: ").strip().lower()
            if local and local not in config["setores"]:
                config["setores"].append(local)
                salvar_config(config)
        elif 1 <= esc_setor <= len(config["setores"]):
            local = config["setores"][esc_setor - 1]
        else:
            print("Opção inválida. Cadastro cancelado.")
            return
    except ValueError:
        print("Entrada inválida. Cadastro cancelado.")
        return

    print("\nSelecione o Tipo de Ativo (Requisito 2):")
    for tipo in TipoAtivo:
        print(f"{tipo.value} - {tipo.name.replace('_', ' ')}")
    
    try:
        escolha_tipo = int(input("Digite o número da categoria: "))
        tipo_obj = TipoAtivo(escolha_tipo)
    except (ValueError, KeyError, TypeError):
        print("Erro: Tipo de ativo inválido. Cadastro cancelado.")
        return

    if not nome:
        print("Erro: O nome do ativo é obrigatório.")
        return

    dicionario_ativos = carregar_dados()
    novo_id = ID_unico(dicionario_ativos)

    dicionario_ativos[novo_id] = {
        "ID": novo_id,
        "Nome": nome,
        "Tipo": tipo_obj.name,
        "Tipo_Codigo": tipo_obj.value,
        "Responsavel": resp,
        "Local": local
    }

    salvar_dados(dicionario_ativos)
    print(f"\nAtivo cadastrado com sucesso! ID gerado: {novo_id}")

def consulta_At():
    print("\n==== CONSULTA DE ATIVO ====")
    termo = input("Digite o ID, Nome, Responsável ou Local para buscar: ").strip().lower()
    if not termo:
        print("Erro: Termo de busca vazio.")
        return

    dicionario_ativos = carregar_dados()
    if not dicionario_ativos:
        print("Nenhum ativo cadastrado.")
        return

    encontrados = []
    for ativo in dicionario_ativos.values():
        if (termo in str(ativo["ID"]) or 
            termo in ativo["Nome"] or 
            termo in ativo["Responsavel"] or 
            termo in ativo["Local"] or
            termo in ativo["Tipo"].lower()):
            encontrados.append(ativo)

    if encontrados:
        try:
            with open(ARQUIVO_VULS, "r", encoding="utf-8") as f:
                lista_vuls = json.load(f)
        except FileNotFoundError:
            lista_vuls = []

        print(f"\n--- Foram encontrados {len(encontrados)} ativo(s) ---")
        for ativo in encontrados:
            print("-" * 40)
            print(f"ID: {ativo['ID']}")
            print(f"Nome: {ativo['Nome'].upper()}")
            print(f"Tipo: {ativo['Tipo']} (Cód: {ativo['Tipo_Codigo']})")
            print(f"Responsável: {ativo['Responsavel'].title()}")
            print(f"Local: {ativo['Local'].title()}")
            
            vuls_do_ativo = [v for v in lista_vuls if ativo['ID'] in v.get("IDs_Ativos_Afetados", [])]
            print("Vulnerabilidades Associadas:")
            if vuls_do_ativo:
                for v in vuls_do_ativo:
                    print(f"   - [{v['Severidade'].upper()}] {v['Nome_Vulnerabilidade']}: {v['Descricao']} (Status: {v['Status']})")
            else:
                print("   - Este ativo está sem vulnerabilidades registradas.")
            print("-" * 40)
    else:
        print("Nenhum ativo encontrado com esse critério.")

def atualizar_At():
    print("\n==== ATUALIZAÇÃO DE ATIVO ====")
    id_alvo_str = input("Digite o ID numérico do Ativo que deseja atualizar: ").strip()
    if not id_alvo_str.isdigit():
        print("Erro: ID inválido.")
        return
    
    id_alvo = int(id_alvo_str)
    dicionario_ativos = carregar_dados()

    if id_alvo not in dicionario_ativos:
        print("Ativo não encontrado.")
        return

    ativo = dicionario_ativos[id_alvo]
    print(f"\nEditando ativo: {ativo['Nome']} (ID: {ativo['ID']})")
    print(f"Atual -> Responsável: {ativo['Responsavel'].title()} | Local: {ativo['Local'].title()}")
    print("Deixe em branco e aperte Enter para manter o valor atual.")

    novo_nome = input(f"Novo Nome [{ativo['Nome']}]: ").strip().lower()
    
    config = carregar_config()
    print("\nNovo Responsável (Deixe em branco para manter):")
    for i, r in enumerate(config["responsaveis"], 1):
        print(f"{i} - {r.title()}")
    escolha_r = input("Escolha o número ou Enter para pular: ").strip()
    
    novo_resp = ativo['Responsavel']
    if escolha_r.isdigit():
        idx = int(escolha_r) - 1
        if 0 <= idx < len(config["responsaveis"]):
            novo_resp = config["responsaveis"][idx]

    print("\nNovo Setor/Local (Deixe em branco para manter):")
    for i, s in enumerate(config["setores"], 1):
        print(f"{i} - {s.title()}")
    escolha_s = input("Escolha o número ou Enter para pular: ").strip()
    
    novo_local = ativo['Local']
    if escolha_s.isdigit():
        idx = int(escolha_s) - 1
        if 0 <= idx < len(config["setores"]):
            novo_local = config["setores"][idx]

    if novo_nome: ativo['Nome'] = novo_nome
    ativo['Responsavel'] = novo_resp
    ativo['Local'] = novo_local

    salvar_dados(dicionario_ativos)
    print("\nAtivo atualizado com sucesso!")

def remover_At():
    print("\n==== REMOÇÃO DE ATIVO ====")
    id_alvo_str = input("Digite o ID numérico do Ativo que deseja remover: ").strip()
    if not id_alvo_str.isdigit():
        print("Erro: ID inválido.")
        return
    
    id_alvo = int(id_alvo_str)
    dicionario_ativos = carregar_dados()

    if id_alvo not in dicionario_ativos:
        print("Ativo não encontrado.")
        return

    print(f"Ativo selecionado: {dicionario_ativos[id_alvo]['Nome']} (ID: {id_alvo})")
    certeza = input("Tem certeza da remoção? Isso removerá o vínculo com as vulnerabilidades (S/N): ").strip().lower()

    if certeza == "s":
        del dicionario_ativos[id_alvo]
        salvar_dados(dicionario_ativos)

        try:
            with open(ARQUIVO_VULS, "r", encoding="utf-8") as f:
                lista_vuls = json.load(f)
        except FileNotFoundError:
            lista_vuls = []

        for v in lista_vuls:
            if id_alvo in v.get("IDs_Ativos_Afetados", []):
                v["IDs_Ativos_Afetados"].remove(id_alvo)

        with open(ARQUIVO_VULS, "w", encoding="utf-8") as f:
            json.dump(lista_vuls, f, ensure_ascii=False, indent=4)

        print("Ativo removido com sucesso e vulnerabilidades atualizadas em cascata!")
    else:
        print("Remoção cancelada.")