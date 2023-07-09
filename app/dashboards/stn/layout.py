from dash import html, dcc
from app.dashboards.stn.componentes import contas_dropdown, regioes_dropdown, \
    bimestre_slider, ano_slider, agregacao_radio, mes_slider, formato_radio
import dash_bootstrap_components as dbc
from app.dashboards.utils import components

margens_div_principais = {'marginTop': 25, 'marginBottom': 35}

layout = html.Div([
    components.navbar,
    dbc.Container([
        # cabeçalho
        html.Div([
            dbc.Row(
                dbc.Col(
                    html.H2("Painel Tesouro Regional")
                )
            )
        ], style=margens_div_principais),

        # filtros
        html.Div([
            dbc.Row(
                dbc.Col(
                    html.H5("Filtros")
                ), style={'marginBottom': 15}
            ),

            dbc.Row([
                dbc.Col(html.I("Conta"), width=6),
                dbc.Col(html.I("Região"), width=2),
                dbc.Col(html.I("Ver valores como:"), width=4)
            ]),

            dbc.Row([
                dbc.Col(contas_dropdown, width=6),
                dbc.Col(regioes_dropdown, width=2),
                dbc.Col(formato_radio, width=4)
            ],
                align="center",
                style={'marginBottom': 25}
            ),

            dbc.Row([
                dbc.Col(html.I("Filtro de Ano")),
                dbc.Col(html.I("Filtro de Mês")),
                dbc.Col(html.I("Filtro de Bimestre"), width=3),
            ]),

            dbc.Row([
                dbc.Col(ano_slider),
                dbc.Col(mes_slider),
                dbc.Col(bimestre_slider, width=3),
            ]),
        ], style=margens_div_principais),

        html.Br(),

        # gráficos
        html.Div([
            dbc.Row([
                dbc.Col([
                    dbc.Row(html.I("Escolha o tipo de agregação:")),
                    dbc.Row(agregacao_radio),
                    dbc.Row([
                        dcc.Graph(id="grafico-barras-recife-valores")
                    ]),
                    dbc.Row([
                        dcc.Graph(id="grafico-linhas-recife-valores")
                    ]),
                ], width=7),
                dbc.Col([
                    dcc.Graph(id="grafico-barras-ranking-capitais")
                ], width=5)
            ]),

            html.Div([
                html.H5("Mapa"),
                html.P("Passe o mouse pelos pontos para informações."),
                html.P("Tamanho dos pontos de acordo com a Receita Per "
                       "Capita."),
            ]),

            html.Div(
                dcc.Graph(id="mapa-capitais")
            )
        ], style=margens_div_principais)
    ]),
    components.footer
])
