import pandas as pd
import plotly.graph_objects as go

from app.dashboards.base_quente.data import df_sete_dias_uteis


def card(titulo, valor_atual, valor_anterior):
    if valor_anterior == 0:
        delta = None
    else:
        delta = {
            "reference": valor_anterior,
            "relative": True,
            "position": "bottom",
            "valueformat": ".1%",
            "font": {"size": 15}
        }

    fig = go.Figure()
    fig.add_trace(
        go.Indicator(
            name="lorem ipsum",
            mode="number+delta",
            title={"text": f"{titulo}", "font": {"size": 25}},
            value=valor_atual,
            number={'prefix': "R$", "valueformat": ",.2f",
                    "font": {"color": "black", "size": 25}},
            delta=delta
        )
    )
    fig.update_layout(
        # margin=dict(l=0, r=0, t=0, b=0),
        height=200,
    )
    return fig


def ytd_card(df):
    data_max = df.data.max()
    ano_ref = df.ano.max()

    data_anterior = df.data.max() - pd.DateOffset(years=1)
    ano_anterior = data_anterior.year

    valor_atual = df.query(
        "data <= @data_max and ano == @ano_ref")['receita'].sum()
    valor_anterior = df.query(
        "ano == @ano_anterior and data <= @data_anterior")['receita'].sum()

    return card(ano_ref, valor_atual, valor_anterior)


def mtd_card(df):
    dia_mes = df.data.max()
    inicio_mes = dia_mes - pd.offsets.MonthBegin(1)

    dia_mes_anterior = df.data.max() - pd.DateOffset(years=1)
    inicio_mes_anterior = dia_mes_anterior - pd.offsets.MonthBegin(1)

    df_mtd = df.query(
        "data >= @inicio_mes and data <= @dia_mes")['receita'].sum()
    df_mtd_anterior = df.query(
        "data >= @inicio_mes_anterior and data <= @dia_mes_anterior"
    )['receita'].sum()
    return card('No mês', df_mtd, df_mtd_anterior)


def wtd_card(df):
    data_ref = df.data.max()
    df_last7wd = df_sete_dias_uteis(df, data_ref)

    data_ref_previous_year = (df.data.max() - pd.DateOffset(years=1))
    df_last7wd_prev_year = df_sete_dias_uteis(df, data_ref_previous_year)

    return card(
        'Último 7 dias úteis',
        df_last7wd.receita.sum(),
        df_last7wd_prev_year.receita.sum()
    )
