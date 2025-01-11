#layout
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import time

from app.dashboards.utils import components
from app.dashboards.consulta_tesouro.SiconfiHandler import SiconfiHandler  # Import the SiconfiHandler class


app = dash.Dash(__name__)
server = app.server

def carrega_municipios():
    df_municipio = pd.read_excel(
        "app/dashboards/consulta_tesouro/dicio/cd_municipio_.xlsx",
        sheet_name="Sheet1",
        usecols=["cod_completo", "nome_municipio"],
    )
    return df_municipio

def convert_df(df):
    return df.to_csv(index=False).encode("utf-8")



def extract(anos, periodos, documento, anexo, cod_entes, nome_entes):
    print("Anos:", anos)
    print("Períodos:", periodos)
    print("Documento:", documento)
    print("Anexo:", anexo)
    print("Códigos de Ente:", cod_entes)
    print("Nomes de Ente:", nome_entes)
    sh = SiconfiHandler()  # Initialize the SiconfiHandler
    dfs = []
    for ano in anos:
        for periodo in periodos:
            for cod_ente, municipio in zip(cod_entes, nome_entes):
                try:
                    sh.mount_url(
                        ano, periodo, documento, anexo, cod_ente, municipio, debug=True
                    )
                    print(
                        f"Extraindo {documento} - {municipio} - {periodo} - {ano} ANEXO {anexo}"
                    )
                    df = sh.receive_data()
                    dfs.append(df)
                    time.sleep(3)
                except Exception as e:
                    print(f"Error extracting data: {str(e)}")
    df = pd.concat(dfs)
    print("Total de dados extraídos:", len(df))  # Adicione esta linha para verificar o número de linhas no DataFrame
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
    [
        components.navbar,
        html.Div(
            style={"background-color": "white", "padding": "20px", "margin-bottom": "30px"},
            children=[
                html.H1("Extrator de dados do Siconfi", style={"text-align": "center", "color": "black"}),
            ],
        ),
        html.Div(
            style={"background-color": "#0f3057", "padding": "20px", "border-radius": "10px", "margin": "0 auto", "max-width": "600px", "max-height": "80vh", "overflow-y": "auto",},
            children=[
                html.H3("Menu", style={"color": "white"}),
                html.Label("Selecione o documento", style={"color": "white"}),
                dcc.Dropdown(id="documento-dropdown", options=[{"label": doc, "value": doc.lower()} for doc in documentos], placeholder="Selecione o documento", style={"width": "100%"}),
                html.Label("Selecione o exercício", style={"color": "white"}),
                dcc.Dropdown(id="anos-dropdown", options=[{"label": str(ano), "value": ano} for ano in range(2015, 2026)], multi=True, placeholder="Selecione o exercício", style={"width": "100%"}),
                html.Label("Selecione o período de referência (bimestre/quadrimestre)", style={"color": "white"}),
                dcc.Dropdown(id="periodos-dropdown", options=[{"label": str(p), "value": p} for p in range(1, 7)], multi=True, placeholder="Selecione o período de referência", style={"width": "100%"}),
                html.Label("Selecione o ente", style={"color": "white"}),
                dcc.Dropdown(id="entes-dropdown", options=[{"label": mun, "value": cod} for mun, cod in zip(df_municipio["nome_municipio"], df_municipio["cod_completo"])], multi=True, placeholder="Selecione o ente", style={"width": "100%"}),
                html.Label("Selecione o anexo", style={"color": "white"}),
                dcc.Dropdown(id="anexo-dropdown", options=[{"label": str(an), "value": str(an)} for an in [1, 2, 3, 4, 5, 6, 7, 10]], placeholder="Selecione o anexo", style={"width": "100%"}),
                html.Button("Extrair dados", id="extract-button"),
                dcc.Loading(
                    id="loading-extract-button",
                    type="circle",
                    children=html.Div(id="loading-output"),
        ),
            ],
        ),
        # Adicione um div separado para a tabela com um fundo branco
        html.Div(
            [
                html.Table(id="output-table", style={"background-color": "white"}),
                html.Div(id="output-data"),
                html.Div(id="output-div"),
                dcc.Download(id="download-link", data=None),
            ],
            style={"background-color": "white"},
        ),
        components.footer,
    ],
    style={"background-color": "white"},
)

# Adicione um callback para atualizar o estilo do botão quando clicado
@app.callback(
    Output("extract-button", "style"),
    [Input("extract-button", "n_clicks")],
    prevent_initial_call=True  # Evita que o callback seja chamado na inicialização
)
def update_button_style(n_clicks):
    if n_clicks % 2 == 1:
        # Botão foi clicado, altera a cor para azul
        return {
            "background-color": "#0f3057",
            "color": "white",
            "border": "2px solid #0f3057",
            "padding": "10px 20px",
            "cursor": "pointer",
            "transition": "background-color 0.3s",
        }
    else:
        # Sem clique, estilo padrão
        return {
            "background-color": "white",
            "color": "#0f3057",
            "border": "2px solid #0f3057",
            "padding": "10px 20px",
            "cursor": "pointer",
            "transition": "background-color 0.3s",
        }

if __name__ == "__main__":
    app.run_server()