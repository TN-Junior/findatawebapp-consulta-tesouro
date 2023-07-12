from dash import html, dcc
import dash_bootstrap_components as dbc

from app.dashboards.utils import components
from app.dashboards.base_quente.bq_components import bq_dcc
from app.dashboards.base_quente.bq_components import bq_html


layout = html.Div([
    components.navbar,
    dbc.Container([
        dbc.Row([
            dbc.Col(
                html.H1([
                    html.I(className='fa fa-money', style={'fontSize': '80%'}),
                    bq_html.dash_titulo
                ])
            ),
        ], style={'marginTop': '15px'}),
        dbc.Row([
            dbc.Col(html.P(bq_html.dash_descricao)),
        ]),
        dbc.Row([
            html.Div(id='rajada'),
            html.Div(id='dash_data'),
        ], id='subtitulo', style={'marginBottom': 25}),
        dbc.Row([
            dbc.Col(bq_dcc.calendar, width=4),
        ], style={'marginBottom': 25}),
        dbc.Row([
            dbc.Col(bq_dcc.drop_atribuicao),
            dbc.Col(bq_dcc.drop_grupo_receita),
            dbc.Col(bq_dcc.drop_nome_receita),
        ], style={'marginBottom': 25},
            class_name='row row-cols-lg-3 row-cols-sm-1'),
        dbc.Row(id='mensagem-filtros'),
        dbc.Row([
            dbc.Col(
                dcc.Graph(id='chart1', config={'displaylogo': False})
            ),
            dbc.Col(
                dcc.Graph(id='chart2', config={'displaylogo': False})
            ),
            dbc.Col(
                dcc.Graph(id='chart3', config={'displaylogo': False})
            )
        ], class_name='row row-cols-lg-3 row-cols-sm-1'
        ),
        dbc.Row([
            html.P(
                html.I('*Valores percentuais são em relação ao mesmo período '
                       'do ano anterior'), style={'fontSize': '70%'}
            )
        ]),
        dbc.Row([
            dbc.Col(
                dcc.Graph(id='chart4', config={'displaylogo': False})
            ),
            dbc.Col(
                dcc.Graph(id='chart5', config={'displaylogo': False})
            )
        ]),
        dbc.Row([
            dbc.Col(
                dcc.Graph(id='chart6', config={'displaylogo': False})
            ),
            dbc.Col(
                dcc.Graph(id="chart7", config={'displaylogo': False})
            )
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='chart9', config={'displaylogo': False})
            ])
        ]),
        dbc.Row([
            dbc.Col(
                html.P(bq_html.tab_descrição)
            )
        ]),
        dbc.Row([
            dbc.Col(
                html.Div(id='chart8')
            ),
        ], style={'marginBottom': 25})
    ]),
    components.footer
])
