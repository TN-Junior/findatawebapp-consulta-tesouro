from dash import Input, Output
from app.dashboards.base_quente.data import filtra_base, dicionario

dic_receita = dicionario()


def filtros(app):
    @app.callback(
        [
            Output("drop-atribuicao", "data"),
            Output("drop-grupo", "data"),
            Output("drop-receita-local", "data")],
        [
            Input("drop-atribuicao", "value"),
            Input("drop-grupo", "value"),
            Input("drop-receita-local", "value"),
            Input("calendario-date-range-picker", "value"),
        ]
    )
    def filters(atr, grp, nm, cal):
        df_result = filtra_base(cal, None, grp, nm)
        rec1 = df_result.atribuicao.unique()

        df_result2 = filtra_base(cal, atr, None, nm)
        rec2 = df_result2.receita_contabil.unique()

        df_result3 = filtra_base(cal, atr, grp)
        rec3 = df_result3.cd_nm_receita.unique()

        return [rec1, rec2, rec3]
