# Importando as bibliotecas e módulos necessários
from dash import Dash, State, Input, Output, html, dcc
from app.dashboards.consulta_tesouro.layout import extract, carrega_municipios, generate_output_table, convert_df
import pandas as pd
import base64


df_municipio = carrega_municipios()


app = Dash(__name__)
server = app.server


def callbacks(app):
    @app.callback(
        Output("loading-output", "children"),
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
    def extract_and_download_data(n_clicks, documento, anos, periodos, entes, anexo):

        if n_clicks is None:
            return [], []


        if not (documento and anos and periodos and entes and anexo):
            return [html.H3("Por favor, preencha todos os campos.", style={"color": "black"})], []


        df_municipios_filtered = df_municipio[df_municipio["cod_completo"].isin(entes)]
        cod_entes = df_municipios_filtered["cod_completo"].tolist()
        nome_entes = df_municipios_filtered["nome_municipio"].tolist()


        data = extract(anos, periodos, documento, anexo, cod_entes, nome_entes)


        csv_data = data.to_csv(index=False).encode("utf-8")


        download_link = html.A(
            "Clique aqui para fazer o download dos dados",
            href=f"data:text/csv;base64,{base64.b64encode(csv_data).decode()}",
            download="dados_extraidos.csv",
            target="_blank",  
        )


        output_children = [
            html.H3("Dados extraídos:", style={"color": "black"}),
            download_link,
            html.Table(
                # Cabeçalho da tabela
                [html.Tr([html.Th(col) for col in data.columns])] +
                # Linhas da tabela
                [html.Tr([html.Td(val) for val in row]) for row in data.values],
                style={"border": "1px solid black", "border-collapse": "collapse"}
            )
        ]

        return [], output_children


if __name__ == "__main__":
    callbacks(app)
    app.run_server()
