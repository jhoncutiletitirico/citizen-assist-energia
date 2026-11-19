"""
teste_simulado.py - teste de uso SIMULADO do simulador de energia

Não consegui fazer o teste com pessoas de fora no prazo, então simulei 4 perfis.
Cada perfil é uma sequência de teclas digitada no main.py de verdade (opção 5 com
números de uma conta de luz típica + perguntas livres). O programa grava o
historico.json e o atendimentos.csv normalmente.

Como rodar (dentro da pasta citizen-assist-energia):  python testes/teste_simulado.py
Atenção: apaga o histórico anterior antes de começar.
"""

import json
import subprocess
import sys

PERFIS = [
    ("Perfil 1 - casal de aposentados, conta de 180 kWh, sem Tarifa Social", [
        "5", "180", "0,92", "n", "s", "s",
        "1", "quanto gasta o chuveiro?", "s",
        "placa solar vale a pena?", "s",
        "0",
        "0", "4",
    ]),
    ("Perfil 2 - senhora de 70 anos que mora sozinha, recebe Tarifa Social", [
        "5", "75 kwh", "75", "", "s", "s", "s",      # digitou "75 kwh" e o programa recusou
        "1", "como pedir desconto na conta de luz", "s",
        "0",
        "0", "5",
    ]),
    ("Perfil 3 - família de 4 pessoas, 280 kWh, não sabe o valor do kWh", [
        "5", "280", "", "n", "s", "s",
        "1", "trocar geladeira velha economiza?", "s",
        "o que é bandeira vermelha?",                 # não encontra
        "0",
        "0", "4",
    ]),
    ("Perfil 4 - neto ajudando o avô, casa sem chuveiro elétrico (usa gás)", [
        "5", "120", "R$ 0,95", "0,95", "n", "n", "n",  # digitou "R$ 0,95" e foi recusado
        "1", "lampada led gasta menos?", "s",
        "0",
        "0", "3",
    ]),
]

with open("data/historico.json", "w", encoding="utf-8") as arquivo:
    json.dump({"atendimentos": [], "avaliacoes_facilidade": []}, arquivo, indent=2)

for descricao, teclas in PERFIS:
    print("=" * 70)
    print(descricao)
    saida = subprocess.run([sys.executable, "main.py"], input="\n".join(teclas) + "\n",
                           text=True, capture_output=True, encoding="utf-8")
    if saida.returncode != 0:
        print("ERRO:", saida.stderr)
        break
    # mostra só as linhas principais da simulação
    for linha in saida.stdout.splitlines():
        if (linha.startswith("Consumo considerado") or "se paga mais rápido" in linha
                or "faixa gratuita" in linha or linha.startswith("Entrada inválida")
                or linha.startswith("Não encontrei")):
            print("  ", linha.strip())

with open("data/historico.json", encoding="utf-8") as arquivo:
    dados = json.load(arquivo)
print("=" * 70)
print(f"Total: {len(dados['atendimentos'])} atendimentos, notas {dados['avaliacoes_facilidade']}")
