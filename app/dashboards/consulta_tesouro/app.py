import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import time
import base64
import io

from app.dashboards.utils import components
from app.dashboards.consulta_tesouro.components import dcc_embed
from app.dashboards.consulta_tesouro.SiconfiHandler import SiconfiHandler

app = dash.Dash(__name__)
server = app.server  # Configuração do servidor

def carrega_municipios():
    df_municipio = pd.read_excel(
        "findatawebapp/app/dashboards/consulta_tesouro/dicio/cd_municipio_.xlsx",
        sheet_name="Sheet1",
        usecols=["cod_completo", "nome_municipio"],
    )
    return df_municipio

def convert_df(df):
    return df.to_csv(index=False).encode("utf-8")

def extract(anos, periodos, documento, anexo, cod_entes, nome_entes):
    sh = SiconfiHandler()
    dfs = []
    for ano in anos:
        for periodo in periodos:
            for cod_ente, municipio in zip(cod_entes, nome_entes):
                sh.mount_url(
                    ano, periodo, documento, anexo, cod_ente, municipio, debug=True
                )
                print(
                    f"Extraindo {documento} - {municipio} - {periodo} - {ano} ANEXO {documento}"
                )
                df = sh.receive_data()
                dfs.append(df)
                time.sleep(0.5)
    df = pd.concat(dfs)
    return df

def generate_output_table(data):
    return html.Table(
        [html.Tr([html.Th(col) for col in data.columns])] +
        [html.Tr([html.Td(val) for val in row]) for row in data.values],
        id="output-table-data"
    )


df_municipio = carrega_municipios()
documentos = ["RREO", "RGF"]

layout = html.Div(
    components.navbar,
    style={"background-color": "white"},
    children=[
        html.Div(
            style={"background-color": "white", "padding": "20px", "margin-bottom": "30px"},
            children=[
                html.H1("Extrator de dados do Siconfi", style={"text-align": "center", "color": "black"}),
                components.footer,
                
                
            ],
        ),
        
        html.Div(
            style={"background-color": "#0f3057", "padding": "20px", "border-radius": "10px", "margin": "0 auto", "max-width": "600px"},
            children=[
                html.H3("Menu", style={"color": "white"}),
                html.Label("Selecione o documento", style={"color": "white"}),
                dcc.Dropdown(id="documento-dropdown", options=[{"label": doc, "value": doc.lower()} for doc in documentos], placeholder="Selecione o documento", style={"width": "100%"}),
                
                html.Label("Selecione o exercício", style={"color": "white"}),
                dcc.Dropdown(id="anos-dropdown", options=[{"label": str(ano), "value": ano} for ano in range(2015, 2024)], multi=True, placeholder="Selecione o exercício", style={"width": "100%"}),
                
                html.Label("Selecione o período de referência (bimestre/quadrimestre)", style={"color": "white"}),
                dcc.Dropdown(id="periodos-dropdown", options=[{"label": str(p), "value": p} for p in range(1, 7)], multi=True, placeholder="Selecione o período de referência", style={"width": "100%"}),
                
                html.Label("Selecione o ente", style={"color": "white"}),
                dcc.Dropdown(id="entes-dropdown", options=[{"label": mun, "value": cod} for mun, cod in zip(df_municipio["nome_municipio"], df_municipio["cod_completo"])], multi=True, placeholder="Selecione o ente", style={"width": "100%"}),
                
                html.Label("Selecione o anexo", style={"color": "white"}),
                dcc.Dropdown(id="anexo-dropdown", options=[{"label": str(an), "value": str(an)} for an in [1, 2, 3, 4, 5, 6, 7, 10]], placeholder="Selecione o anexo", style={"width": "100%"}),
                
                
                html.Button("Extrair dados", id="extract-button"),
                html.Table(id="output-table"),
                html.Div(id="output-data")
            ],
        ),
        
        dcc.Download(id="download-link", data=None)
        
        
    ],
    
)


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


if __name__ == "__main__":
    app.run_server()
