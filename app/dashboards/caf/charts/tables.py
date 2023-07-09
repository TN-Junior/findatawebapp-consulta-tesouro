from dash.dash_table import DataTable
from app.dashboards.caf.data import df_contagem_por_datasets

MONEY = {
    'locale': {'decimal': ',', 'symbol': ['R$', ''], 'group': '.'},
    'nully': '',
    'prefix': None,
    'specifier': '$,.2f'
}
PERCENT = {
    'locale': {'decimal': ','},
    'nully': '',
    'prefix': None,
    'specifier': ',.2%'
}
FLOAT = {
    'locale': {'group': '.'},
    'nully': '',
    'prefix': None,
    'specifier': ',.0f'
}


def tab_razao_social(df):
    table = DataTable(
        id="tab-razao-social",
        columns=[
            {"name": "Cód", "id": "Cód"},
            {"name": "Razão Social", "id": "Razão Social"},
            {"name": "Lavratura", "id": "Lavratura"},
            {"name": "Últ. moviment.", "id": "Últ. moviment."},
            {"name": "Valor", "id": "Valor", "type": "numeric",
             "format": MONEY},
            {"name": "Duração (média, em dias)",
             "id": "Duração (média, em dias)",
             "type": "numeric", "format": FLOAT},
        ],
        page_current=0,
        page_size=25,
        data=df.to_dict('records'),
        style_as_list_view=True,
        sort_action="native",
        fixed_rows={"headers": True},
        style_table={"overflowY": "auto"},
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 255)',
            }
        ],
        style_data={
            'color': 'black',
            'backgroundColor': 'white'
        },
        style_header={
            "backgroundColor": "rgb(230, 230, 230)",
            'color': 'black',
            "fontWeight": "bold",
        },
        style_cell={
            "font_family": "sans-serif",
            "fontSize": 11,
            "padding": "7px",
            "height": "auto",
            "whiteSpace": "normal",
            "width": 135,
            "minWidth": 35,
            'textAlign': 'left'
        },
    )
    return table


def tab_ranking(df):
    table = DataTable(
        id="tab-ranking",
        columns=[
            {"name": "Situação Atual", "id": "Situação Atual"},
            {"name": "% de Process.", "id": "% de Process.", "type": "numeric",
             "format": PERCENT},
            {"name": "Qtd Process.", "id": "Qtd Process.", "type": "numeric"},
            {"name": "Valor", "id": "Valor", "type": "numeric",
             "format": MONEY}
        ],
        data=df.to_dict('records'),
        style_as_list_view=True,
        sort_action="native",
        fixed_rows={"headers": True},
        style_table={"overflowY": "auto"},
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 255)',
            }
        ],
        style_data={
            'color': 'black',
            'backgroundColor': 'white'
        },
        style_header={
            "backgroundColor": "rgb(230, 230, 230)",
            'color': 'black',
            "fontWeight": "bold"
        },
        style_cell={
            "font_family": "sans-serif",
            "fontSize": 11,
            "padding": "7px",
            "height": "auto",
            "whiteSpace": "normal",
            "minWidth": 60,
            "textAlign": "left",
        },
    )
    return table


def tab_resultado(df):
    table = DataTable(
        id="tab-resultado",
        columns=[
            {"name": "Resultado", "id": "Resultado"},
            {"name": "Qtd Process.", "id": "Qtd Process.", "type": "numeric"},
            {"name": "Valor", "id": "Valor", "type": "numeric", "format":
                MONEY},
            {"name": "Duração (média, em dias)", "id": "Duração (média, "
                                                       "em dias)",
             "type": "numeric", "format": FLOAT},
        ],
        data=df.to_dict('records'),
        style_as_list_view=True,
        sort_action="native",
        fixed_rows={"headers": True},
        style_table={"overflowY": "auto"},
        style_data={
            'color': 'black',
            'backgroundColor': 'white'
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 255)',
            }
        ],
        style_header={
            "backgroundColor": "rgb(230, 230, 230)",
            'color': 'black',
            "fontWeight": "bold"
        },
        style_cell_conditional=[
            {
                "if": {"column_id": "Resultado"},
                "textAlign": "left",
            }
        ],
        style_cell={
            "font_family": "sans-serif",
            "fontSize": 11,
            "padding": "7px",
            "height": "auto",
            "whiteSpace": "normal",
            "width": 135,
            "minWidth": 35
        },
    )
    return table


def tab_contagem_por_datasets(df, agg):
    df = df_contagem_por_datasets(df, agg=agg)
    cols = [
        {"name": "Instância", "id": "Instância"},
        {"name": "Resultado", "id": "Resultado"},
    ]

    if agg == "cd_processo":
        cols_vals = [{"name": col, "id": col} for col in df.columns]
    else:
        cols_vals = [
            {"name": col, "id": col, "type": "numeric", "format": MONEY}
            for col in df.columns
        ]

    columns = cols + cols_vals

    df.reset_index(inplace=True)

    table = DataTable(
        id="tab-contagem-por-dataset",
        columns=columns,
        data=df.to_dict('records'),
        export_format='xlsx',
        style_as_list_view=True,
        fixed_rows={"headers": True},
        style_table={"overflowY": "auto"},
        style_data={
            'color': 'black',
            'backgroundColor': 'white'
        },
        style_data_conditional=[
            {
                'if': {'row_index': [2, 5, 7, 8]},
                'backgroundColor': 'rgb(248, 248, 255)',
            }
        ],
        style_header={
            "backgroundColor": "rgb(230, 230, 230)",
            'color': 'black',
            "fontWeight": "bold"
        },
        style_cell={
            "font_family": "sans-serif",
            "textAlign": "left",
            "fontSize": 11,
            "padding": "7px",
            "height": "auto",
            "whiteSpace": "normal",
            "width": 95,
            "minWidth": 55
        },
    )
    return table


def tab_rs_quitado_parcelado(df):
    columns = [
        {"name": "Razão Social", "id": "Razão Social"},
        {"name": "Sit. Débito", "id": "Sit. Débito"},
        {"name": df.columns[-1], "id": df.columns[-1],
         "type": "numeric", "format": MONEY},
    ]

    table = DataTable(
        id="tab-rs-quitado-parcelado",
        columns=columns,
        data=df.to_dict('records'),
        page_current=0,
        page_size=10,
        style_as_list_view=True,
        fixed_rows={"headers": True},
        style_data={
            'color': 'black',
            'backgroundColor': 'white'
        },
        style_header={
            "backgroundColor": "rgb(230, 230, 230)",
            "color": "black",
            "fontWeight": "bold"
        },
        style_cell_conditional=[
            {
                "if": {"column_id": df.columns[-1]},
                "textAlign": "right",
            }
        ],
        style_cell={
            "font_family": "sans-serif",
            "textAlign": "left",
            "fontSize": 10,
            "padding": "px",
            "height": "auto",
            "whiteSpace": "normal",
            "width": 35
        },
    )

    return table
