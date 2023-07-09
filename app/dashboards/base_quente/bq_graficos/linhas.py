import plotly.graph_objects as go


def linhas(titulo, df):
    traces = [
        go.Scatter(
            name=gr,
            hovertemplate='R$%{y:,.2f}',
            x=df.query(
                'receita_contabil == @gr'
            ).groupby('data').sum(numeric_only=True).index,
            y=df.query(
                'receita_contabil == @gr'
            ).groupby('data').sum(numeric_only=True).receita,
        )
        for gr in df.receita_contabil.unique()
    ]

    fig_daily = go.Figure(
        data=traces
    )
    fig_daily.update_layout(
        title=titulo
    )
    return fig_daily


def linhas_serie_completa(df):
    df_daily = df.groupby(['data', 'receita_contabil'], as_index=False)[
        'receita'
    ].sum()
    return linhas('Série diária', df_daily)
