import dash_bootstrap_components as dbc
from dash import html
from app.dashboards.monitoramento.graficos.tabelas import gera_tabela

from app.dashboards.monitoramento.data import Dataset

data = Dataset()


def gera_modal(is_open, obj_id):
    nm_obj, tab = gera_tabela(obj_id)
    modal = dbc.Modal([
                dbc.ModalHeader([html.H4(nm_obj)]),
                dbc.ModalBody(
                    html.Div(tab)
                ),
            ],
                id="modal",
                size="xl",
                is_open=is_open
            )
    return modal
