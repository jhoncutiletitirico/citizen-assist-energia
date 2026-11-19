"""
base_conhecimento.py - classe BaseConhecimento
Lê o JSON, cria os objetos Orientacao e faz a busca por pontuação.

Jhon Cutile Titirico - RM 571976
"""

import json

from orientacao import Orientacao

# campos que todo registro do JSON precisa ter (tupla: não muda)
CAMPOS = ("id", "categoria", "titulo", "palavras_chave", "resposta",
          "documentos", "onde", "fonte", "verificado_em")

ACENTOS = {"á": "a", "à": "a", "ã": "a", "â": "a", "é": "e", "ê": "e",
           "í": "i", "ó": "o", "õ": "o", "ô": "o", "ú": "u", "ç": "c"}

# pesos da pontuação
PONTOS_PALAVRA_CHAVE = 3   # palavra-chave da orientação que aparece na pergunta
PONTOS_TITULO = 1          # palavra da pergunta (4 letras ou mais) que aparece no título


def normalizar(texto):
    """Deixa o texto em minúsculas, sem acentos e sem pontuação.
    Coloca um espaço no começo e no fim para achar ' sus ' sem pegar 'suspenso'."""
    texto = texto.lower().strip()
    for letra, troca in ACENTOS.items():
        texto = texto.replace(letra, troca)
    for sinal in "?!.,;:()/-\"'":       # tirei também / - " ' além dos sinais do enunciado
        texto = texto.replace(sinal, " ")
    return " " + " ".join(texto.split()) + " "


def nivel_confianca(pontos):
    if pontos >= 6:
        return "ALTA"
    if pontos >= 3:
        return "MÉDIA"
    return ""          # menos de 3 pontos: não encontrou


def pegar_pontos(resultado):
    """Usada para ordenar a lista de tuplas (pontos, orientacao) pelos pontos."""
    return resultado[0]


class BaseConhecimento:

    def __init__(self, caminho):
        self.caminho = caminho
        self.orientacoes = []      # lista de objetos Orientacao

    def carregar(self):
        """Lê o JSON. Devolve True se deu certo e False se o arquivo não existe,
        está corrompido ou não tem nenhuma orientação válida."""
        try:
            with open(self.caminho, encoding="utf-8") as arquivo:
                registros = json.load(arquivo)
        except FileNotFoundError:
            print(f"Erro: o arquivo {self.caminho} não foi encontrado.")
            return False
        except json.JSONDecodeError:
            print(f"Erro: o arquivo {self.caminho} está corrompido (JSON inválido).")
            return False

        if not isinstance(registros, list):
            print("Erro: a base precisa ser uma lista de orientações.")
            return False

        self.orientacoes = []
        for registro in registros:
            if self.registro_completo(registro):
                self.orientacoes.append(Orientacao(registro))
            else:
                print("Aviso: um registro foi ignorado porque falta algum campo.")

        if len(self.orientacoes) == 0:
            print("Erro: nenhuma orientação válida na base.")
            return False
        return True

    def registro_completo(self, registro):
        if not isinstance(registro, dict):
            return False
        for campo in CAMPOS:
            if campo not in registro:
                return False
        return True

    def categorias(self):
        """Tupla com as categorias, sem repetir, em ordem alfabética."""
        lista = []
        for orientacao in self.orientacoes:
            if orientacao.categoria not in lista:
                lista.append(orientacao.categoria)
        lista.sort()
        return tuple(lista)

    def por_categoria(self, categoria):
        lista = []
        for orientacao in self.orientacoes:
            if orientacao.categoria == categoria:
                lista.append(orientacao)
        return lista

    def pontuar(self, pergunta, orientacao):
        """Dá pontos para UMA orientação. A pergunta já chega normalizada."""
        pontos = 0

        # +3 para cada palavra-chave que aparece na pergunta
        for chave in orientacao.palavras_chave:
            if normalizar(chave) in pergunta:
                pontos += PONTOS_PALAVRA_CHAVE

        # +1 para cada palavra da pergunta (4+ letras) que está no título
        palavras_titulo = normalizar(orientacao.titulo).split()
        palavras_ja_contadas = []
        for palavra in pergunta.split():
            if len(palavra) >= 4 and palavra in palavras_titulo and palavra not in palavras_ja_contadas:
                pontos += PONTOS_TITULO
                palavras_ja_contadas.append(palavra)

        return pontos

    def buscar(self, pergunta):
        """Devolve uma lista de tuplas (pontos, orientacao), da maior para a menor pontuação.
        Só entram as orientações que fizeram pelo menos 1 ponto."""
        pergunta = normalizar(pergunta)
        resultados = []
        for orientacao in self.orientacoes:
            pontos = self.pontuar(pergunta, orientacao)
            if pontos > 0:
                resultados.append((pontos, orientacao))
        # no empate fica a ordem do JSON (o sort do Python mantém a ordem dos iguais)
        resultados.sort(key=pegar_pontos, reverse=True)
        return resultados
