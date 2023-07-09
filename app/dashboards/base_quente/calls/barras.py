from dash import Input, Output
from app.dashboards.base_quente.data import filtra_base
from app.dashboards.base_quente.bq_graficos.barras import (
    ytd_barras_por_tributo, mtd_barras_por_tributo, ytd_barras, mtd_barras)


def barras(app):
    @app.callback(
        [
            Output("chart4", "figure"),
            Output("chart5", "figure"),
            Output("chart6", "figure"),
            Output("chart7", "figure")
        ],
        [
            Input("drop-atribuicao", "value"),
            Input("drop-grupo", "value"),
            Input("drop-receita-local", "value"),
            Input("calendario-date-range-picker", "value")
        ]
    )
    def bars(atr, grp, nm, cal):
        df = filtra_base(cal, atr, grp, nm)
        return ytd_barras(df), mtd_barras(df), ytd_barras_por_tributo(df), \
            mtd_barras_por_tributo(df)
