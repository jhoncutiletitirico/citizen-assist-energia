"""
main.py - Citizen Assist AI com o simulador de energia
GS 2026.2 - Soluções em Energias Renováveis e Sustentáveis (SERS)

Jhon Cutile Titirico - RM 571976 - Turma 1CCPI

O que é desta disciplina: a opção 5 do menu (energia.py), as premissas em
data/premissas_energia.json e as orientações 13, 14 e 15 da base.

Como rodar (dentro da pasta citizen-assist-energia):  python main.py
"""

from assistente import Assistente, ler_opcao
from base_conhecimento import BaseConhecimento
from energia import SimuladorEnergia, atendimento_energia


def main():
    base = BaseConhecimento("data/base_conhecimento.json")
    if not base.carregar():
        print("Não foi possível abrir a base de conhecimento. Confira a pasta data/.")
        return

    simulador = SimuladorEnergia("data/premissas_energia.json")
    energia_ok = simulador.carregar()

    assistente = Assistente("Citizen Assist AI", base)

    print("=" * 62)
    print(f"  {assistente.nome} - Pessoas idosas (60+) e uso consciente de energia")
    print("=" * 62)
    print("Este assistente NÃO é canal oficial e NÃO pede seus dados pessoais.")

    while True:
        print("\n------------- MENU -------------")
        print(" 1 - Fazer uma pergunta")
        print(" 2 - Navegar por categorias")
        print(" 3 - Ver indicadores")
        print(" 4 - Exportar atendimentos (CSV)")
        print(" 5 - Simulador de economia de energia")
        print(" 0 - Sair")
        opcao = ler_opcao("Escolha uma opção: ", 0, 5)

        if opcao == 1:
            assistente.perguntar()
        elif opcao == 2:
            assistente.navegar()
        elif opcao == 3:
            assistente.indicadores()
        elif opcao == 4:
            assistente.exportar_csv()
        elif opcao == 5:
            if energia_ok:
                atendimento_energia(assistente, simulador)
            else:
                print("Simulador indisponível: confira o arquivo data/premissas_energia.json.")
        else:
            assistente.pedir_nota()
            assistente.exportar_csv()
            print("Até logo! Procure sempre os canais oficiais.")
            break


main()
