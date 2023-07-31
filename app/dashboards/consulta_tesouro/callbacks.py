from dash import State, Input, Output
from app.dashboards.consulta_tesouro.layout import extract, carrega_municipios, generate_output_table, convert_df
import pandas as pd

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
    def extract_data(df_municipio, n_clicks, documento, anos, periodos, entes, anexo):
        if n_clicks is None:
            return []

        if not (documento and anos and periodos and entes and anexo):
            return "Por favor, preencha todos os campos"

        df_municipios_filtered = df_municipio[df_municipio["cod_completo"].isin(entes)]
        cod_entes = df_municipios_filtered["cod_completo"].tolist()
        nome_entes = df_municipios_filtered["nome_municipio"].tolist()

        data = extract(anos, periodos, documento, anexo, cod_entes, nome_entes)

        output_children = [
            html.H3("Dados extraídos:", style={"color": "black"}),
            generate_output_table(data),
        ]

        return output_children


    @app.callback(
        Output("download-link", "data"),
        [Input("extract-button", "n_clicks")],
        [State("output-table", "children")]
    )

    def download_data(n_clicks, children):
        if n_clicks is None:
            return None

        if n_clicks > 0:
            table = children[1].props.children[1]
            data = [list(map(lambda x: x.props.children, row.props.children)) for row in table.props.children]
            headers = [cell.props.children for cell in table.props.children[0].props.children]
            df = pd.DataFrame(data, columns=headers)
            csv = convert_df(df)

            # Criar um objeto de arquivo em memória
            buffer = io.BytesIO()
            buffer.write(csv)
            buffer.seek(0)

            # Codificar o arquivo em base64
            csv_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

            # Definir o conteúdo do arquivo e o nome do arquivo para download
            content = "data:text/csv;base64," + csv_base64
            filename = "dados_extraidos.csv"

            # Retornar os dados para download
            return dict(content=content, filename=filename)

        return None

    @app.callback(
        Output("output-data", "children"),
        [Input("extract-button", "n_clicks")],
        [
            State("documento-dropdown", "value"),
            State("anos-dropdown", "value"),
            State("periodos-dropdown", "value"),
            State("entes-dropdown", "value"),
            State("anexo-dropdown", "value"),
        ]
    )
    def update_output_data(n_clicks, documento, anos, periodos, entes, anexo):
        if n_clicks is None:
            return []

        if not (documento and anos and periodos and entes and anexo):
            return "Por favor, preencha todos os campos"

        df_municipios_filtered = df_municipio[df_municipio["cod_completo"].isin(entes)]
        cod_entes = df_municipios_filtered["cod_completo"].tolist()
        nome_entes = df_municipios_filtered["nome_municipio"].tolist()

        data = extract(anos, periodos, documento, anexo, cod_entes, nome_entes)

        return generate_output_table(data)

    @app.callback(
        Output("download-link", "data"),
        [Input("extract-button", "n_clicks")],
        [State("output-table", "children")]
    )
    def download_data(n_clicks, children):
        if n_clicks is None:
            return None

        if n_clicks > 0:
            table = children[1]
            data = [list(map(lambda x: x['props']['children'], row['props']['children'])) for row in
                    table['props']['children']]
            headers = [cell['props']['children'] for cell in table['props']['children'][0]['props']['children']]
            df = pd.DataFrame(data, columns=headers)
            csv = convert_df(df)

            # Criar um objeto de arquivo em memória
            buffer = io.BytesIO()
            buffer.write(csv)
            buffer.seek(0)

            # Codificar o arquivo em base64
            csv_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

            # Definir o conteúdo do arquivo e o nome do arquivo para download
            content = "data:text/csv;base64," + csv_base64
            filename = "dados_extraidos.csv"

            # Retornar os dados para download
            return dict(content=content, filename=filename)

        return None
