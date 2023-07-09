from dash.dash_table import DataTable

LIGHT_BLUE = '#7385C1'
BLUE = '#134284'
GRAY1 = '#E6E6E6'
GRAY2 = '#F5F5F5'
FLOAT = {
    'locale': {'decimal': ',', 'group': '.'},
    'nully': '',
    'prefix': None,
    'specifier': ',.1f',
}


def formatacao_cabecalho(n):
    meses = [
        'Janeiro',
        'Fevereiro',
        'Março',
        'Abril',
        'Maio',
        'Junho',
        'Julho',
        'Agosto',
        'Setembro',
        'Outubro',
        'Novembro',
        'Dezembro',
    ]
    formatacao = [
        {
            'if': {'column_id': meses[n:]},
            'color': BLUE,
            'backgroundColor': 'white',
            'fontWeight': 'bold',
        },
        {
            'if': {'column_id': meses[:n]},
            'backgroundColor': GRAY1
        }
    ]
    return formatacao


def tab_liquidez(df, tabela_id):
    float_cols = [
        {'name': i, 'id': i, 'type': 'numeric', 'format': FLOAT}
        for i in df.columns
    ]

    bold_condition = (
        "{Fonte} = TOTAL || {Fonte} = 'RECURSOS NÃO VINCULADOS "
        "(I)' || {Fonte} = 'RECURSOS VINCULADOS (II)'"
    )

    tab = DataTable(
        id=tabela_id,
        columns=float_cols,
        data=df.to_dict('records'),
        export_format='xlsx',
        export_headers='display',
        style_as_list_view=True,
        fixed_rows={'headers': True},
        style_data_conditional=[
            {
                'if': {'filter_query': bold_condition},
                'backgroundColor': LIGHT_BLUE,
                'color': 'white',
                'fontSize': 13,
            },
        ],
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto',
            # 'backgroundColor': 'lavender'
        },
        style_header={
            'backgroundColor': GRAY1,
            'color': 'black',
            'fontWeight': 'bold',
            'fontSize': 13,
        },
        style_cell_conditional=[
            {
                'if': {'column_id': 'Fonte'},
                'backgroundColor': GRAY1,
                'textAlign': 'left',
            },
            {
                'if': {'column_id': 'Receitas'},
                'backgroundColor': GRAY2,
                'textAlign': 'left',
            },
        ],
        style_cell={
            'font_family': 'sans-serif',
            'fontSize': 12,
            'padding': '7px',
            'height': 'auto',
            'whiteSpace': 'normal',
            # 'width': 95,
            # 'minWidth': 90,
            'textAlign': 'center',
        },
    )
    return tab


def tab_previsao_pf_ggaf_rri(df, tabela_id, estilo_cabecalho, ano):
    float_cols = [
        {'name': i, 'id': i, 'type': 'numeric', 'format': FLOAT}
        for i in df.columns
    ]

    bold_condition = {
        'if': {
            'filter_query':
                '{Conta} = Transferência || '
                '{Conta} = Municipal || '
                '{Conta} = TOTAL'
        },
        'backgroundColor': LIGHT_BLUE,
        'color': 'white',
        'fontSize': 13,
    }

    tab = DataTable(
        id=tabela_id,
        columns=float_cols,
        data=df.to_dict('records'),
        export_format='xlsx',
        export_headers='display',
        style_as_list_view=True,
        fixed_rows={'headers': True},
        # style_table={"overflowX": "auto", "overflowY": "auto"},
        style_data_conditional=[bold_condition],
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto',
        },
        style_header_conditional=estilo_cabecalho,
        style_header={
            'backgroundColor': GRAY1,
            'color': 'black',
            # 'fontWeight': 'bold',
            'fontSize': 13,
        },
        style_cell_conditional=[
            {
                'if': {'column_id': 'Conta'},
                'backgroundColor': GRAY1,
                'textAlign': 'left',
            },
            {
                'if': {'column_id': f'{ano}'},
                'backgroundColor': GRAY1,
                'fontWeight': 'bold',
                'textAlign': 'right'
            }
        ],
        style_cell={
            'font_family': 'sans-serif',
            'fontSize': 12,
            'padding': '7px',
            'height': 'auto',
            'whiteSpace': 'normal',
            # 'width': 100,
            # 'minWidth': 95,
            'textAlign': 'center',
        },
    )
    return tab


def tab_previsao_rcl(df, tabela_id, estilo_cabecalho, ano):
    float_cols = [
        {'name': i, 'id': i, 'type': 'numeric', 'format': FLOAT}
        for i in df.columns
    ]

    receitas_condition = (
        "{Conta} = 'RECEITA CORRENTE AJUSTADA (RCA) CAPAG' || "
        "{Conta} = 'RECEITA CORRENTE LÍQUIDA (III) = (I - II)' || "
        "{Conta} = 'RECEITAS CORRENTES (I)' || "
        "{Conta} = 'DEDUÇÕES (II)' || "
        "{Conta} = 'RECEITAS CORRENTES INTRAORÇAMENTÁRIAS'"
    )

    contas_condition = (
        "{Conta} = 'IMPOSTOS, TAXAS E CONTRIB. DE MELHORIA' || "
        "{Conta} = 'CONTRIBUIÇÕES' || "
        "{Conta} = 'RECEITAS PATRIMONIAL' || "
        "{Conta} = 'RECEITAS DE SERVIÇOS' || "
        "{Conta} = 'TRANSFERÊNCIAS CORRENTES' || "
        "{Conta} = 'OUTRAS RECEITAS CORRENTES'"
    )

    tab = DataTable(
        id=tabela_id,
        columns=float_cols,
        data=df.to_dict('records'),
        export_format='xlsx',
        export_headers='display',
        style_as_list_view=True,
        fixed_rows={'headers': True},
        # style_table={"overflowX": "auto", "overflowY": "auto"},
        style_data_conditional=[
            {
                'if': {'filter_query': receitas_condition},
                'backgroundColor': LIGHT_BLUE,
                'color': 'white',
                'fontSize': 13
            },
            {
                'if': {'filter_query': contas_condition},
                'backgroundColor': GRAY1
            },
        ],
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto',
        },
        style_header_conditional=estilo_cabecalho,
        style_header={
            'backgroundColor': GRAY1,
            'color': 'black',
            'fontWeight': 'bold',
            'fontSize': 13,
        },
        style_cell_conditional=[
            {
                'if': {'column_id': 'Conta'},
                'textAlign': 'left'
            },
            {
                'if': {'column_id': f'{ano}'},
                'backgroundColor': GRAY1,
                'fontWeight': 'bold',
                'textAlign': 'right'
            }
        ],
        style_cell={
            'font_family': 'sans-serif',
            'fontSize': 12,
            'padding': '7px',
            'height': 'auto',
            'whiteSpace': 'normal',
            # 'width': 95,
            # 'minWidth': 90,
            'textAlign': 'center',
        },
    )
    return tab


def tab_exemplo(ano):
    table = DataTable(
        columns=[
            {'name': ["", 'Conta'], 'id': 'conta'},
            {'name': ['Realizado', 'Jan'], 'id': 'r'},
            {'name': ['Realizado', 'Fev'], 'id': 'r'},
            {'name': ['Previsto', 'Mar'], 'id': 'p'},
            {'name': ['Previsto', 'Abr'], 'id': 'p'},
            {'name': ["", f'{ano}'], 'id': f'{ano}'},
        ],
        data=[
            {
                'conta': 'Nome da conta',
                'r': 'Valor Realizado',
                'p': 'Valor Previsto',
                f'{ano}': 'Valor Total'
            }
        ],
        style_header_conditional=[
            {
                'if': {'column_id': 'p', 'header_index': 1},
                'color': BLUE,
                'backgroundColor': 'white',
                'fontWeight': 'bold',
            },
            {
                'if': {'column_id': 'r', 'header_index': 1},
                'backgroundColor': GRAY1
            },
            {
                'if': {'column_id': 'conta', 'header_index': 1},
                'backgroundColor': GRAY1
            },
            {
                'if': {'column_id': f'{ano}'},
                'backgroundColor': GRAY1
            }
        ],
        style_header={
            'color': 'black',
            'fontSize': 13,
        },
        merge_duplicate_headers=True,
        style_cell={
            'font_family': 'sans-serif',
            'fontSize': 12,
            'padding': '7px',
            'height': 'auto',
            'whiteSpace': 'normal',
            'textAlign': 'center',
        },
    )
    return table
