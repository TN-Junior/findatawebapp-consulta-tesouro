from dash import Input, Output
from app.dashboards.base_quente import data


def rajada(app):
    @app.callback(
            [Output("dash_data", "children"),
             Output("rajada", "children")],
            Input("subtitulo", "children")
        )
    def data_dos_dados(foo):
        data_ref = f"Dados até: {data.data_ref_str()}"
        valor_rajada = data.df_rajada()
        txt_rajada = f"Rajada de {data.data_arquivo_str()}: " \
                     f"R${valor_rajada:,.2f}"
        return data_ref, txt_rajada
