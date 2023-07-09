from dash import html, dcc
from app.dashboards.stn.dataset import df

contas = {
    "RECEITAS CORRENTES (I)": "RECEITAS CORRENTES (I)",
    "Impostos, Taxas e Contribuições de Melhoria":
        "--- Impostos, Taxas e Contribuições de Melhoria",
    "IPTU": "--- IPTU",
    "ISS": "--- ISS",
    "ITBI": "--- ITBI",
    "IRRF": "--- IRRF",
    "Outros Impostos, Taxas e Contribuições de Melhoria":
        "--- Outros Impostos, Taxas e Contribuições de Melhoria",
    "Contribuições": "--- Contribuições",
    "Receita Patrimonial": "--- Receita Patrimonial",
    "Rendimentos de Aplicação Financeira":
        "--- Rendimentos de Aplicação Financeira",
    "Outras Receitas Patrimoniais": "--- Outras Receitas Patrimoniais",
    "Receita de Serviços": "--- Receita de Serviços",
    "Transferências Correntes": "--- Transferências Correntes",
    "Cota-Parte do FPM": "--- Cota-Parte do FPM",
    "Cota-Parte do ICMS": "--- Cota-Parte do ICMS",
    "Cota-Parte do IPVA": "--- Cota-Parte do IPVA",
    "Cota-Parte do ITR": "--- Cota-Parte do ITR",
    "Transferências do FUNDEB": "--- Transferências do FUNDEB",
    "Outras Transferências Correntes": "--- Outras Transferências Correntes",
    "Outras Receitas Correntes": "--- Outras Receitas Correntes",
    "DEDUÇÕES (II)": "DEDUÇÕES (II)",
    "Contrib. do Servidor para o Plano de Previdência":
        "--- Contrib. do Servidor para o Plano de Previdência",
    "Compensações Financ. entre Regimes Previdência":
        "--- Compensações Financ. entre Regimes Previdência",
    "Rendimentos de Aplicações de Recursos Previdenciários":
        "--- Rendimentos de Aplicações de Recursos Previdenciários",
    "Dedução de Receita para Formação do FUNDEB":
        "--- Dedução de Receita para Formação do FUNDEB",
    "RECEITA CORRENTE LÍQUIDA (III) = (I - II)":
        "RECEITA CORRENTE LÍQUIDA (III) = (I - II)",
    "(-) Transferências obrigatórias da União relativas às emendas individuais (art. 166-A, § 1º, da CF)  (IV)":
        "(-) Transf obrig da União às emendas individuais (IV)",
    "RECEITA CORRENTE LÍQUIDA AJUSTADA PARA CÁLCULO DOS LIMITES DE ENDIVIDAMENTO (V) = (III - IV)":
        "RCL AJUST PARA LIMITES DE ENDIVIDAMENTO (V) = (III - IV)",
    "(-) Transferências obrigatórias da União relativas às emendas de bancada  (art. 166, § 16, da CF)  (VI)":
        "(-) Transf obrig da União às emendas de bancada (VI)",
    "RECEITA CORRENTE LÍQUIDA AJUSTADA PARA CÁLCULO DOS LIMITES DA DESPESA COM PESSOAL (VII) = (V - VI)":
        "RCL AJUST PARA LIMITES DA DESP C/ PESSOAL (VII) = (V - VI)",
}

contas_dropdown = html.Div(
    dcc.Dropdown(
        options=[{'label': v, 'value': k} for k, v in contas.items()],
        value="RECEITAS CORRENTES (I)",
        id="conta-dropdown",
        clearable=False
    )
)

regioes_dropdown = html.Div(
    dcc.Dropdown(
        options=df.regiao.unique(),
        # value="Nordeste",
        id="regioes-dropdown",
        clearable=True
    )
)

agregacao_radio = dcc.RadioItems(
    [
        {"label": "Ano", "value": "ano"},
        {"label": "Ano/Bimestre", "value": "ano_bimestre"},
        {"label": 'Mês/Ano', "value": "mes_ano"}
    ],
    'ano',
    labelStyle={
        'display': 'inline-block',
        'width': 150,
        'marginBottom': 15
    },
    id="agregacao-radio"
)

ano_max = df.ano.max()
ano_min = df.ano.min()

ano_slider = html.Div(
    dcc.RangeSlider(
        ano_min,
        ano_max,
        1,
        value=[ano_max - 1, ano_max],
        marks={i: str(i) for i in range(ano_min, ano_max + 1)},
        id='ano-slider'
    )
)

bi_max = df.query("ano == @ano_max").bimestre.max()

bimestre_slider = html.Div(
    dcc.RangeSlider(1, 6, 1, value=[1, bi_max], id='bimestre-slider')
)

mes_num_max = df.query("ano == @ano_max").mes_num.max()
meses = ["jan", "fev", "mar", "abr", "mai", "jun",
         "jul", "ago", "set", "out", "nov", "dez"]

mes_slider = dcc.RangeSlider(
    min=1,
    max=12,
    step=1,
    marks={i: m for i, m in zip(list(range(1, 13)), meses)},
    value=[1, mes_num_max],
    id="mes-slider"
)

formatos_check = dcc.Checklist(
    options={
        'per_capita': 'Per Capita',
        'deflacionado': 'Deflacionado'
    },
    # inline=True,
    labelStyle={
        'display': 'inline-block',
        'width': 135
    },
    id="formato-check"
)

formato_radio = dcc.RadioItems(
    [
        {"label": "Nominal", "value": "valor"},
        {"label": "Deflacionado", "value": "valor_deflac"},
        {"label": "Per Capita", "value": "per_capita"}
    ],
    "valor",
    inline=True,
    inputStyle={"marginLeft": 10},
    id="formato-radio"
)
