"""
orientacao.py - classe Orientacao
Cada objeto Orientacao guarda UMA orientação da base (um registro do JSON).

Jhon Cutile Titirico - RM 571976
"""

AVISO = "Aviso: este assistente NÃO é um canal oficial. Confirme na fonte indicada."


class Orientacao:

    def __init__(self, dados):
        # "dados" é o dicionário de um registro do JSON
        self.id = dados["id"]
        self.categoria = dados["categoria"]
        self.titulo = dados["titulo"]
        self.palavras_chave = dados["palavras_chave"]
        self.resposta = dados["resposta"]
        self.documentos = dados["documentos"]
        self.onde = dados["onde"]
        self.fonte = dados["fonte"]
        self.verificado_em = dados["verificado_em"]

    def exibir(self):
        """Mostra a orientação na tela, sempre com a fonte, a data e o aviso."""
        print(f"\n>> {self.titulo} [{self.categoria}]")
        print(self.resposta)
        print("Documentos necessários:")
        for documento in self.documentos:
            print(f"  - {documento}")
        print(f"Onde: {self.onde}")
        print(f"Fonte: {self.fonte} (verificado em {self.verificado_em})")
        print(AVISO)
