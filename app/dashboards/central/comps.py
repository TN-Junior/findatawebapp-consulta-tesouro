from dash import html
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc

from app.dashboards.central.data import (
    df_pf,
    df_ggaf,
    df_rri,
    df_rcl,
    df_liquidez,
    data_ref_str,
    data_ref
)
from app.dashboards.central.table import (
    tab_previsao_pf_ggaf_rri,
    tab_previsao_rcl,
    tab_liquidez,
    tab_exemplo,
    formatacao_cabecalho
)


def accord_comp(titulo, tabela, botao_id):
    comp = dmc.AccordionItem(
        [
            dbc.Row(
                [
                    # html.I("Valores em milhões"),
                    tabela
                ],
                style={'marginBottom': 25, 'marginTop': 25},
            ),
            html.Button(
                'Exportar',
                id=botao_id,
                **{f'data-{botao_id}': ''},
                style={'border': 0},
            ),
        ],
        label=titulo,
    )
    return comp


ano_ref = data_ref.year
estilo_cabecalho = formatacao_cabecalho(data_ref.month)

tab_pf = tab_previsao_pf_ggaf_rri(
    df_pf, 'tabela-painel-fiscal', estilo_cabecalho, ano_ref
)
accord_pf = accord_comp('Painel Fiscal', tab_pf, 'btn-painel-fiscal')

tab_ggaf = tab_previsao_pf_ggaf_rri(
    df_ggaf, 'tabela-ggaf', estilo_cabecalho, ano_ref
)
accord_ggaf = accord_comp('GGAF', tab_ggaf, 'btn-ggaf')

tab_rri = tab_previsao_pf_ggaf_rri(
    df_rri, 'tabela-rri', estilo_cabecalho, ano_ref
)
accord_rri = accord_comp('RRI', tab_rri, 'btn-rri')

tab_rcl = tab_previsao_rcl(
    df_rcl, 'tabela-rcl', estilo_cabecalho, ano_ref
)
accord_rcl = accord_comp('RCL', tab_rcl, 'btn-rcl')

tab_liquidez = tab_liquidez(
    df_liquidez, 'tabela-liquidez'
)
accord_liq = accord_comp('Liquidez', tab_liquidez, 'btn-liquidez')

accor = dmc.Accordion(
    children=[accord_pf, accord_ggaf, accord_rri, accord_rcl, accord_liq]
)

tab_explo = tab_exemplo(ano_ref)
texto_exemplo = html.P(
    [
        'As colunas de meses com os valores previstos possuem ',
        html.Span(
            'fundo branco com a cor da fonte azul. ',
            style={
                'backgroundColor': 'white',
                'color': 'darkBlue'
            }
        ),
        'Valores com dados realizados possuem colunas de meses com ',
        html.Span(
            'fundo cinza escuro',
            style={
                'backgroundColor': '#E6E6E6'
            }
        ),
        '. Há também a coluna "Conta" e ',
        html.Span(f'"{ano_ref}" que totaliza todos os meses.'),
    ]
)
intro = html.Div([
    html.H2('Central de Previsões'),
    html.H5(
        'Página com previsões de receita para diversos tributos, '
        'por área de atuação.',
        style={'marginBottom': 25}
    ),
    html.H6("Como ler as tabelas:"),
    dbc.Row(
        [
            dbc.Col([texto_exemplo], width=4),
            dbc.Col([tab_explo], width=8)
        ],
        style={'marginBottom': 10}
    ),
    html.P(
        f'Dados previstos acontecem após {data_ref_str}. '
        f'Clique nos tópicos para ver cada tabela.')
])
