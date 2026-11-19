# Memória de cálculo – Energia no Citizen Assist AI

Período de referência comum: **1 mês (30 dias)**. Payback simples = investimento ÷ economia mensal.

## Premissas

| Premissa | Valor | Unidade | Tipo | Origem |
|---|---|---|---|---|
| tarifa_r_kwh | 1.1 | R$/kWh (com ICMS e PIS/Cofins) | estimado | ANEEL InfoTarifa jun/2026: tarifa residencial B1 média de R$ 851/MWh sem tributos; ICMS médio 17,3% e PIS/Cofins 5,2% calculados 'por dentro': 0,851 / (1 - 0,225) = 1,098 R$/kWh. Bandeiras e iluminação pública não incluídas. |
| chuveiro_inverno_w | 5500 | W | estimado | Potência típica de chuveiro elétrico residencial na posição inverno; a potência real está na etiqueta do aparelho. |
| banhos_por_dia | 2 | banhos/dia | estimado | Casa de referência: 2 moradores, 1 banho cada. |
| minutos_banho_atual | 10 | min | estimado | Premissa da casa de referência. |
| minutos_banho_consciente | 7 | min | estimado | Meta de redução de 3 minutos por banho. |
| lampadas_qtd | 6 | lâmpadas | estimado | Casa de referência. |
| lampadas_horas_dia | 5 | h/dia | estimado | Uso noturno típico. |
| lampada_fluorescente_w | 15 | W | estimado | Fluorescente compacta com fluxo luminoso equivalente a uma LED de 9 W (~800 lm). |
| lampada_led_w | 9 | W | estimado | LED de ~800 lm (equivalente). |
| preco_lampada_led_r | 12.0 | R$/unidade | estimado | Preço de varejo de referência (conferir no comércio local). |
| geladeira_kwh_mes | 30 | kWh/mês | estimado | Faixa de consumo de refrigerador de 1 porta na Etiqueta Nacional de Conservação de Energia (ENCE). |
| tv_e_outros_kwh_mes | 35 | kWh/mês | estimado | TV (100 W x 5 h x 30 dias = 15 kWh) + outros aparelhos (20 kWh). |
| aquecedor_solar_custo_r | 3000 | R$ instalado | estimado | Aquecedor solar de água para 2 pessoas (reservatório ~200 L), faixa de mercado; pedir orçamento local. |
| aquecedor_solar_fracao | 0.7 | fração da energia do banho suprida pelo sol | estimado | Fração solar usual de projeto (60% a 80%), varia com clima e dimensionamento. |
| fv_custo_r_wp | 2.93 | R$/Wp | oficial | Greener: sistema residencial de 4 kWp custa em média R$ 11,7 mil (dados 2024) = R$ 2,93/Wp. Sistemas menores tendem a custar mais por Wp. |
| fv_geracao_kwh_kwp_mes | 115 | kWh/kWp/mês | estimado | Irradiação média ~4,8 kWh/m²/dia x 30 dias x rendimento global 0,80. |
| fv_fracao_compensada | 0.85 | fração | estimado | Perda de parte do crédito pela cobrança gradual do 'Fio B' para sistemas novos (Lei 14.300/2022). |
| custo_disponibilidade_kwh | 30 | kWh/mês (monofásico) | oficial | Consumo mínimo faturado de unidade monofásica (REN ANEEL 1.000/2021). |
| tarifa_social_isencao_kwh | 80 | kWh/mês | oficial | Luz do Povo: gratuidade até 80 kWh/mês para famílias do CadÚnico com renda de até 1/2 salário mínimo por pessoa e beneficiários do BPC (vigente desde 05/07/2025). |
| fator_emissao_t_mwh | 0.0385 | tCO2/MWh | oficial | Fator médio anual de emissão do SIN em 2023 (MCTI). |

## Casa de referência (2 moradores)

| Uso | kWh/mês | Cálculo |
|---|---|---|
| Chuveiro elétrico | 55,0 | 5,5 kW × (2 banhos × 10 min ÷ 60) h/dia × 30 dias |
| Iluminação (fluorescente) | 13,5 | 6 × 15 W = 0,09 kW × 5 h × 30 dias |
| Geladeira | 30,0 | etiqueta ENCE |
| TV e outros | 35,0 | 0,1 kW × 5 h × 30 + 20 |
| **Total** | **133,5** | |

## Comparação – SEM Tarifa Social

Consumo: 133,5 kWh/mês | Conta atual estimada: R$ 146,85

| Alternativa | Tipo | Economia (kWh/mês) | Economia (R$/mês) | Investimento (R$) | Payback (meses) | CO₂ evitado (kg/ano) |
|---|---|---|---|---|---|---|
| Uso consciente + LED | Eficiência energética | 21,9 | 24,09 | 72,00 | 3,0 | 10,1 |
| Aquecedor solar de água | Renovável (solar térmica) | 38,5 | 42,35 | 3.000,00 | 70,8 | 17,8 |
| Solar fotovoltaica (1.0 kWp) | Renovável (solar fotovoltaica) | 97,8 | 107,53 | 2.930,00 | 27,2 | 45,2 |

Recomendações geradas:
- 1º passo, sempre: uso consciente (banho mais curto, chuveiro na posição verão nos dias quentes e lâmpadas LED). É o que tem o menor custo.
- Entre as renováveis, 'Solar fotovoltaica (1.0 kWp)' se paga mais rápido (cerca de 2.3 anos).
- Antes de comprar equipamentos, peça pelo menos 3 orçamentos e desconfie de promessas de 'conta zero'.

## Comparação – COM Tarifa Social (Luz do Povo)

Consumo: 133,5 kWh/mês | Conta atual estimada: R$ 58,85

| Alternativa | Tipo | Economia (kWh/mês) | Economia (R$/mês) | Investimento (R$) | Payback (meses) | CO₂ evitado (kg/ano) |
|---|---|---|---|---|---|---|
| Uso consciente + LED | Eficiência energética | 21,9 | 24,09 | 72,00 | 3,0 | 10,1 |
| Aquecedor solar de água | Renovável (solar térmica) | 38,5 | 42,35 | 3.000,00 | 70,8 | 17,8 |
| Solar fotovoltaica (0.5 kWp) | Renovável (solar fotovoltaica) | 48,9 | 53,76 | 1.465,00 | 27,2 | 22,6 |

Recomendações geradas:
- 1º passo, sempre: uso consciente (banho mais curto, chuveiro na posição verão nos dias quentes e lâmpadas LED). É o que tem o menor custo.
- Entre as renováveis, 'Solar fotovoltaica (0.5 kWp)' se paga mais rápido (cerca de 2.3 anos).
- Com Tarifa Social, a economia em dinheiro de qualquer alternativa é menor, porque os primeiros 80 kWh já são gratuitos.
- Antes de comprar equipamentos, peça pelo menos 3 orçamentos e desconfie de promessas de 'conta zero'.
