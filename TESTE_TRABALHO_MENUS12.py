from TESTE_TRABALHO_FUNCAO_ATV import cadastro_At, consulta_At, atualizar_At, remover_At
from TESTE_TRABALHO_FUNCAO_VUL import cadastrar_catalogo_vul, consulta_Vul, atualizar_Vul, remover_Vul, associar_vul_ativo, desassociar_vul_ativo

def menu_ativos():
    while True:
        print("\n======== MENU ATIVOS ========")
        print("1 - Cadastrar Ativo")
        print("2 - Consultar Ativo")
        print("3 - Atualizar Ativo")
        print("4 - Remover Ativo")
        print("5 - Voltar ao Menu Principal")
        
        op = input("Escolha uma opção: ").strip()
        
        if op == "1": cadastro_At()
        elif op == "2": consulta_At()
        elif op == "3": atualizar_At()
        elif op == "4": remover_At()
        elif op == "5": break
        else: print("❌ Opção inválida!")

def menu_vulnerabilidades():
    while True:
        print("\n======== MENU VULNERABILIDADES ========")
        print("1 - Cadastrar Nova Vulnerabilidade no Catálogo Global")
        print("2 - Associar Vulnerabilidade a um Ativo")
        print("3 - Remover Vulnerabilidade de um Ativo")
        print("4 - Consultar Vulnerabilidade")
        print("5 - Atualizar Vulnerabilidade")
        print("6 - Remover Vulnerabilidade do Catálogo Global")
        print("7 - Voltar ao Menu Principal")
        
        op = input("Escolha uma opção: ").strip()
        
        if op == "1": cadastrar_catalogo_vul()
        elif op == "2": associar_vul_ativo()
        elif op == "3": desassociar_vul_ativo()
        elif op == "4": consulta_Vul()
        elif op == "5": atualizar_Vul()
        elif op == "6": remover_Vul()
        elif op == "7": break
        else: print("❌ Opção inválida!")