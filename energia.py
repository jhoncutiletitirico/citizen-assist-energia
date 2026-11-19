"""
energia.py - parte de Energias Renováveis e Sustentáveis (SERS) no Citizen Assist AI

Jhon Cutile Titirico - RM 571976 - Turma 1CCPI

Para a MESMA necessidade (a energia elétrica de uma casa, principalmente o
chuveiro) e o MESMO período (1 mês), compara 3 alternativas:
  A) Uso consciente + lâmpadas LED   (eficiência energética)
  B) Aquecedor solar de água         (renovável: solar térmica)
  C) Placas solares fotovoltaicas    (renovável: solar fotovoltaica)

- No assistente: menu 5 do main.py chama atendimento_energia().
- Rodando "python energia.py": gera a memória de cálculo na pasta calculos/.
"""

import csv
import json
import math
import os
import time

from assistente import ler_sim_nao

AVISO_ENERGIA = ("Aviso: valores ESTIMADOS para orientação. Economia, geração e custos reais "
                 "dependem do seu aparelho, clima, tarifa da distribuidora e orçamento local. "
                 "Este assistente NÃO é canal oficial.")


def formatar(valor, casas=2):
    """Número no padrão brasileiro (1.234,56). Infinito vira 'não se paga'."""
    if math.isinf(valor):
        return "não se paga"
    texto = f"{valor:,.{casas}f}"
    return texto.replace(",", "X").replace(".", ",").replace("X", ".")


def consumo_kwh(potencia_w, horas_por_dia, dias=30):
    """Energia (kWh) = potência (kW) x tempo (h)."""
    return potencia_w / 1000 * horas_por_dia * dias


class SimuladorEnergia:

    def __init__(self, caminho="data/premissas_energia.json"):
        self.caminho = caminho
        self.premissas = {}

    def carregar(self):
        """Lê as premissas (tarifa, potências, custos...). Devolve True ou False."""
        try:
            with open(self.caminho, encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"Erro: não foi possível ler {self.caminho}.")
            return False
        for chave, item in dados.items():
            if not chave.startswith("_"):      # "_descricao" é só um comentário
                self.premissas[chave] = item
        return True

    def valor(self, chave):
        return self.premissas[chave]["valor"]

    # ------------------------------------------------------------ consumo da casa
    def chuveiro_kwh(self):
        horas_por_dia = self.valor("banhos_por_dia") * self.valor("minutos_banho_atual") / 60
        return consumo_kwh(self.valor("chuveiro_inverno_w"), horas_por_dia)

    def lampadas_kwh(self, potencia_lampada_w):
        potencia_total = self.valor("lampadas_qtd") * potencia_lampada_w
        return consumo_kwh(potencia_total, self.valor("lampadas_horas_dia"))

    def perfil_referencia(self):
        """Consumo da casa de referência (2 moradores), em kWh por mês."""
        return {
            "Chuveiro elétrico": self.chuveiro_kwh(),
            "Iluminação (fluorescente)": self.lampadas_kwh(self.valor("lampada_fluorescente_w")),
            "Geladeira": self.valor("geladeira_kwh_mes"),
            "TV e outros": self.valor("tv_e_outros_kwh_mes"),
        }

    # ------------------------------------------------------------ conta de luz
    def conta(self, consumo, tarifa, tarifa_social):
        """Valor aproximado da conta, sem bandeira e sem iluminação pública.
        Com Tarifa Social: os primeiros 80 kWh são de graça.
        Sem Tarifa Social: paga no mínimo 30 kWh (custo de disponibilidade)."""
        consumo = max(0.0, consumo)
        if tarifa_social:
            kwh_cobrados = max(0.0, consumo - self.valor("tarifa_social_isencao_kwh"))
        else:
            kwh_cobrados = max(consumo, self.valor("custo_disponibilidade_kwh"))
        return kwh_cobrados * tarifa

    # ------------------------------------------------------------ alternativas
    def montar_alternativa(self, nome, tipo, economia_kwh, investimento, observacao,
                           consumo, tarifa, tarifa_social):
        """Calcula economia em R$, payback e CO2 evitado de uma alternativa."""
        economia_kwh = max(0.0, min(economia_kwh, consumo))   # não dá para economizar mais que o consumo
        conta_atual = self.conta(consumo, tarifa, tarifa_social)
        conta_nova = self.conta(consumo - economia_kwh, tarifa, tarifa_social)
        economia_reais = conta_atual - conta_nova

        if economia_reais > 0.01:
            payback = investimento / economia_reais        # em meses
        else:
            payback = math.inf                              # nunca se paga

        # fator em tCO2/MWh é igual a kgCO2/kWh
        co2_ano = economia_kwh * 12 * self.valor("fator_emissao_t_mwh")

        return {"alternativa": nome, "tipo": tipo, "economia_kwh_mes": economia_kwh,
                "conta_nova_r": conta_nova, "economia_r_mes": economia_reais,
                "investimento_r": investimento, "payback_meses": payback,
                "co2_evitado_kg_ano": co2_ano, "observacao": observacao}

    def comparar(self, consumo=None, tarifa=None, tarifa_social=False, tem_chuveiro=True):
        """Compara as 3 alternativas para a mesma casa no mesmo mês.
        Devolve (consumo, conta_atual, [alternativa A, B, C])."""
        perfil = self.perfil_referencia()
        if consumo is None:
            consumo = sum(perfil.values())
        if tarifa is None:
            tarifa = self.valor("tarifa_r_kwh")

        # quanto do consumo é chuveiro: vem da casa de referência, no máximo 60% do total
        if tem_chuveiro:
            chuveiro = min(perfil["Chuveiro elétrico"], 0.6 * consumo)
        else:
            chuveiro = 0.0

        conta_atual = self.conta(consumo, tarifa, tarifa_social)

        # A) banho de 10 para 7 minutos + trocar as lâmpadas por LED
        economia_banho = chuveiro * (1 - self.valor("minutos_banho_consciente")
                                     / self.valor("minutos_banho_atual"))
        economia_led = (self.lampadas_kwh(self.valor("lampada_fluorescente_w"))
                        - self.lampadas_kwh(self.valor("lampada_led_w")))
        custo_leds = self.valor("lampadas_qtd") * self.valor("preco_lampada_led_r")
        alternativa_a = self.montar_alternativa(
            "Uso consciente + LED", "Eficiência energética", economia_banho + economia_led,
            custo_leds, "Baixo custo e retorno imediato; depende da mudança de hábito.",
            consumo, tarifa, tarifa_social)

        # B) aquecedor solar faz 70% do trabalho do chuveiro
        if tem_chuveiro:
            obs_b = ("Precisa de telhado com sol e espaço para o reservatório; em dias nublados o "
                     "chuveiro elétrico complementa.")
        else:
            obs_b = "Sem chuveiro elétrico não há economia elétrica."
        alternativa_b = self.montar_alternativa(
            "Aquecedor solar de água", "Renovável (solar térmica)",
            chuveiro * self.valor("aquecedor_solar_fracao"), self.valor("aquecedor_solar_custo_r"),
            obs_b, consumo, tarifa, tarifa_social)

        # C) placas solares só para o consumo que é cobrado, em passos de 0,5 kWp
        #    (com Tarifa Social os 80 kWh já são grátis; sem ela sempre paga a taxa mínima)
        if tarifa_social:
            minimo = self.valor("tarifa_social_isencao_kwh")
        else:
            minimo = self.valor("custo_disponibilidade_kwh")
        consumo_a_cobrir = max(0.0, consumo - minimo)
        geracao_por_kwp = self.valor("fv_geracao_kwh_kwp_mes")
        kwp = math.ceil(consumo_a_cobrir / geracao_por_kwp / 0.5) * 0.5
        kwp = max(0.5, kwp)                                  # menor sistema: 0,5 kWp
        geracao = kwp * geracao_por_kwp
        compensado = min(geracao * self.valor("fv_fracao_compensada"), consumo)
        alternativa_c = self.montar_alternativa(
            f"Solar fotovoltaica ({kwp:.1f} kWp)", "Renovável (solar fotovoltaica)", compensado,
            kwp * 1000 * self.valor("fv_custo_r_wp"),
            "Exige telhado adequado, instalador habilitado e aprovação da distribuidora; "
            "a taxa mínima e a iluminação pública continuam.",
            consumo, tarifa, tarifa_social)

        return consumo, conta_atual, [alternativa_a, alternativa_b, alternativa_c]

    def recomendacoes(self, consumo, tarifa_social, alternativas):
        """Monta as recomendações em linguagem simples, de acordo com os números."""
        textos = ["1º passo, sempre: uso consciente (banho mais curto, chuveiro na posição verão "
                  "nos dias quentes e lâmpadas LED). É o que tem o menor custo."]

        if tarifa_social and consumo <= self.valor("tarifa_social_isencao_kwh"):
            textos.append("Seu consumo está dentro da faixa gratuita da Tarifa Social (80 kWh). "
                          "Investir em placas solares NÃO traz economia na conta.")

        # entre as duas renováveis (B e C), qual se paga mais rápido?
        melhor = None
        for alternativa in alternativas[1:]:
            if math.isfinite(alternativa["payback_meses"]):
                if melhor is None or alternativa["payback_meses"] < melhor["payback_meses"]:
                    melhor = alternativa
        if melhor is not None:
            anos = melhor["payback_meses"] / 12
            textos.append(f"Entre as renováveis, '{melhor['alternativa']}' se paga mais rápido "
                          f"(cerca de {anos:.1f} anos).")

        if tarifa_social:
            textos.append("Com Tarifa Social, a economia em dinheiro de qualquer alternativa é menor, "
                          "porque os primeiros 80 kWh já são gratuitos.")
        textos.append("Antes de comprar equipamentos, peça pelo menos 3 orçamentos e desconfie de "
                      "promessas de 'conta zero'.")
        return textos


# ---------------------------------------------------------------------------
# Atendimento do menu 5
# ---------------------------------------------------------------------------
def ler_numero(mensagem, minimo, maximo):
    """Lê um número (aceita vírgula). ENTER vazio devolve None (usa o valor padrão)."""
    while True:
        texto = input(mensagem).lower()
        # ajuste do teste: a pessoa copia da conta "75 kWh" ou "R$ 0,95", então tiro essas partes
        texto = texto.replace("kwh", "").replace("r$", "").strip().replace(",", ".")
        if texto == "":
            return None
        try:
            numero = float(texto)
        except ValueError:
            print("Entrada inválida: digite apenas o número (ex.: 150).")
            continue
        if numero < minimo or numero > maximo:
            print(f"Valor fora da faixa. Digite entre {minimo:g} e {maximo:g}.")
            continue
        return numero


def atendimento_energia(assistente, simulador):
    """Simulação com os números da conta de luz. Não pede nenhum dado pessoal."""
    inicio = time.time()
    print("\n== SIMULADOR DE ECONOMIA DE ENERGIA ==")
    print("Use os números da sua conta de luz. NÃO digite nome, CPF ou nº de instalação.")
    consumo = ler_numero("Consumo do mês em kWh (ENTER = casa de referência de 2 pessoas): ", 1, 2000)
    tarifa = ler_numero(f"Valor do kWh em R$ (ENTER = {simulador.valor('tarifa_r_kwh'):.2f}, "
                        "estimativa): ", 0.1, 5)
    social = ler_sim_nao("Sua família recebe a Tarifa Social / Luz do Povo? (s/n): ")
    chuveiro = ler_sim_nao("Vocês usam chuveiro elétrico? (s/n): ")

    consumo, conta_atual, alternativas = simulador.comparar(consumo, tarifa, social, chuveiro)

    print(f"\nConsumo considerado: {formatar(consumo, 1)} kWh/mês | "
          f"Conta estimada: R$ {formatar(conta_atual)}")
    print(f"{'Alternativa':<32}{'Economia/mês':>16}{'Investimento':>16}{'Se paga em':>14}")
    for a in alternativas:
        if math.isinf(a["payback_meses"]):
            payback = "não se paga"
        else:
            payback = f"{a['payback_meses']:.0f} meses"
        print(f"{a['alternativa']:<32}{'R$ ' + formatar(a['economia_r_mes']):>16}"
              f"{'R$ ' + formatar(a['investimento_r']):>16}{payback:>14}")

    print("\nObservações:")
    for a in alternativas:
        print(f"  - {a['alternativa']}: {a['observacao']}")
    print("\nRecomendações:")
    for texto in simulador.recomendacoes(consumo, social, alternativas):
        print(f"  * {texto}")
    print("\nFontes: ANEEL (tarifas), MME (Luz do Povo), Greener (custo solar), MCTI (emissões).")
    print("Detalhes em calculos/memoria_de_calculo.md")
    print(AVISO_ENERGIA)

    ajudou = ler_sim_nao("\nEssa simulação ajudou? (s/n): ")
    assistente.registrar("energia", "simulação de economia de energia", None, True, ajudou, 1,
                         round(time.time() - inicio, 1))


# ---------------------------------------------------------------------------
# Memória de cálculo (python energia.py)
# ---------------------------------------------------------------------------
def gerar_memoria_calculo():
    simulador = SimuladorEnergia()
    if not simulador.carregar():
        return
    os.makedirs("calculos", exist_ok=True)

    md = ["# Memória de cálculo – Energia no Citizen Assist AI", "",
          "Período de referência comum: **1 mês (30 dias)**. "
          "Payback simples = investimento ÷ economia mensal.", "",
          "## Premissas", "",
          "| Premissa | Valor | Unidade | Tipo | Origem |", "|---|---|---|---|---|"]
    for chave, p in simulador.premissas.items():
        md.append(f"| {chave} | {p['valor']} | {p['unidade']} | {p['tipo']} | {p['origem']} |")

    md += ["", "## Casa de referência (2 moradores)", "",
           "| Uso | kWh/mês | Cálculo |", "|---|---|---|"]
    como_calculei = {
        "Chuveiro elétrico": "5,5 kW × (2 banhos × 10 min ÷ 60) h/dia × 30 dias",
        "Iluminação (fluorescente)": "6 × 15 W = 0,09 kW × 5 h × 30 dias",
        "Geladeira": "etiqueta ENCE",
        "TV e outros": "0,1 kW × 5 h × 30 + 20",
    }
    perfil = simulador.perfil_referencia()
    for uso, kwh in perfil.items():
        md.append(f"| {uso} | {formatar(kwh, 1)} | {como_calculei[uso]} |")
    md.append(f"| **Total** | **{formatar(sum(perfil.values()), 1)}** | |")

    linhas_csv = []
    for social in (False, True):
        consumo, conta_atual, alternativas = simulador.comparar(tarifa_social=social)
        if social:
            cenario = "COM Tarifa Social (Luz do Povo)"
        else:
            cenario = "SEM Tarifa Social"
        md += ["", f"## Comparação – {cenario}", "",
               f"Consumo: {formatar(consumo, 1)} kWh/mês | "
               f"Conta atual estimada: R$ {formatar(conta_atual)}", "",
               "| Alternativa | Tipo | Economia (kWh/mês) | Economia (R$/mês) | Investimento (R$) | "
               "Payback (meses) | CO₂ evitado (kg/ano) |", "|---|---|---|---|---|---|---|"]
        for a in alternativas:
            md.append(f"| {a['alternativa']} | {a['tipo']} | {formatar(a['economia_kwh_mes'], 1)} | "
                      f"{formatar(a['economia_r_mes'])} | {formatar(a['investimento_r'])} | "
                      f"{formatar(a['payback_meses'], 1)} | {formatar(a['co2_evitado_kg_ano'], 1)} |")
            linha = {"cenario": cenario}
            for chave, valor in a.items():
                if isinstance(valor, float) and math.isfinite(valor):
                    valor = round(valor, 2)
                linha[chave] = valor
            linhas_csv.append(linha)
        md += ["", "Recomendações geradas:"]
        for texto in simulador.recomendacoes(consumo, social, alternativas):
            md.append(f"- {texto}")

    with open("calculos/comparacao_alternativas.csv", "w", newline="", encoding="utf-8-sig") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=list(linhas_csv[0].keys()), delimiter=";")
        escritor.writeheader()
        escritor.writerows(linhas_csv)
    with open("calculos/memoria_de_calculo.md", "w", encoding="utf-8") as arquivo:
        arquivo.write("\n".join(md) + "\n")

    print("\n".join(md))
    print("\nArquivos gerados em calculos/")


if __name__ == "__main__":
    gerar_memoria_calculo()
