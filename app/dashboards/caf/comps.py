from dash import html, dcc
import dash_bootstrap_components as dbc
from app.dashboards.caf.data import coluna_vals, data_arquivo, \
    anos_intervalo, novos_processos

link_decreto = "https://leismunicipais.com.br/a/pe/r/recife/decreto/2014/" \
               "2802/28021/decreto-n-28021-2014-aprova-o-regulamento-do-" \
               "conselho-administrativo-fiscal-caf-e-dispoe-sobre-o-" \
               "julgamento-do-contencioso-administrativo-tributario-em-" \
               "primeira-e-segunda-instancias-administrativas"

link_lei = "https://leismunicipais.com.br/a/pe/r/recife/lei-ordinaria/2016/" \
           "1827/18276/lei-ordinaria-n-18276-2016-dispoe-sobre-a-" \
           "organizacao-estrutura-e-competencia-do-contencioso-" \
           "administrativo-tributario-do-municipio-do-recife-e-da-outras-" \
           "providencias"

intro = [
    html.H1([
        html.I(className="fa fa-gavel", style={'fontSize': '80%'}),
        " Conselho Adminitrativo Fiscal (CAF)"
    ]),
    html.P([
        "Regulamentado pelo decreto ",
        html.A("28.021/14 ", href=link_decreto,
               target="_blank"),
        "e instituído pela lei ",
        html.A("18.276/16", href=link_lei, target="_blank"),
        html.Br(),
        f"Dados até: {data_arquivo()}"
    ])
]

meses = ["jan", "fev", "mar", "abr", "mai", "jun",
         "jul", "ago", "set", "out", "nov", "dez"]

rs = coluna_vals("razao_social")
rs_process = coluna_vals("razao_social_process")
situacao_atual = coluna_vals("desc_sit_atual")
sit_debito = coluna_vals("situacao_debito")
mudanca_status = coluna_vals("mudanca_status")
instancia = coluna_vals("instancia")
finalizado = coluna_vals("flag_sit_terminativa")
fora_caf = coluna_vals("flag_sit_fora_caf")
anos = anos_intervalo()

drop_razao_social = dcc.Dropdown(
    id="drop-razao-social",
    options=[
        {"label": rs, "value": rs} for rs in rs
    ],
    placeholder="Razão Social",
    multi=True
)

drop_razao_social_processo = dcc.Dropdown(
    id="drop-razao-social-processo",
    options=[
        {"label": rs, "value": rs} for rs in rs_process
    ],
    placeholder="Razão Social - Nº Processo",
    multi=True
)

drop_situacao_debito = dcc.Dropdown(
    id="drop-situacao-debito",
    options=[
        {"label": sd, "value": sd} for sd in sit_debito
    ],
    placeholder="Situação Débito",
    multi=True
)

drop_situacao_atual = dcc.Dropdown(
    id="drop-situacao-atual",
    options=[
        {"label": sa, "value": sa} for sa in situacao_atual
    ],
    placeholder="Situação Atual do Processo",
    multi=True
)

drop_mudanca_status = dcc.Dropdown(
    id="drop-mudanca-status",
    options=[
        {"label": ms, "value": ms} for ms in mudanca_status
    ],
    placeholder="Tramitaram desde última atualização",
    multi=True
)

drop_instancia = dcc.Dropdown(
    id="drop-instancia",
    options=[
        {"label": inst, "value": inst} for inst in instancia
    ],
    placeholder="Instância",
    multi=True
)

drop_finalizado = dcc.Dropdown(
    id="drop-finalizado",
    options=[
        {"label": inst, "value": inst} for inst in finalizado
    ],
    placeholder="Finalizados",
    multi=True
)

drop_fora_caf = dcc.Dropdown(
    id="drop-fora-caf",
    options=[
        {"label": inst, "value": inst} for inst in fora_caf
    ],
    placeholder="Fora do CAF",
    multi=True
)

slide_ano_lavratura = dcc.RangeSlider(
    id="slide-anos",
    min=min(anos),
    max=max(anos),
    # step=1,
    marks={i: f"{i}" for i in anos[::4]},
    value=[min(anos), max(anos)],
    tooltip={"placement": "bottom", "always_visible": False}
)

slide_mes = dcc.RangeSlider(
    id="slide-meses",
    min=1,
    max=12,
    marks={i: m for i, m in zip(list(range(1, 13)), meses)},
    value=[1, 12]
)

slide_mes_lavratura = dcc.RangeSlider(
    id="slide-meses-sit-atual",
    min=1,
    max=12,
    marks={i: m for i, m in zip(list(range(1, 13)), meses)},
    value=[1, 12]
)

slide_ano_sit_atual = dcc.RangeSlider(
    id="slide-anos-sit-atual",
    min=min(anos),
    max=max(anos),
    marks={i: f"{i}" for i in anos[::4]},
    value=[min(anos), max(anos)],
    tooltip={"placement": "bottom", "always_visible": False}
)

radio_dot_chart = dcc.RadioItems(
    id="radio-dot-chart",
    options=[
        {"label": "Data de situação mais antiga", "value": "situacao"},
        {"label": "Maior intervalo entre datas", "value": "intervalo"}
    ],
    value="situacao"
)

radio_tab_cont_datasets = dcc.RadioItems(
    id="radio-tab-cont-datasets",
    options=[
        {"label": "Contagem", "value": "cd_processo"},
        {"label": "Valor Total Devido", "value": "valor_total"}
    ],
    value="cd_processo",
    labelStyle={'display': 'inline-block', 'width': 200}
)

kpi_txt = [
    html.I(
        html.P([
            "Para visualizar informaçoes apenas de processos ativos, selecione"
            " 'N' para os filtros 'Fora do CAF' e 'Finalizados'.",
            html.Br(),
            "O tempo médio em dias é o intervalo entre a data de lavratura e"
            " a última data de movimentação."
        ], style={"fontSize": "90%"})
    ),
]

dot_chart_txt = [
    html.P("O gráfico ao lado lista razão social pela data de lavratura e da "
           "situação atual (última data de movimentação)."),
    html.P("Abaixo, escolha se esta lista será visualizada de acordo com a "
           "diferença entre essas datas ou para ordenar pela data de situação "
           "mais antiga.")
]


def kpis(vals):
    row = [
        # global
        dbc.Col([
            html.H4("Global", style={"textAlign": "center"}),
            dbc.Row([
                dbc.Col(
                    [html.I(className="fa fa-file-text-o"),
                     f" Processos: {vals[0]:,}"]),
            ], style={"textAlign": "center"}),
            dbc.Row([
                dbc.Col(
                    [html.I(className="fa fa-usd"),
                     f" Valor: R$ {vals[1]:,.0f}"]),
            ], style={"textAlign": "center"}),
            dbc.Row([
                dbc.Col(
                    [html.I(className="fa fa-clock-o"),
                     f" Dias (em média): {vals[2]:,.0f}"]),
            ], style={"textAlign": "center"})
        ],
            style={
                "backgroundColor": "rgb(248, 248, 255)",
                "padding": "20px"},
            ),
        # ativos
        dbc.Col([
            html.H4("Ativos", style={"textAlign": "center"}),
            dbc.Row([
                dbc.Col(
                    [html.I(className="fa fa-file-text-o"), f" {vals[3]:,}"]),
            ], style={"textAlign": "center"}),
            dbc.Row([
                dbc.Col(
                    [html.I(className="fa fa-usd"), f" R$ {vals[4]:,.0f}"]),
            ], style={"textAlign": "center"}),
            dbc.Row([
                dbc.Col(
                    [html.I(className="fa fa-clock-o"),
                     f" {vals[5]:,.0f}"]),
            ], style={"textAlign": "center"})
        ],
            style={
                "backgroundColor": "rgb(248, 248, 255)",
                "padding": "20px"},
            ),
        # Tramitados
        dbc.Col([
            html.H4("Tramitados", style={"textAlign": "center"}),
            dbc.Row([
                dbc.Col(
                    [html.I(className="fa fa-file-text-o"), f" {vals[6]:,}"]),
            ], style={"textAlign": "center"}),
            dbc.Row([
                dbc.Col(
                    [html.I(className="fa fa-usd"), f" R$ {vals[7]:,.0f}"]),
            ], style={"textAlign": "center"}),
            dbc.Row([
                dbc.Col(
                    [html.I(className="fa fa-clock-o"), f" {vals[8]:,.0f}"]),
            ], style={"textAlign": "center"})
        ],
            style={
                "backgroundColor": "rgb(248, 248, 255)",
                "padding": "20px"},
            ),
        # Finalizados
        dbc.Col([
            html.H4("Finalizados", style={"textAlign": "center"}),
            dbc.Row([
                dbc.Col(
                    [html.I(className="fa fa-file-text-o"), f" {vals[9]:,}"]),
            ], style={"textAlign": "center"}),
            dbc.Row([
                dbc.Col(
                    [html.I(className="fa fa-usd"), f" R$ {vals[10]:,.0f}"]),
            ], style={"textAlign": "center"}),
            dbc.Row([
                dbc.Col(
                    [html.I(className="fa fa-clock-o"), f" {vals[11]:,.0f}"]),
            ], style={"textAlign": "center"})
        ],
            style={
                "backgroundColor": "rgb(248, 248, 255)",
                "padding": "20px"},
            ),
        # Dívida Ativa
        dbc.Col([
            html.H4("Dívida Ativa", style={"textAlign": "center"}),
            dbc.Row([
                dbc.Col(
                    [html.I(className="fa fa-file-text-o"), f" {vals[12]:,}"]),
            ], style={"textAlign": "center"}),
            dbc.Row([
                dbc.Col(
                    [html.I(className="fa fa-usd"), f" R$ {vals[13]:,.0f}"]),
            ], style={"textAlign": "center"}),
            dbc.Row([
                dbc.Col(
                    [html.I(className="fa fa-clock-o"), f" {vals[14]:,.0f}"]),
            ], style={"textAlign": "center"})
        ],
            style={
                "backgroundColor": "rgb(248, 248, 255)",
                "padding": "20px"},
            ),
    ]
    return row


tabs_styles = {
    # 'height': '30px'
}
tab_style = {
    # 'borderBottom': '0px solid #d6d6d6',
    'padding': '3px',
    # 'fontWeight': 'bold'
}
tab_selected_style = {
    # 'borderTop': '0px solid #d6d6d6',
    # 'borderBottom': '1px solid #d6d6d6',
    # 'backgroundColor': '#119DFF',
    # 'color': 'white',
    'padding': '3px'
}

novos_processos = html.Div([
    dbc.Row([
        html.H3("Novos Processos")
    ]),
    dbc.Row([
        html.P(" | ".join(novos_processos()))
    ])
])