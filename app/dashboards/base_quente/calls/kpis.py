from dash import Input, Output
from app.dashboards.base_quente.data import filtra_base
from app.dashboards.base_quente.bq_graficos.cartoes import ytd_card, \
    mtd_card, wtd_card


def kpis(app):
    @app.callback(
        [
            Output("chart1", "figure"),
            Output("chart2", "figure"),
            Output("chart3", "figure")
        ],
        [
            Input("drop-atribuicao", "value"),
            Input("drop-grupo", "value"),
            Input("drop-receita-local", "value"),
            Input("calendario-date-range-picker", "value")
        ],
    )
    def gera_kpi(atr, grp, nm, cal):
        df = filtra_base(cal, atr, grp, nm)
        return ytd_card(df), mtd_card(df), wtd_card(df)
