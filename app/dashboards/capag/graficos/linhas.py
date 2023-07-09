import plotly.graph_objects as go


def indicador(df, data_ref, *args):
    df_realiz = df.query("index <= @data_ref")
    df_prev = df.query("index >= @data_ref")
    fig = go.Figure([
        go.Scatter(name=args[2],
                   x=df_realiz.index.strftime("%b %Y"),
                   y=df_realiz[args[0]],
                   text=df_realiz[args[0]].round(2),
                   mode="lines+markers+text",
                   hovertemplate='%{y:,.1%}', texttemplate='%{y:,.0%}',
                   line=dict(color='#3366CC', width=2)
                   ),
        go.Scatter(name=args[3],
                   x=df_prev.index.strftime("%b %Y"),
                   y=df_prev[args[0]],
                   text=df_prev[args[0]].round(2),
                   mode="lines+markers+text",
                   hovertemplate='%{y:,.1%}', texttemplate='%{y:,.0%}',
                   line=dict(color='#636EFA', width=2, dash='dash')
                   )
    ])

    fig.update_layout(
        title=args[1],
        showlegend=False,
        yaxis_tickformat='0%'
    )

    fig.update_yaxes(rangemode="tozero")
    # fig.update_yaxes(range=[0.5, 1.7])
    fig.update_xaxes(
        tickangle=45
    )

    fig.update_traces(textposition='top center')

    return fig


def componentes(df, data_ref, *args):
    df_realiz = df.query("index <= @data_ref")
    df_prev = df.query("index >= @data_ref")
    fig = go.Figure([
        go.Scatter(name=args[3],
                   x=df_realiz.index,
                   y=df_realiz[args[0]],
                   hovertemplate='R$%{y:,.2f}',
                   line=dict(color='#1C8356', width=2)
                   ),
        go.Scatter(name=args[4],
                   x=df_prev.index,
                   y=df_prev[args[0]],
                   text=df_prev[args[0]],
                   hovertemplate='R$%{y:,.2f}',
                   line=dict(color='#1CBE4F', width=2, dash='dash')
                   ),
        go.Scatter(name=args[5],
                   x=df_realiz.index,
                   y=df_realiz[args[1]],
                   hovertemplate='R$%{y:,.2f}',
                   line=dict(color='#DC3912', width=2)
                   ),
        go.Scatter(name=args[6],
                   x=df_prev.index,
                   y=df_prev[args[1]],
                   text=df_prev[args[1]],
                   hovertemplate='R$%{y:,.2f}',
                   line=dict(color='#FB0D0D', width=2, dash='dash')
                   )
    ])

    fig.update_layout(
        title=args[2]
    )

    fig.update_yaxes(rangemode="tozero")
    # fig_pc.update_yaxes(range=[0.5, 1.7])
    fig.update_xaxes(tickangle=45)

    fig.update_traces(textposition='top center')

    return fig


def componentes_dc_rc(df, data_ref, *args):
    df_realiz = df.query("index <= @data_ref")
    fig = go.Figure([
        go.Scatter(name=args[3],
                   x=df_realiz.index.strftime("%b %Y"),
                   y=df_realiz[args[0]],
                   hovertemplate='R$%{y:,.2f}',
                   line=dict(color='#1C8356', width=2)
                   ),
        go.Scatter(name=args[4],
                   x=df_realiz.index.strftime("%b %Y"),
                   y=df_realiz[args[1]],
                   hovertemplate='R$%{y:,.2f}',
                   line=dict(color='#DC3912', width=2)
                   )
    ])

    fig.update_layout(
        title=args[2]
    )

    fig.update_yaxes(rangemode="tozero")
    # fig_pc.update_yaxes(range=[0.5, 1.7])
    fig.update_xaxes(
        type='category',
        tickangle=45
    )

    fig.update_traces(textposition='top center')

    return fig


def liq(df):
    fig = go.Figure([
        go.Scatter(name="Endividamento",
                   x=df.index,
                   y=df["Indicador de Liquidez"],
                   text=df["Indicador de Liquidez"],
                   mode="lines+markers+text",
                   hovertemplate='%{y:,.2%}',
                   texttemplate='%{y:,.2%}',
                   line=dict(color='#3366CC', width=2)
                   )
    ])

    fig.update_layout(
        title="Liquidez",
        showlegend=False,
        yaxis_tickformat='%'
    )
    fig.update_xaxes(nticks=df.shape[0])
    fig.update_xaxes(tickangle=45)
    fig.update_traces(textposition='top center')

    return fig


def cx_obg(df):
    fig = go.Figure([
        go.Scatter(name="Disp. Caixa",
                   x=df.index,
                   y=df["Disponbilidade de Caixa Bruto"],
                   hovertemplate='R$%{y:,.2f}',
                   line=dict(color='#1C8356', width=2)
                   ),
        go.Scatter(name="Obrig. Finaceiras",
                   x=df.index,
                   y=df["obg_finaceiras"],
                   hovertemplate='R$%{y:,.2f}',
                   line=dict(color='#DC3912', width=2)
                   )
    ])

    fig.update_layout(
        title="Obrigações Finaceiras x Dispon. de Caixa")

    fig.update_yaxes(rangemode="tozero")
    fig.update_xaxes(tickangle=45, nticks=df.shape[0])
    fig.update_traces(textposition='top center')

    return fig


def liquidez(df):
    ind = go.Figure([
        go.Scatter(
            x=df.index,
            y=df.ind_liquidez,
            mode="lines+markers+text",
            hovertemplate='%{y:,.1%}',
            texttemplate='%{y:,.0%}',
            textposition="bottom right",
            line=dict(color='#3366CC', width=2)
        )
    ])
    ind.update_layout(
        title="Liquidez",
        showlegend=False,
        yaxis_tickformat='0%'
    )
    ind.update_yaxes(rangemode="tozero")
    ind.update_xaxes(tickangle=45)

    comps = go.Figure([
        go.Scatter(
            name="Disp. Caixa",
            x=df.index,
            y=df.disp_caixa,
            mode="lines+markers",
            hovertemplate="R$%{y:,.2f}",
            line=dict(color="#1C8356", width=2)
        ),
        go.Scatter(
            name="Obrig. Financ.",
            x=df.index,
            y=df.obg_financeiras,
            mode="lines+markers",
            hovertemplate="R$%{y:,.2f}",
            line=dict(color="#DC3912", width=2)
        )
    ])
    comps.update_layout(
        title="Disponibilidade de Caixa x Obrigações Financeiras"
    )
    comps.update_yaxes(rangemode="tozero")
    comps.update_xaxes(tickangle=45)

    return ind, comps
