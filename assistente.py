"""
assistente.py - classe Assistente
Faz o atendimento (pergunta ou categoria), guarda o histórico,
calcula os indicadores e exporta o CSV.

Jhon Cutile Titirico - RM 571976
"""

import csv
import json
import time
from datetime import datetime

from base_conhecimento import nivel_confianca

COLUNAS_CSV = ["data", "origem", "pergunta", "id_orientacao", "encontrou",
               "ajudou", "tentativas", "tempo_segundos"]


# ---------------------------------------------------------------------------
# Funções de leitura: nenhuma delas deixa o programa fechar com entrada errada
# ---------------------------------------------------------------------------
def ler_opcao(mensagem, minimo, maximo):
    """Pede um número entre minimo e maximo até a pessoa digitar certo."""
    while True:
        texto = input(mensagem).strip()
        if texto == "":
            print("Você não digitou nada. Digite um número.")
        elif not texto.isdigit():
            print("Entrada inválida: digite só números.")
        elif int(texto) < minimo or int(texto) > maximo:
            print(f"Opção fora da faixa. Escolha de {minimo} a {maximo}.")
        else:
            return int(texto)


def ler_sim_nao(mensagem):
    """Aceita s ou n (também sim/não). Repete até ser válido."""
    while True:
        texto = input(mensagem).strip().lower()
        if texto in ("s", "sim"):
            return True
        if texto in ("n", "nao", "não"):
            return False
        print("Resposta inválida. Digite s ou n.")


def tem_dado_pessoal(texto):
    """Pergunta com 8 ou mais números (CPF, telefone, RG) ou com @ (e-mail)."""
    quantidade_digitos = 0
    for caractere in texto:
        if caractere.isdigit():
            quantidade_digitos += 1
    return quantidade_digitos >= 8 or "@" in texto


# ---------------------------------------------------------------------------
class Assistente:

    def __init__(self, nome, base):
        self.nome = nome
        self.base = base                 # objeto BaseConhecimento (composição)
        self.historico = []              # lista de dicionários, um por atendimento
        self.notas = []                  # notas de facilidade (1 a 5)
        self.arquivo_historico = "data/historico.json"
        self.arquivo_csv = "data/atendimentos.csv"
        self.carregar_historico()

    # ------------------------------------------------------------ arquivos
    def carregar_historico(self):
        """Lê o histórico salvo. Se não existir ou estiver com erro, começa vazio."""
        try:
            with open(self.arquivo_historico, encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
            self.historico = dados["atendimentos"]
            self.notas = dados["avaliacoes_facilidade"]
        except FileNotFoundError:
            pass    # primeira vez: ainda não tem histórico
        except (json.JSONDecodeError, KeyError, TypeError):
            print("Aviso: o histórico estava com erro. Um novo histórico será iniciado.")

    def salvar_historico(self):
        dados = {"atendimentos": self.historico, "avaliacoes_facilidade": self.notas}
        with open(self.arquivo_historico, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=2)

    # ------------------------------------------------------------ atendimento
    def perguntar(self):
        """Atendimento por texto livre."""
        inicio = time.time()
        tentativas = 0
        ultima_pergunta = ""

        while True:
            pergunta = input("\nDigite sua dúvida (0 para voltar): ").strip()

            if pergunta == "0":
                # se tentou e não achou nada, entra como dúvida sem solução
                if tentativas > 0:
                    self.registrar("pergunta", ultima_pergunta, None, False, False,
                                   tentativas, round(time.time() - inicio, 1))
                return

            if pergunta == "":
                print("Pergunta vazia. Escreva sua dúvida com suas palavras.")
                continue

            if tem_dado_pessoal(pergunta):
                print("Atenção: não digite CPF, telefone ou e-mail. Reescreva.")
                continue    # essa pergunta NÃO é registrada

            tentativas += 1
            ultima_pergunta = pergunta
            resultados = self.base.buscar(pergunta)

            if len(resultados) == 0 or nivel_confianca(resultados[0][0]) == "":
                print("\nNão encontrei uma orientação para essa dúvida.")
                print("Tente outras palavras ou procure numa categoria:")
                print(", ".join(self.base.categorias()))
                continue

            pontos, melhor = resultados[0]
            print(f"\nConfiança da resposta: {nivel_confianca(pontos)} ({pontos} pontos)")
            melhor.exibir()

            # até 2 alternativas que também tenham 3 pontos ou mais
            alternativas = []
            for pontos_alt, orientacao_alt in resultados[1:3]:
                if pontos_alt >= 3:
                    alternativas.append((pontos_alt, orientacao_alt))
            if alternativas:
                print("\nTalvez também ajude:")
                for pontos_alt, orientacao_alt in alternativas:
                    print(f"  - {orientacao_alt.titulo} ({pontos_alt} pontos)")

            ajudou = ler_sim_nao("\nEssa orientação respondeu sua dúvida? (s/n): ")
            self.registrar("pergunta", pergunta, melhor.id, True, ajudou,
                           tentativas, round(time.time() - inicio, 1))

            # começa um novo atendimento
            inicio = time.time()
            tentativas = 0
            ultima_pergunta = ""

    def navegar(self):
        """Atendimento por categorias numeradas. O 0 sempre volta."""
        inicio = time.time()
        categorias = self.base.categorias()

        while True:
            print("\n== CATEGORIAS ==")
            for numero, categoria in enumerate(categorias, start=1):
                print(f" {numero} - {categoria}")
            print(" 0 - Voltar")
            escolha = ler_opcao("Escolha a categoria: ", 0, len(categorias))
            if escolha == 0:
                return

            categoria = categorias[escolha - 1]
            orientacoes = self.base.por_categoria(categoria)

            while True:
                print(f"\n== {categoria.upper()} ==")
                for numero, orientacao in enumerate(orientacoes, start=1):
                    print(f" {numero} - {orientacao.titulo}")
                print(" 0 - Voltar")
                item = ler_opcao("Escolha a orientação: ", 0, len(orientacoes))
                if item == 0:
                    break

                orientacao = orientacoes[item - 1]
                orientacao.exibir()
                ajudou = ler_sim_nao("\nEssa orientação respondeu sua dúvida? (s/n): ")
                self.registrar("categoria", f"[{categoria}] {orientacao.titulo}", orientacao.id,
                               True, ajudou, 1, round(time.time() - inicio, 1))
                inicio = time.time()

    def registrar(self, origem, pergunta, id_orientacao, encontrou, ajudou, tentativas, tempo):
        """Guarda um atendimento e já salva no historico.json."""
        atendimento = {
            "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "origem": origem,
            "pergunta": pergunta,
            "id_orientacao": id_orientacao,
            "encontrou": encontrou,
            "ajudou": ajudou,
            "tentativas": tentativas,
            "tempo_segundos": tempo,
        }
        self.historico.append(atendimento)
        self.salvar_historico()

    def pedir_nota(self):
        """Ao sair, pede uma nota de facilidade de 1 a 5 (0 pula)."""
        nota = ler_opcao("\nDe 1 a 5, quão fácil foi usar o assistente? (0 para pular): ", 0, 5)
        if nota > 0:
            self.notas.append(nota)
            self.salvar_historico()
            print("Obrigado pela nota!")

    # ------------------------------------------------------------ indicadores
    def indicadores(self):
        total = len(self.historico)
        if total == 0:
            print("\nAinda não há atendimentos registrados.")
            return

        encontrados = 0
        ajudaram = 0
        soma_tempo = 0
        soma_tentativas = 0
        sem_solucao = []
        for atendimento in self.historico:
            soma_tentativas += atendimento["tentativas"]
            if atendimento["encontrou"]:
                encontrados += 1
                soma_tempo += atendimento["tempo_segundos"]
            if atendimento["ajudou"]:
                ajudaram += 1
            else:
                sem_solucao.append(atendimento["pergunta"])

        print("\n== INDICADORES ==")
        print(f"Atendimentos registrados ....: {total}")
        print(f"Resposta encontrada .........: {100 * encontrados / total:.1f}%")
        print(f"Taxa de acerto (ajudou) .....: {100 * ajudaram / total:.1f}%")
        if encontrados > 0:
            print(f"Tempo médio para encontrar ..: {soma_tempo / encontrados:.1f} s")
        print(f"Tentativas por atendimento ..: {soma_tentativas / total:.2f}")
        if self.notas:
            print(f"Facilidade de uso (1 a 5) ...: {sum(self.notas) / len(self.notas):.2f}"
                  f" ({len(self.notas)} notas)")
        else:
            print("Facilidade de uso (1 a 5) ...: ainda sem notas")
        print("Dúvidas sem solução:")
        if sem_solucao:
            for duvida in sem_solucao:
                print(f"  - {duvida}")
        else:
            print("  (nenhuma)")

    def exportar_csv(self):
        """Salva o histórico em data/atendimentos.csv (csv.DictWriter, como na Aula 09)."""
        if len(self.historico) == 0:
            print("\nNada para exportar: nenhum atendimento registrado.")
            return
        with open(self.arquivo_csv, "w", newline="", encoding="utf-8-sig") as arquivo:
            escritor = csv.DictWriter(arquivo, fieldnames=COLUNAS_CSV)
            escritor.writeheader()
            escritor.writerows(self.historico)
        print(f"\n{len(self.historico)} atendimento(s) exportado(s) para {self.arquivo_csv}")
