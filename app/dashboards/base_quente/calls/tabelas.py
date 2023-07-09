from dash import Input, Output
from app.dashboards.base_quente.data import filtra_base
from app.dashboards.base_quente.bq_graficos.tabelas import tab_por_mes


def tabelas(app):
    @app.callback(
        Output("chart8", "children"),
        [
            Input("drop-atribuicao", "value"),
            Input("drop-grupo", "value"),
            Input("drop-receita-local", "value"),
            Input("calendario-date-range-picker", "value")
        ]
        )
    def table(atr, grp, nm, cal):
        df = filtra_base(cal, atr, grp, nm)
        return tab_por_mes(df)
