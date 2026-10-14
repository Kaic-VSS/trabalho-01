from Funcao_ID import StatusVulnerabilidade, SeveridadeVulnerabilidade
import json

ARQUIVO_DADOS = "dados.json"
ARQUIVO_VULS = "vulnerabilidades.json"

def cadastrar_catalogo_vul():
    print("\n=== CADASTRO DE VULNERABILIDADE NO CATÁLOGO GLOBAL ===")
    nome = input("Nome da Vulnerabilidade: ").strip().lower()
    desc = input("Descrição detalhada: ").strip()

    print("\nSeveridades disponíveis:")
    for sev in SeveridadeVulnerabilidade:
        print(f"- {sev.value}")
    severidade = input("Digite a severidade: ").strip().lower()
    if severidade not in [s.value for s in SeveridadeVulnerabilidade]:
        print("❌ Erro: Severidade inválida.")
        return


    print("\nStatus padrão de tratamento:")
    for st in StatusVulnerabilidade:
        print(f"- {st.value}")
    status = input("Digite o status: ").strip().lower()
    if status not in [s.value for s in StatusVulnerabilidade]:
        print("❌ Erro: Status inválido.")
        return

    if not nome or not desc:
        print("❌ Erro: Campos obrigatórios em branco.")
        return

    try:
        with open(ARQUIVO_VULS, "r", encoding="utf-8") as f:
            lista_vuls = json.load(f)
    except FileNotFoundError:
        lista_vuls = []


    if any(v["Nome_Vulnerabilidade"] == nome for v in lista_vuls):
        print("⚠️ Esta vulnerabilidade já está cadastrada no catálogo global.")
        return

    nova_vul = {
        "Nome_Vulnerabilidade": nome,
        "Descricao": desc,
        "Severidade": severidade,
        "Status": status,
        "IDs_Ativos_Afetados": []  # Começa sem ativos vinculados
    }

    lista_vuls.append(nova_vul)

    with open(ARQUIVO_VULS, "w", encoding="utf-8") as f:
        json.dump(lista_vuls, f, ensure_ascii=False, indent=4)

    print(f"✅ Vulnerabilidade '{nome}' adicionada ao catálogo global com sucesso!")


def associar_vul_ativo():
    print("\n=== ASSOCIAR VULNERABILIDADE A UM ATIVO ===")
    
    # 1. Carrega Catálogo de Vulnerabilidades
    try:
        with open(ARQUIVO_VULS, "r", encoding="utf-8") as f:
            lista_vuls = json.load(f)
    except FileNotFoundError:
        lista_vuls = []

    if not lista_vuls:
        print("⚠️ O catálogo global de vulnerabilidades está vazio. Cadastre uma vulnerabilidade primeiro.")
        return

    print("\nVulnerabilidades disponíveis no Catálogo:")
    for i, v in enumerate(lista_vuls, 1):
        print(f"{i} - [{v['Severidade'].upper()}] {v['Nome_Vulnerabilidade']} (Status: {v['Status']})")

    try:
        escolha_vul = int(input("\nDigite o número da vulnerabilidade que deseja associar: "))
        vul_selecionada = lista_vuls[escolha_vul - 1]
    except (ValueError, IndexError):
        print("❌ Opção inválida.")
        return


    try:
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
            lista_ativos = json.load(f)
    except FileNotFoundError:
        lista_ativos = []

    if not lista_ativos:
        print("⚠️ Não há ativos cadastrados no sistema.")
        return

    print("\nAtivos disponíveis:")
    for a in lista_ativos:
        print(f"ID: {a['ID']} | Nome: {a['Nome']} | Setor: {a['Local']}")

    id_ass_str = input("\nDigite o ID do Ativo que receberá esta vulnerabilidade: ").strip()
    if not id_ass_str.isdigit():
        print("❌ Erro: ID inválido.")
        return
    id_associado = int(id_ass_str)

    if not any(a["ID"] == id_associado for a in lista_ativos):
        print("❌ Erro: ID de ativo não encontrado.")
        return

    if id_associado not in vul_selecionada["IDs_Ativos_Afetados"]:
        vul_selecionada["IDs_Ativos_Afetados"].append(id_associado)
        
        with open(ARQUIVO_VULS, "w", encoding="utf-8") as f:
            json.dump(lista_vuls, f, ensure_ascii=False, indent=4)
            
        print(f"✅ Vulnerabilidade '{vul_selecionada['Nome_Vulnerabilidade']}' associada com sucesso ao ativo ID {id_associado}!")
    else:
        print("⚠️ Este ativo já possui esta vulnerabilidade associada.")


def desassociar_vul_ativo():
    print("\n=== REMOVER VULNERABILIDADE DE UM ATIVO (CORRIGIDA) ===")
    
    try:
        with open(ARQUIVO_VULS, "r", encoding="utf-8") as f:
            lista_vuls = json.load(f)
    except FileNotFoundError:
        print("Nenhuma vulnerabilidade cadastrada.")
        return

    if not lista_vuls:
        print("⚠️ O catálogo global está vazio.")
        return


    vuls_com_ativos = [v for v in lista_vuls if v.get("IDs_Ativos_Afetados")]
    
    if not vuls_com_ativos:
        print("⚠️ Não há vulnerabilidades associadas a nenhum ativo no momento.")
        return

    print("\nVulnerabilidades atualmente associadas a ativos:")
    for i, v in enumerate(vuls_com_ativos, 1):
        print(f"{i} - [{v['Severidade'].upper()}] {v['Nome_Vulnerabilidade']} (Ativos afetados IDs: {v['IDs_Ativos_Afetados']})")

    try:
        escolha = int(input("\nDigite o número da vulnerabilidade que deseja desassociar de um ativo: "))
        vul_escolhida = vuls_com_ativos[escolha - 1]
    except (ValueError, IndexError):
        print("❌ Opção inválida.")
        return

    ids_afetados = vul_escolhida["IDs_Ativos_Afetados"]
    
    try:
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
            lista_ativos = json.load(f)
    except FileNotFoundError:
        lista_ativos = []

    ativos_vinculados = [a for a in lista_ativos if a["ID"] in ids_afetados]

    print("\nAtivos afetados por esta vulnerabilidade:")
    for a in ativos_vinculados:
        print(f"ID: {a['ID']} | Nome: {a['Nome']} | Setor: {a['Local']}")

    id_remover_str = input("\nDigite o ID do Ativo que teve a vulnerabilidade corrigida/removida: ").strip()
    if not id_remover_str.isdigit():
        print("❌ Erro: ID inválido.")
        return
    id_remover = int(id_remover_str)

    if id_remover in vul_escolhida["IDs_Ativos_Afetados"]:
        vul_escolhida["IDs_Ativos_Afetados"].remove(id_remover)
        
        with open(ARQUIVO_VULS, "w", encoding="utf-8") as f:
            json.dump(lista_vuls, f, ensure_ascii=False, indent=4)
            
        print(f"✅ Vulnerabilidade '{vul_escolhida['Nome_Vulnerabilidade']}' removida com sucesso do ativo ID {id_remover} (Corrigida)!")
    else:
        print("⚠️ Este ativo não possui esta vulnerabilidade associada.")


def consulta_Vul():
    print("\n==== CONSULTA DE VULNERABILIDADE ====")
    termo = input("Digite o nome da vulnerabilidade para buscar: ").strip().lower()
    if not termo:
        print("❌ Erro: Termo de busca vazio.")
        return

    try:
        with open(ARQUIVO_VULS, "r", encoding="utf-8") as f:
            lista_vuls = json.load(f)
    except FileNotFoundError:
        print("Nenhuma vulnerabilidade cadastrada.")
        return

    vuls_encontradas = [v for v in lista_vuls if termo in v["Nome_Vulnerabilidade"]]

    if vuls_encontradas:
        try:
            with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
                lista_ativos = json.load(f)
        except FileNotFoundError:
            lista_ativos = []

        print(f"\n--- Encontradas {len(vuls_encontradas)} vulnerabilidade(s) ---")
        for v in vuls_encontradas:
            print("-" * 40)
            print(f"Vulnerabilidade: {v['Nome_Vulnerabilidade'].upper()}")
            print(f"Descrição: {v['Descricao']}")
            print(f"Severidade: {v['Severidade'].upper()}")
            print(f"Status: {v['Status'].upper()}")
            
            ids_afetados = v.get("IDs_Ativos_Afetados", [])
            print("💻 Ativos Afetados:")
            ativos_af = [a for a in lista_ativos if a["ID"] in ids_afetados]
            if ativos_af:
                for a in ativos_af:
                    print(f"   - ID: {a['ID']} | Nome: {a['Nome']} | Setor: {a['Local']}")
            else:
                print("   - Nenhum ativo associado a esta vulnerabilidade no momento.")
        print("-" * 40)
    else:
        print("Nenhuma vulnerabilidade encontrada.")


def atualizar_Vul():
    print("\n==== ATUALIZAÇÃO DE VULNERABILIDADE ====")
    nome_busca = input("Nome da Vulnerabilidade do Catálogo que deseja atualizar: ").strip().lower()
    
    try:
        with open(ARQUIVO_VULS, "r", encoding="utf-8") as f:
            lista_vuls = json.load(f)
    except FileNotFoundError:
        print("Nenhuma vulnerabilidade cadastrada.")
        return

    vul = next((v for v in lista_vuls if v["Nome_Vulnerabilidade"] == nome_busca), None)
    if not vul:
        print("❌ Vulnerabilidade não encontrada.")
        return

    print(f"\nAtualizando: {vul['Nome_Vulnerabilidade']} | Status Atual: {vul['Status']} | Risco Atual: {vul['Severidade']}")
    
    nova_sev = input("Nova severidade (baixa/media/alta/critica) [Enter para manter]: ").strip().lower()
    if nova_sev in [s.value for s in SeveridadeVulnerabilidade]:
        vul['Severidade'] = nova_sev

    novo_status = input("Novo status (aberta/em tratamento/corrigida/aceita como risco) [Enter para manter]: ").strip().lower()
    if novo_status in [s.value for s in StatusVulnerabilidade]:
        vul['Status'] = novo_status

    with open(ARQUIVO_VULS, "w", encoding="utf-8") as f:
        json.dump(lista_vuls, f, ensure_ascii=False, indent=4)
    print("✅ Vulnerabilidade atualizada com sucesso!")


def remover_Vul():
    print("\n==== REMOÇÃO DE VULNERABILIDADE (DO CATÁLOGO) ====")
    nome_vul = input("Nome da Vulnerabilidade a remover do catálogo: ").strip().lower()
    
    try:
        with open(ARQUIVO_VULS, "r", encoding="utf-8") as f:
            lista_vuls = json.load(f)
    except FileNotFoundError:
        print("Nenhuma vulnerabilidade cadastrada.")
        return

    vul = next((v for v in lista_vuls if v["Nome_Vulnerabilidade"] == nome_vul), None)
    if not vul:
        print("❌ Vulnerabilidade não encontrada.")
        return

    certeza = input("Tem certeza da remoção do catálogo? (S/N): ").strip().lower()
    if certeza == "s":
        lista_vuls.remove(vul)
        with open(ARQUIVO_VULS, "w", encoding="utf-8") as f:
            json.dump(lista_vuls, f, ensure_ascii=False, indent=4)
        print("✅ Vulnerabilidade removida do catálogo com sucesso!")
    else:
        print("Operação cancelada.")