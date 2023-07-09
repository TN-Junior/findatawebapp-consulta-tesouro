from dash import html, dcc
import dash_bootstrap_components as dbc

from app.dashboards.utils import components
from app.dashboards.caf import comps

margins_style = {"marginTop": "50px", "marginBottom": "50px"}

layout = html.Div([
    # navbar
    components.navbar,
    dbc.Container([
        # intro
        html.Div(comps.intro, style={
            "marginTop": "15px",
            "marginBottom": "50px"}
                 ),
        # filtros
        html.Div([
            dbc.Row([
                dbc.Col(comps.drop_razao_social, sm=12, md=4, lg=4),
                dbc.Col(comps.drop_razao_social_processo, sm=12, md=4, lg=3),
                dbc.Col(comps.drop_instancia, sm=12, md=3, lg=2),
                dbc.Col(comps.drop_mudanca_status, sm=12, md=3, lg=3)
            ]),
            dbc.Row([
                dbc.Col(comps.drop_situacao_debito, sm=12, md=4, lg=4),
                dbc.Col(comps.drop_situacao_atual, sm=12, md=6, lg=4),
                dbc.Col(comps.drop_fora_caf, sm=12, md=2, lg=2),
                dbc.Col(comps.drop_finalizado, sm=12, md=2, lg=2),
            ], style={"marginTop": "10px"}),
        ], style=margins_style),
        html.Div([
            dbc.Row([
                dbc.Col(["Ano de Lavratura", comps.slide_ano_lavratura],
                        sm=12, md=12, lg=7),
                dbc.Col(["Mês de Lavratura", comps.slide_mes])
            ]),
        ], style=margins_style),
        html.Div([
            dbc.Row([
                dbc.Col(["Ano da Situação Atual", comps.slide_ano_sit_atual],
                        sm=12, md=12, lg=7),
                dbc.Col(["Mês da Situação Atual", comps.slide_mes_lavratura])
            ]),
        ], style=margins_style),
        html.Hr(),

        # KPIs
        html.Div([
            dbc.Row(id="kpi-cabecalho"),
            dbc.Row(comps.kpi_txt),
        ], style=margins_style),

        # tab ganho/perda
        comps.novos_processos,
        html.Div([
            dbc.Row(
                html.H3("Evolução dos processos por data de extração")
            ),
            dbc.Row(
                html.P("Cada data se refere a um banco enviado com com "
                       "o status dos processos naquele momento.")
            ),
            dbc.Row([
                dbc.Col([
                    html.Div(comps.radio_tab_cont_datasets)
                ]),
            ]),
            dbc.Row([
                dbc.Col(id="tab-resultado"),
            ])
        ], style=margins_style),
        html.Div([
            dbc.Row([
                html.H3("Evolução dos valores quitados e parcelados")
            ]),
            dbc.Row([
                html.P("Clique nas legendas para destacar um segmento.")
            ]),
            dbc.Row([
                dbc.Col(dcc.Graph(
                    id="bar-quitados-parcelados",
                    config={'displayModeBar': False}), width=7),
                dbc.Col([
                    html.Div(html.P("Clique em cada segmento das barras "
                                    "para visualizar tabela com as razões "
                                    "sociais e seus respectivos valores "
                                    "pagos.")),
                    html.Div(id="tab-output")
                ], width=5, style={"marginTop": "10px"})
            ])
        ]),

        # stacked bar
        html.Div([
            dbc.Row([
                html.H3("Distribuição dos processos"),
            ]),
            dbc.Row([
                dbc.Col(dcc.Graph(id="stacked-bar-processos",
                                  config={'displayModeBar': False}),
                        sm=12, md=12, lg=6),
                dbc.Col(dcc.Graph(id="stacked-bar-valor",
                                  config={'displayModeBar': False}),
                        ),
            ])
        ], style=margins_style),

        # combo chart
        html.Div([
            dbc.Row([
                html.H3("Evolução por ano de lavratura")
            ]),
            dbc.Row([
                html.P("Distribuição dos processos por ano (barras azuis, "
                       "primeiro eixo) e por valores (linha vermelha, "
                       "segundo eixo)."),
            ]),
            dbc.Row([
                dbc.Col(dcc.Graph(id="combo-chart",
                                  config={'displaylogo': False}))
            ])
        ], style=margins_style),

        # dot plot
        html.Div([
            dbc.Row([
                dbc.Col([
                    html.H3("Data de lavratura vs data da situação atual")
                ]),
            ]),
            dbc.Row([
                dbc.Col([
                    html.Div(comps.dot_chart_txt),
                    html.Div(comps.radio_dot_chart),
                ], style={"marginTop": "30px"},
                    sm=12, md=12, lg=3
                ),
                dbc.Col(dcc.Graph(
                    id="dot-line-chart",
                    config={'displaylogo': False}),
                    style={"overflowY": "auto", "maxHeight": "600px"},
                    className="no-scrollbars")
            ], justify="between"),
            # footer
            html.Div(),
        ], style=margins_style),

        # table
        html.Div([
            dbc.Row([
                html.H3("Detalhe dos processos")
            ]),
            dbc.Row(
                html.P("Utilize os filtros do topo da página para refinar"
                       "a pesquisa.")
            ),
            dcc.Tabs(id='tabs-caf', value='tab-1', children=[
                dcc.Tab(
                    label="Detalhe Razão Social",
                    value='tab-1',
                    style=comps.tab_style,
                    selected_style=comps.tab_selected_style
                ),
                dcc.Tab(
                    label="Detalhe Situação",
                    value='tab-2',
                    style=comps.tab_style,
                    selected_style=comps.tab_selected_style
                ),
            ], style=comps.tabs_styles),
            html.Div(id='tabs-caf-conteudo')
        ], style=margins_style)
    ]),
    components.footer
])
