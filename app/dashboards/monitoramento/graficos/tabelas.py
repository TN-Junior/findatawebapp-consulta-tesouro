from dash import html, dash_table
from app.dashboards.monitoramento.data import Dataset

data = Dataset()

status_cores = [
    {
        'if': {'row_index': 'odd'},
        'backgroundColor': 'rgb(248, 248, 248)'
    },
    {
        'if': {
            'filter_query': '{STATUS} = CONCLUÍDA',
            'column_id': 'STATUS'
        },
        'backgroundColor': 'PaleGreen',
        'color': 'black'
    },
    {
        'if': {
            'filter_query': '{STATUS} = ATRASADA',
            'column_id': 'STATUS'
        },
        'backgroundColor': 'DarkSalmon',
        'color': 'black'
    },
    {
        'if': {
            'filter_query': '{STATUS} = "A INICIAR"',
            'column_id': 'STATUS'
        },
        'backgroundColor': 'Gainsboro',
        'color': 'black'
    },
    {
        'if': {
            'filter_query': '{STATUS} = "EM ANDAMENTO"',
            'column_id': 'STATUS'
        },
        'backgroundColor': 'LightSkyBlue',
        'color': 'black'
    }
]
datas_cols = ['PREV. INÍCIO', 'PREVISÃO TÉRM.',
              'INÍCIO EXEC.', 'FIM EXEC.']
colunas = ['N', 'TAREFA', 'RESP.',
           'STATUS', 'PREV. INÍCIO', 'PREVISÃO TÉRM.',
           'INÍCIO EXEC.', 'FIM EXEC.', 'OBSERVAÇÕES']


def ajusta_df(df):
    df.rename(columns={"REPONSÁVEL PELA TAREFA": "RESP.",
                           "TAREFA SEQUÊNCIA": "N",
                           "PREV. REPACTUADA DE INÍCIO": "PREV. INÍCIO",
                           "PREV. REPACTUADA DE TÉRMINO": "PREVISÃO TÉRM.",
                           "INÍCIO EXECUÇÃO": "INÍCIO EXEC.",
                           "FIM EXECUÇÃO": "FIM EXEC."}, inplace=True)

    for col in datas_cols:
        df[col] = df[col].dt.strftime("%d/%m/%y")

    return df


def tabela(df):
    records = df.to_dict("records")
    stl_cell_cond_cols = [
        "N",
        "RESP.",
        "STATUS",
        "PREV. INÍCIO",
        "PREVISÃO TÉRM.",
        "INÍCIO EXEC.",
        "FIM EXEC."
    ]
    return dash_table.DataTable(
        id="table",
        columns=[{"name": i, "id": i} for i in colunas],
        data=records,
        tooltip_data=[{
            'PREV. INÍCIO': {
                'value': f"1a. previsão de início **{row['PREVISÃO DE INÍCIO'].strftime('%d/%m/%Y')}**",
                'type': 'markdown'},
            'PREVISÃO TÉRM.': {
                'value': f"1a. previsão de término **{row['PREVISÃO DE TÉRMINO'].strftime('%d/%m/%Y')}**",
                'type': 'markdown'},
        } for row in records],
        css=[{
            'selector':
                '.dash-table-tooltip',
            'rule':
                'background-color: grey; '
                'font-family: sans-serif; '
                'color: white'
        }],
        fixed_rows={"headers": True},
        style_table={"overflowX": "auto", "overflowY": "auto"},
        style_header={
            "backgroundColor": "rgb(230, 230, 230)",
            "fontWeight": "bold"
        },
        style_cell_conditional=[
                                   {
                                       "if": {"column_id": c},
                                       "textAlign": "left",
                                   } for c in ["TAREFA", "OBSERVAÇÕES"]
                               ] +
                               [
                                   {
                                       "if": {"column_id": c},
                                       "width": 45,
                                       "textAlign": "center"
                                   } for c in stl_cell_cond_cols
                               ],
        style_cell={
            "font_family": "sans-serif",
            # "textAlign": "left",
            "padding": "7px",
            "height": "auto",
            "whiteSpace": "normal",
            "minWidth": 35, "width": 135},
        style_data_conditional=status_cores,
    )


def gera_tabela(cd_obj):
    infos_obj = data.info_objetivo(cod_obj=cd_obj)

    nm_obj = infos_obj["objetivo"]

    df_obj = infos_obj["tabela"]
    df_obj = ajusta_df(df_obj)

    acoes = df_obj.groupby(["AÇÃO"], sort=False)

    tab = [
        html.Div([
            html.H5(f"Ação: {nm}", style={"margin-top": 27}),
            tabela(tab)
        ])
        for nm, tab in acoes
    ]
    return nm_obj, tab
