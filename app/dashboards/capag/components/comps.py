from datetime import datetime

from dash import html, dcc
import dash_bootstrap_components as dbc

from app.dashboards.capag import data
from app.dashboards.capag.graficos import linhas, bullet


# notas
def col_nota(data_format, nota):
    col = dbc.Col([
        html.H5(f"Nota em {data_format}: {nota}"),
    ],
        style={"background-color": "#EEEEEE",
               "border-radius": 25,
               "margin": 5,
               "text-align": "center"},
        lg=3
    )
    return col


def meta(bullet_comp, valores, texto):
    fig = dbc.Col([
        dcc.Graph(figure=bullet_comp,
                  config={"displaylogo": False})
    ])
    legenda = dbc.Col([
        html.P([
            f"{texto} (posição atual): " + "R${:,.2f}".format(valores[0])
        ], style={"color": "green"}),
        html.P([
            "Limite p/ nota A: " + "R${:,.2f}".format(valores[1])
        ], style={"color": "blue"}),
        html.P([
            "Diferença: " + "R${:,.2f}".format(valores[2])
        ]),
    ])
    return [fig, legenda]


# links
site_capag_link = "https://www.tesourotransparente.gov.br/temas/estados-e" \
                  "-municipios/capacidade-de-pagamento-capag "
tab_notas_geral_link = "https://drive.google.com/file/d/" \
                       "1pWf8QiIzbg0I9sKN7LQ-Cw_oW6ZvbAlg/view?usp=sharing"
tab_notas_parciais_link = "https://drive.google.com/file/d/" \
                          "1wwSq0jbdzwdtrGi85LJRkvK2KqVUeJWo/view?usp=sharing"

# datas
ano_ref = data.ano_ref()
data_ref = data.data_ref()
data_ref_format = data.data_ref_format()
data_fim_ano_format = data.data_fim_ano_format()
dt = datetime.strptime(data_ref, "%Y-%m")

# endividamento
df_end = data.tab_endividamento()
end = linhas.indicador(
    df_end,
    data_ref,
    "ind_end",
    "Endividamento",
    "Endividamento",
    "Previsto")
rcl_end = linhas.componentes(
    df_end,
    data_ref,
    "rcl_12m",
    "divida",
    "Dívida consol. x RC líquida",
    "RCL", "RCL prevista",
    "Dívida consol.",
    "Dívida contratual Prev."
)

nota_end_realiz, _ = data.pesquisa_nota(df_end, data_ref)
nota_end_projetada, _ = data.pesquisa_nota(df_end, data.data_fim_ano())

col_nota_end_realiz = col_nota(data_ref_format, nota_end_realiz)
col_nota_end_proj = col_nota(data_fim_ano_format, nota_end_projetada)

div_cons_atual = df_end.query(
    "data.dt.year == @dt.year and data.dt.month == @dt.month"). \
    divida.to_list()[0]

div_cons_limite_a = df_end.query(
    "data.dt.year == @ano_ref")["rcl"].sum() * 0.59999

div_end_dif = div_cons_limite_a - div_cons_atual

bullet_end = bullet.bullet("Div. Consol.", div_cons_atual, div_cons_limite_a)

meta_end = meta(bullet_end,
                [div_cons_atual, div_cons_limite_a, div_end_dif],
                "Dívida")

# poupança corrente

# liquidez
df_liq_serie = data.tab_liquidez()
df_liq = df_liq_serie[-1:]

liq_ind_graf, liq_comps_graf = linhas.liquidez(df_liq_serie)

card_liq = dbc.Card(
    dbc.CardBody(
        [
            html.H6("Indicador de liquidez"),
            html.P(
                "{:.1%}".format(df_liq["ind_liquidez"][0]),
            ),
            html.P(
                "Obg. Fincaneiras: R${:,.2f}".format(df_liq["obg_financeiras"][0]),
            ),
            html.P(
                "Disp. de Caixa: R${:,.2f}".format(df_liq["disp_caixa"][0]),
            )
        ]
    ),
    # style={"width": "18rem"},
)

card1 = dbc.Card(
    dbc.CardBody(
        [
            html.H6("Disponibilidade de Caixa Líquida dos Recursos Não "
                    "Vinculados (Deduzidas as Obrigações de Educação e "
                    "Saúde)"),
            html.P(
                "R${:,.2f}".format(df_liq["disp_cx_liq_nao_vinc_deduz_educ_saude"][0]),
            )
        ]
    ),
    style={"width": "18rem"},
)

card2 = dbc.Card(
    dbc.CardBody(
        [
            html.H6("Disponibilidade de Caixa Líquida dos Recursos Não "
                    "Vinculados (Cumprindo o Percentual de Educação e "
                    "Saúde)"),
            html.P(
                "R${:,.2f}".format(df_liq["disp_cx_liq_nao_vinc_cumprindo_educ_saude"][0]),
            )
        ]
    ),
    style={"width": "18rem"},
)

card3 = dbc.Card(
    dbc.CardBody(
        [
            html.H6("Restos a Pagar Empenhados e Não Liquidados do Exercício "
                    "dos Recursos Não Vinculados"),
            html.P(
                "R${:,.2f}".format(df_liq["restos_pagar_n_liq_exerc"][0]),
            )
        ]
    ),
    style={"width": "18rem"},
)

card4 = dbc.Card(
    dbc.CardBody(
        [
            html.H6("Restos a Pagar Empenhados e Não Liquidados do Exercício "
                    "dos Recursos Não Vinculados - Sem Grupo 1 de Despesa"),
            html.P(
                "R${:,.2f}".format(df_liq["restos_pagar_n_liq_exerc_sem_gd1"][0]),
            )
        ]
    ),
    style={"width": "18rem"},
)

# seletores
poup_corr_radio_ano = dbc.Col([
    dbc.Row(
        html.P("Ano:", style={"margin-bottom": 0})
    ),
    dbc.Row(
        dbc.Col([
            dcc.RadioItems(
                options=[
                    {'label': '2022', 'value': 2022},
                    {'label': '2021', 'value': 2021},
                    {'label': '2020', 'value': 2020}
                ],
                id='poup-corr-radio-ano',
                value=2022,
                labelStyle={'display': 'inline-block',
                            'margin-right': 50,
                            'margin-top': 0
                            }
            )
        ])
    )
])

poup_corr_radio_cenarios = dbc.Col([
        dbc.Row(
            html.P("Cenários previstos para desp. corrente:",
                   style={"margin-bottom": 0})
        ),
        dbc.Row(
            dbc.Col([
                dcc.RadioItems(
                    options=[
                        {'label': 'Var. Acumulada Ano', 'value': 0},
                        {'label': 'Var. Média Histórica', 'value': 1},
                        {'label': 'Var. Médias 3 anos (2019-2021)', 'value': 2}
                    ],
                    id='poup-corr-radio-cenarios',
                    value='Var. Acumulada Ano',
                    labelStyle={'display': 'inline-block',
                                'margin-right': 50,
                                'margin-top': 0
                                }
                )
            ])
        )
])

dc_rc_radio = dcc.RadioItems(
    options=[
        {'label': '2022', 'value': 2022},
        {'label': '2021', 'value': 2021},
        {'label': '2020', 'value': 2020}
    ],
    id='dc-rc-radio',
    value=2022,
    labelStyle={'display': 'inline-block',
                'margin-right': 50,
                'margin-top': 25}
)

# HTML
descricao = html.Div([
    html.H1([
        html.I(className="fa fa-tachometer", style={'fontSize': '80%'}),
        " Análise de Capacidade Pagamentos (CAPAG)"]),
    dbc.Row([
        dbc.Col([
            html.P("A análise da capacidade de pagamento apura a situação "
                   "fiscal dos Entes Subnacionais que querem contrair novos "
                   "empréstimos com garantia da União. O intuito da Capag é "
                   "apresentar de forma simples e transparente se um novo "
                   "endividamento representa risco de crédito para o Tesouro "
                   "Nacional. "
                   ),
            html.P("A metodologia do cálculo, dada pela Portaria MF nº "
                   "501/2017, é composta por três indicadores: "
                   "endividamento, poupança corrente e índice de liquidez. "
                   "Os conceitos e variáveis utilizadas e os procedimentos a "
                   "serem adotados na análise da Capag foram definidos na "
                   "Portaria STN nº 882/2018. "
                   ),
            html.I(
                html.A("Texto Extraído do Site do Capag",
                       href=site_capag_link,
                       target="_blank")
            )
        ], sm=12, lg=6, style={"margin-bottom": 35})
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Col([
                html.H3(id="nota-realizada")
            ], style={"background-color": "#EEEEEE",
                      "border-radius": 25,
                      "text-align": "center"}),
            dbc.Col([
                html.H3(id="nota-projetada")
            ], style={"background-color": "#EEEEEE",
                      "border-radius": 25,
                      "text-align": "center"}),
        ], sm=12, lg=6)
    ])
])

endividamento = dbc.Col([
    html.Hr(),
    html.Div([
        html.H2("Endividamento"),
        html.P("Razão entre a Dívida Consolidada e a Receita Corrente Líquida")
    ])
])
poupancas_correntes = html.Div([
    html.H2("Poupança Corrente"),
    html.P("O indicador de poupança corrente (PC) corresponde à relação "
           "entre despesas correntes empenhadas e receitas correntes "
           "ajustadas (RCA), ponderada pelo exercício e pelos dois "
           "exercícios imediatamente anteriores. A RCA são as receitas "
           "correntes, incluindo as intraorçamentárias, menos a receita "
           "utilizada na formação do Fundo de Manutenção e Desenvolvimento "
           "da Educação Básica e de Valorização dos Profissionais da "
           "Educação (FUNDEB)")
])
liquidez = html.Div([
    html.H2("Índice de Liquidez"),
    html.P("Razão entre o Obrigações Financeiras e a Disponibilidade de "
           "Caixa Bruta."),
    col_nota(df_liq.index[0].strftime("%b/%y"), df_liq.nota[0])
], style={"margin-bottom": 35})
despesas_correntes = html.Div([
    html.H2("Despesas Correntes x Receitas Correntes"),
    html.P("O indicador DC/RC é um dispositivo do Art. 167-A que estabelece "
           "uma série de medidas de ajuste fiscal e limita a possibilidade "
           "concessão de operações de crédito com a garantia da União. Nesse "
           "sentido, trata-se de um indicador auxiliar que deve apoiar o CAPAG")
])
