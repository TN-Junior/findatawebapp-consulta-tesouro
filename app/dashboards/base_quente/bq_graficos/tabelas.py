import numpy as np
import pandas as pd

from dash.dash_table import DataTable, FormatTemplate

from app.dashboards.base_quente.bq_components.bq_dcc import alerta_tabela


def table(df_table, ano, ano_anterior):
    money = FormatTemplate.money(2)
    perc = FormatTemplate.percentage(2)

    table = DataTable(
        columns=[
            {'name': 'ATRIBUIÇÃO', 'id': 'Atribuição'},
            {'name': 'RECEITA', 'id': 'Receita'},
            {'name': 'Mês', 'id': 'Mês'},
            {'name': ano_anterior, 'id': ano_anterior, 'type': 'numeric', 'format': money},
            {'name': ano, 'id': ano, 'type': 'numeric', 'format': money},
            {'name': 'Var. %', 'id': 'Var. %', 'type': 'numeric',
             'format': perc}
        ],
        data=df_table.to_dict("records"),
        # page_size=40,  # paginação
        fixed_rows={'headers': True},
        style_table={'overflowX': 'auto', 'overflowY': 'auto'},
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        },
        style_cell={
            'font_family': 'sans-serif',
            'height': 'auto',
            'minWidth': 100, 'maxWidth': 200, 'width': 125},
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto',
            # 'backgroundColor': 'lavender'
        },
        style_data_conditional=
        [{
            'if': {
                'filter_query': '{Mês} = Total',
            },
            'backgroundColor': 'rgb(246, 246, 246)'
        }] +
        [{
            'if': {
                'filter_query': '{Var. %} >= 0',
                'column_id': 'Var. %'
            },
            'fontWeight': 'bold',
            'color': 'green'
        }] +
        [{
            'if': {
                'filter_query': '{Var. %} < 0',
                'column_id': 'Var. %'
            },
            'color': 'red'
        }]
    )
    return table


def tab_por_mes(df):
    meses = {"Total": "Total", 1: "jan", 2: "fev", 3: "mar", 4: "abr",
             5: "mai", 6: "jun", 7: "jul", 8: "ago", 9: "set",
             10: "out", 11: "nov", 12: "dez"}

    dt_max = df.data.max()

    ano = dt_max.year
    ano_anterior = ano - 1

    mes_dia_num = df.query("data == @dt_max")['mes_dia_num'].unique()[0]
    df_ytd = df.query("ano >= @ano_anterior & mes_dia_num <= @mes_dia_num")

    anos = [ano, ano_anterior]
    try:
        tables = list()
        for ano in anos:
            pivot = pd.pivot_table(
                df_ytd.query("ano == @ano"),
                values=["receita"],
                index=["atribuicao", "receita_grupo2"],
                columns=["mes_num"],
                aggfunc=np.sum,
                margins=True,
                margins_name="Total"
            )
            pivot = pivot.stack("mes_num")
            pivot.columns = [str(ano)]
            tables.append(pivot)
    except ValueError:
        return alerta_tabela

    df_table2 = pd.concat(tables, axis=1)

    ano, ano_anterior = df_table2.columns
    df_table2 = df_table2.assign(
        col=(df_table2[ano] / df_table2[ano_anterior]) - 1)

    df_table2.reset_index(inplace=True)
    df_table2 = df_table2.assign(mes=df_table2["mes_num"].map(meses))
    df_table2 = df_table2[["atribuicao", "receita_grupo2", "mes",
                           "mes_num", str(ano), str(ano_anterior), "col"]]
    df_table2.columns = ["Atribuição", "Receita", "Mês",
                         "mes_num", ano, ano_anterior, "Var. %"]
    df_table2.drop("mes_num", axis=1, inplace=True)
    df_table2 = df_table2.query("Mês == 'Total' | Atribuição != 'Total'")

    return table(df_table2, ano, ano_anterior)
