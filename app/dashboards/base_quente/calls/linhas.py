from dash import Input, Output
from app.dashboards.base_quente.data import filtra_base
from app.dashboards.base_quente.bq_graficos.linhas import linhas_serie_completa


def linhas(app):
    @app.callback(
        Output("chart9", "figure"),
        [
            Input("drop-atribuicao", "value"),
            Input("drop-grupo", "value"),
            Input("drop-receita-local", "value"),
            Input("calendario-date-range-picker", "value")
        ]
    )
    def lines(atr, grp, nm, cal):
        df = filtra_base(cal, atr, grp, nm)
        return linhas_serie_completa(df)
