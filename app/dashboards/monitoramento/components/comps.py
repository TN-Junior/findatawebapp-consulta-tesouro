from dash import html, dcc
import dash_bootstrap_components as dbc
from app.dashboards.monitoramento.data import Dataset

data = Dataset()
dimensoes = data.dimensoes()

drop_setor = dcc.Dropdown(
    id='drop-setor',
    options=[
        {'label': att, 'value': att}
        for att in dimensoes["PLANILHA"]
        if att is not None
    ],
    placeholder="Setor",
    searchable=False,
    clearable=False,
    multi=False,
    value='TESOURO'
)

drop_estrategia = dcc.Dropdown(
    id='drop-estrategia',
    options=[
        {'label': 'Sim', 'value': 'SIM'},
        {'label': 'Não', 'value': 'NÃO'}
    ],
    # placeholder="Não",
    searchable=False,
    multi=False,
    clearable=False,
    value='NÃO'
)

drop_seplag = dcc.Dropdown(
    id='drop-seplag',
    options=[
        {'label': 'Sim', 'value': 'SIM'},
        {'label': 'Não', 'value': 'NÃO'}
    ],
    # placeholder="Não",
    searchable=False,
    multi=False,
    clearable=False,
    value='NÃO'
)

drop_concluidas = dcc.Dropdown(
    id='drop-concluidas',
    options=[
        {'label': 'Em 2022', 'value': '2022'},
        {'label': 'Em 2021', 'value': '2021'},
        {'label': 'Não', 'value': 'Não'}
    ],
    clearable=False,
    searchable=False,
    multi=False,
    value='Não'
)

drop_pnafm = dcc.Dropdown(
    id='drop-pnafm',
    options=[
        {'label': 'Sim', 'value': 'SIM'},
        {'label': 'Não', 'value': 'NÃO'}
    ],
    # placeholder="Não",
    searchable=False,
    multi=False,
    clearable=False,
    value='NÃO'
)

drop_operacional = dcc.Dropdown(
    id='drop-operacional',
    options=[
        {'label': 'Sim', 'value': 'SIM'},
        {'label': 'Não', 'value': 'NÃO'}
    ],
    # placeholder="Não",
    multi=False,
    searchable=False,
    clearable=False,
    value='NÃO'
)

modal = dbc.Modal([
    dbc.ModalHeader("Header"),
    dbc.ModalBody("This is the content of the modal")
],
    id="modal",
    size="xl",
    is_open=False
)

data = data.data_arquivo_str()
dt_arquivo = html.P(f"Dados de {data}")

descricao = html.Div([
    html.H1([
        html.I(className='fa fa-check-circle-o', style={'fontSize': '80%'}),
        " Monitoramento SEFIN"]
    ),
    html.H5(f"Seção para visualização de objetivos, "
            f"ações e tarefas das secretarias executivas."),
    dt_arquivo,
    html.P("Escolha uma área e clique nos botões azuis "
           "para visualizar ações e tarefas."),
    # html.P("Atualizações serão feitas às 18h.")
])
