import plotly.graph_objects as go
import plotly.express as px

COR_PLOTLY = px.colors.qualitative.Plotly
COR_D3 = px.colors.qualitative.D3


def barras(titulo, df, cor=COR_D3[0]):
    fig_ytd = go.Figure(
        data=[
            go.Bar(  # name="Receita",
                x=df.index,
                y=df.values,
                name="",
                marker_color=cor,
                texttemplate='R$%{y:,.3s}', textposition='inside',
                hovertemplate='R$%{y:,.2f}')
        ]
    )
    fig_ytd.update_layout(
        autosize=False,
        title=titulo,
        # width=820,
        # height=420,
        barmode="group",
        uniformtext_minsize=6,
        xaxis={"tickformat": "d", "tickvals": df.index},
        yaxis={'categoryorder': 'total ascending', 'automargin': True}
    )
    return fig_ytd


def ytd_barras(df):
    dt_fim = df.data.max()
    data_ref = dt_fim.strftime("%d/%b")
    mes_dia_num = df.query("data == @dt_fim")['mes_dia_num'].unique()[0]

    df_ = df.query("mes_dia_num <= @mes_dia_num")
    df_ytd_gby = df_.groupby('ano')['receita'].sum()
    return barras(f"Série Anual (de 1/Jan a {data_ref}):", df_ytd_gby)


def mtd_barras(df):
    dt_fim = df.data.max()
    mes_num = dt_fim.month
    mes_dia_num = df.query("data == @dt_fim")['mes_dia_num'].unique()[0]

    mes_ref = dt_fim.strftime("%b")
    df_mtd = df.query("mes_num == @mes_num & mes_dia_num <= @mes_dia_num")
    df_mtd_gby = df_mtd.groupby('ano')['receita'].sum()
    return barras(f"No mês de {mes_ref}:", df_mtd_gby, cor=COR_PLOTLY[5])


def barras_por_tributo(titulo, df, ano, ano_anterior):
    data = [
        go.Bar(name=ano,
               x=df.loc[ano].values,
               y=df.loc[ano].index,
               texttemplate='R$%{x:,.5s}', textposition='inside',
               hovertemplate='R$%{x:,.2f}',
               marker_color=COR_PLOTLY[0],
               orientation='h'),
    ]

    try:
        barra_ano_anterior = go.Bar(
            name=ano_anterior,
            x=df.loc[ano_anterior].values,
            y=df.loc[ano_anterior].index,
            texttemplate='R$%{x:,.5s}',
            textposition='inside',
            hovertemplate='R$%{x:,.2f}',
            marker_color=COR_PLOTLY[4],
            orientation='h'
        )
        data.append(barra_ano_anterior)
    except KeyError:
        pass

    fig = go.Figure(
        data=data
    )
    fig.update_layout(
        title=titulo,
        # width=540,
        height=480,
        barmode="group",
        legend=dict(traceorder="reversed"),
        yaxis={'categoryorder': 'total ascending'}
    )
    return fig


def ytd_barras_por_tributo(df):
    # filtra ano
    dt_max = df.data.max()

    mes_dia_num = df.query("data == @dt_max")['mes_dia_num'].unique()[0]

    ano = dt_max.year
    ano_anterior = ano - 1
    ano_query = [ano, ano_anterior]

    df_ = df.query("ano == @ano_query")

    df_ytd = df_.query("mes_dia_num <= @mes_dia_num")
    df_ytd_gby = df_ytd.groupby(['ano', 'receita_contabil'])['receita'].sum()

    return barras_por_tributo("Acumulado do Ano", df_ytd_gby, ano,
                              ano_anterior)


def mtd_barras_por_tributo(df):
    # filtra ano
    dt_max = df.data.max()
    mes_num = dt_max.month
    mes_dia_num = df.query("data == @dt_max")['mes_dia_num'].unique()[0]

    ano = dt_max.year
    ano_anterior = ano - 1
    ano_query = [ano, ano_anterior]
    df_ = df.query("ano == @ano_query & mes_num == @mes_num")

    df_mtd = df_.query("mes_dia_num <= @mes_dia_num")
    df_mtd_gby = df_mtd.groupby(['ano', 'receita_contabil'])['receita'].sum()

    return barras_por_tributo("No mês", df_mtd_gby, ano, ano_anterior)
