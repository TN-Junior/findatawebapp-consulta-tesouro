from dash import html
import dash_bootstrap_components as dbc

from app.dashboards.utils import components
from app.dashboards.monitoramento.components import comps

layout = html.Div([
    components.navbar,
    html.Div([
        html.Div(comps.modal, id="modal-obj"),
        dbc.Row([
            dbc.Col([
                comps.descricao
            ], style={"marginTop": 15})
        ]),
        dbc.Row([
            dbc.Col(["Escolha uma área:", comps.drop_setor]),
            dbc.Col(["Ver objetivos finalizados?", comps.drop_concluidas]),
            dbc.Col(["Ver apenas estratégicos?", comps.drop_estrategia]),
            dbc.Col(["Ver apenas Operacional?", comps.drop_operacional]),
            dbc.Col(["Ver apenas SEPLAG?", comps.drop_seplag]),
            dbc.Col(["Ver apenas PNAFM?", comps.drop_pnafm])
        ], style={"marginBottom": 25},
            class_name="row row-cols-1 row-cols-lg-6"),
        dbc.Row([
            dbc.Col(id="cards-obj")
        ], align="center"),
    ], style={"margin-left": 25, "margin-right": 25, "margin-top": 10}
    ),
    components.footer
])
