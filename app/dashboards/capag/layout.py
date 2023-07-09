from dash import html, dcc
import dash_bootstrap_components as dbc

from app.dashboards.utils import components
from app.dashboards.capag.components import comps


layout = html.Div([
    components.navbar,
    html.Div([
        # descrição
        dbc.Row([
            dbc.Col([
                comps.descricao,
            ], style={"padding": 5})
        ]),
        # endividamento
        dbc.Row([
            comps.endividamento
        ]),
        dbc.Row([
            comps.col_nota_end_realiz,
            comps.col_nota_end_proj,
        ], align="center"),
        dbc.Row(
            comps.meta_end, align="center",
            style={"height": 200}),
        dbc.Row([
            dbc.Col([
                dcc.Graph(figure=comps.end,
                          config={'displaylogo': False}),
            ]),
            dbc.Col([
                dcc.Graph(figure=comps.rcl_end,
                          config={'displaylogo': False}),
            ])
        ]),
        # poupancas correntes
        dbc.Row([
            dbc.Col([
                html.Hr(),
                comps.poupancas_correntes,
            ], sm=12, lg=6)
        ]),
        dbc.Row(id="nota-poup-corr"),
        dbc.Row(id="meta-poup-corr", align="center"),
        dbc.Row([
            dbc.Col([
                dbc.Row(comps.poup_corr_radio_ano),
                dbc.Row(dcc.Graph(id="poup-corr_graf",
                                  config={'displaylogo': False}))
            ]),
            dbc.Col([
                dbc.Row(comps.poup_corr_radio_cenarios),
                dbc.Row(dcc.Graph(id="desp-corr-rca-graf",
                                  config={'displaylogo': False})),
            ]),
        ], justify="start"),
        # liquidez
        dbc.Row([
            dbc.Col([
                html.Hr(),
                comps.liquidez
            ])
        ]),
        dbc.Row(id="nota-liquidez"),
        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    figure=comps.liq_ind_graf,
                    config={'displaylogo': False}),
            ]),
            dbc.Col([
                dcc.Graph(
                    figure=comps.liq_comps_graf,
                    config={'displaylogo': False}),
            ])
        ]),
        dbc.Row([
            dbc.Col([
                comps.card1,
            ]),
            dbc.Col([
                comps.card2
            ]),
            dbc.Col([
                comps.card3
            ]),
            dbc.Col([
                comps.card4
            ])
        ],
            justify="center",
            style={"margin-bottom": 35},
            class_name="row row-cols-2 row-cols-lg-4 row gy-2"),
        # desp. liq. / receitas
        dbc.Row([
            dbc.Col([
                html.Hr(),
                comps.despesas_correntes,
            ], sm=12, lg=6)
        ]),
        dbc.Row(id="nota-dc-rc"),
        dbc.Row([
            dbc.Col([
                html.Div([
                    comps.dc_rc_radio,
                ])
            ])
        ], justify="start"),
        dbc.Row([
            dbc.Col([
                dcc.Graph(id="dc-rc-graf",
                          config={'displaylogo': False}),
            ]),
            dbc.Col([
                dcc.Graph(id="desp-liq-rc-graf",
                          config={'displaylogo': False}),
            ])
        ]),
    ], style={"margin-left": 35, "margin-right": 35, "margin-top": 15}
    ),
    components.footer
])
