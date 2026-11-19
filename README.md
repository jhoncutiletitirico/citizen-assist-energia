# Citizen Assist AI – Energia e Sustentabilidade (SERS)

Global Solution 2026.2 – CitizenTech | **Soluções em Energias Renováveis e Sustentáveis** | 1CC

> ⚠️ Protótipo acadêmico. **Não é canal oficial.** Os valores de economia, geração e custo são **estimativas**, não resultados garantidos.

## Integrantes
| Nome | RM |
|---|---|
| Jhon Cutile Titirico | 571976 |

## Público e necessidade energética
**Público:** pessoas idosas (60+) e famílias de baixa renda, muitas no Cadastro Único.
**Necessidade:** a conta de luz pesa no orçamento, e o **aquecimento de água do banho (chuveiro elétrico)** costuma ser o maior consumo da casa. Essas famílias recebem ofertas de "placa solar que zera a conta" sem saber se compensa, e muitas não sabem que já podem ter **gratuidade até 80 kWh** (Tarifa Social / Luz do Povo).
**Como o assistente ajuda:** responde dúvidas sobre energia e simula, com os números da própria conta de luz, quanto cada alternativa economiza, quanto custa e em quanto tempo se paga.

## Contribuição desta disciplina (o que é de SERS no projeto)
| Item | Arquivo |
|---|---|
| Módulo de cálculo e comparação de alternativas | [energia.py](energia.py) |
| Integração no menu do assistente (opção 5) | [main.py](main.py) |
| Premissas com origem, unidade e tipo (oficial/estimado) | [data/premissas_energia.json](data/premissas_energia.json) |
| 3 novas orientações de energia (ids 13, 14, 15) + Tarifa Social (id 9) | [data/base_conhecimento.json](data/base_conhecimento.json) |
| Memória de cálculo e comparação | [calculos/memoria_de_calculo.md](calculos/memoria_de_calculo.md), [calculos/comparacao_alternativas.csv](calculos/comparacao_alternativas.csv) |
| Testes | [testes/](testes/) |

Os arquivos `orientacao.py`, `base_conhecimento.py` e `assistente.py` são a base do assistente desenvolvida em Pensamento Computacional com Python.

## Como executar
Python 3.10+ (sem bibliotecas externas).
```bash
python main.py      # assistente completo; opção 5 = simulador de energia
python energia.py   # regenera a memória de cálculo em calculos/
```

## Análise de consumo – casa de referência (2 moradores, 1 mês)
| Uso | kWh/mês | Cálculo (E = P × t) |
|---|---|---|
| Chuveiro elétrico | 55,0 | 5,5 kW × (2 banhos × 10 min) × 30 dias |
| Iluminação (fluorescente) | 13,5 | 6 × 15 W × 5 h × 30 dias |
| Geladeira | 30,0 | etiqueta ENCE (estimado) |
| TV e outros | 35,0 | estimado |
| **Total** | **133,5** | |

O chuveiro representa **41%** do consumo, por isso é o foco das alternativas.

## Comparação das alternativas (mesma casa, mesmo mês)
Tarifa estimada: R$ 1,10/kWh com impostos.

**Sem Tarifa Social** (conta estimada R$ 146,85)
| Alternativa | Tipo | Economia/mês | Investimento | Payback | CO₂ evitado/ano |
|---|---|---|---|---|---|
| Uso consciente + LED | Eficiência | R$ 24,09 (21,9 kWh) | R$ 72 | 3 meses | 10 kg |
| Aquecedor solar de água | Renovável – solar térmica | R$ 42,35 (38,5 kWh) | R$ 3.000 | 71 meses | 18 kg |
| Solar fotovoltaica 1,0 kWp | Renovável – fotovoltaica | R$ 107,53 (97,8 kWh) | R$ 2.930 | 27 meses | 45 kg |

**Com Tarifa Social** (conta estimada R$ 58,85 – os primeiros 80 kWh são gratuitos)
| Alternativa | Economia/mês | Investimento | Payback |
|---|---|---|---|
| Uso consciente + LED | R$ 24,09 | R$ 72 | 3 meses |
| Aquecedor solar de água | R$ 42,35 | R$ 3.000 | 71 meses |
| Solar fotovoltaica 0,5 kWp | R$ 53,76 | R$ 1.465 | 27 meses |

Memória completa: [calculos/memoria_de_calculo.md](calculos/memoria_de_calculo.md).

## Justificativa das recomendações
- **Custo:** o uso consciente + LED se paga em ~3 meses e deve ser sempre o 1º passo. Entre as renováveis, a fotovoltaica tem o menor payback, mas exige maior investimento inicial; o aquecedor solar é mais simples de instalar.
- **Viabilidade:** as duas renováveis exigem telhado com sol. A fotovoltaica exige instalador habilitado e aprovação da distribuidora; para baixa renda, o investimento inicial é a maior barreira. Quem mora de aluguel ou em apartamento normalmente não consegue instalar.
- **Impacto ambiental:** a matriz elétrica brasileira é muito renovável (fator 0,0385 tCO₂/MWh em 2023), então o CO₂ evitado por uma casa é pequeno (cerca de 10 a 45 kg/ano). O principal ganho é **econômico e social**; também conta o descarte correto de lâmpadas fluorescentes (contêm mercúrio) e de placas no fim da vida útil.
- **Tarifa Social muda a recomendação:** quem já tem gratuidade até 80 kWh economiza menos em reais com qualquer alternativa; se o consumo já está abaixo de 80 kWh, placas solares **não** reduzem a conta.

## Referências
| Dado | Fonte |
|---|---|
| Tarifa residencial (R$ 851/MWh sem tributos, ICMS 17,3%, PIS/Cofins 5,2%) | ANEEL – boletim InfoTarifa, jun/2026 |
| Gratuidade até 80 kWh (Luz do Povo) | MME – https://www.gov.br/mme/pt-br/a-revolucao-brasileira-em-energia-e-mineracao/combate-a-pobreza-energetica-e-inclusao-social/luz-do-povo |
| Custo de sistema FV residencial (4 kWp ≈ R$ 11,7 mil) | Greener – estudos de mercado de GD |
| Fator de emissão do SIN 2023 (38,5 kgCO₂/MWh) | MCTI – SIRENE |
| Compensação de energia / Fio B | Lei 14.300/2022 |
| Custo de disponibilidade (30 kWh monofásico) | ANEEL – REN 1.000/2021 |
| Etiquetagem de aparelhos | Inmetro – Programa Brasileiro de Etiquetagem |
| Irradiação solar | INPE – Atlas Brasileiro de Energia Solar |

Todos os valores marcados como **estimado** em `premissas_energia.json` são premissas do grupo, com justificativa.

## Testes com usuários
> **Atenção: este teste foi SIMULADO.** Não consegui testar com pessoas de fora no prazo. Simulei 4 perfis com números típicos de conta de luz. Cada perfil é uma sequência de teclas digitada automaticamente no `main.py` de verdade, pelo script `testes/teste_simulado.py`. As respostas "ajudou" e as notas também fazem parte da simulação.

| # | Perfil simulado | O que o programa mostrou | Ajudou? | Observação |
|---|---|---|---|---|
| 1 | Casal de aposentados, 180 kWh, R$ 0,92/kWh, sem Tarifa Social | Conta de R$ 165,60; a solar de 1,5 kWp se paga mais rápido (cerca de 2,7 anos) | sim | Também perguntou sobre o chuveiro e a placa solar; as duas foram encontradas |
| 2 | Senhora de 70 anos, 75 kWh, com Tarifa Social | Conta de R$ 0,00; aviso de que a placa solar **não** traz economia | sim | Digitou "75 kwh" do jeito que está na conta e o programa recusou → **ajuste feito** |
| 3 | Família de 4 pessoas, 280 kWh, sem saber o valor do kWh (ENTER) | Conta de R$ 308,00; a solar de 2,5 kWp se paga em cerca de 2,3 anos | sim | "o que é bandeira vermelha?" não foi encontrada (fica como dúvida sem solução) |
| 4 | Neto e avô, 120 kWh, casa sem chuveiro elétrico | Conta de R$ 114,00; a solar de 1,0 kWp se paga em cerca de 2,9 anos | não | Digitou "R$ 0,95" e foi recusado. Como a casa usa gás, a parte do chuveiro não ajudou |

**Indicadores (menu 3):** 10 atendimentos · 90,0% de resposta encontrada · 80,0% de acerto · facilidade 4,00 (simulada) · tempo 0,0 s (as teclas foram digitadas pelo script).

**Ajuste feito a partir do teste:** a função `ler_numero()` do `energia.py` agora aceita o número do jeito que vem na conta, como "75 kWh" ou "R$ 0,95". Ela tira o "kWh" e o "R$" antes de converter. Antes, essas entradas davam "Entrada inválida".

Teste automatizado de funcionamento: [testes/roteiro_teste_energia.txt](testes/roteiro_teste_energia.txt) → [testes/saida_teste_energia.txt](testes/saida_teste_energia.txt).

## Limitações
- Valores médios nacionais; a tarifa real varia por distribuidora e bandeira.
- Payback simples (sem juros, inflação, manutenção ou reajuste de tarifa).
- O custo por Wp de sistemas pequenos (0,5–1,5 kWp) tende a ser maior que o de 4 kWp usado como referência.
- A parcela do chuveiro no consumo informado pelo usuário vem da casa de referência (limitada a 60%).

## Vídeo técnico
<link do YouTube não listado, até 3 minutos>
