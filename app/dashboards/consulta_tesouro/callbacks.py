from dash import State, Input, Output
from app.dashboards.consulta_tesouro.layout import extract, carrega_municipios, generate_output_table, convert_df
import pandas as pd
import io
import base64


df_municipio = carrega_municipios()

def callbacks(app):
    @app.callback(
        Output("output-div", "children"),
        [Input("extract-button", "n_clicks")],
        [
            State("documento-dropdown", "value"),
            State("anos-dropdown", "value"),
            State("periodos-dropdown", "value"),
            State("entes-dropdown", "value"),
            State("anexo-dropdown", "value"),
        ]
    )
    def extract_data(n_clicks, documento, anos, periodos, entes, anexo):
        if n_clicks is None:
            return []

        if not (documento and anos and periodos and entes and anexo):
            return "Por favor, preencha todos os campos"

        df_municipios_filtered = df_municipio[df_municipio["cod_completo"].isin(entes)]
        cod_entes = df_municipios_filtered["cod_completo"].tolist()
        nome_entes = df_municipios_filtered["nome_municipio"].tolist()

        data = extract(anos, periodos, documento, anexo, cod_entes, nome_entes)

        output_children = [
            html.H3("Dados extr aídos:", style={"color": "black"}),
            generate_output_table(data),
        ]

        return output_children




    if __name__ == "__main__":
        app.run_server()