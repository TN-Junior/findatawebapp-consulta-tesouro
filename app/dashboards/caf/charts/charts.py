import plotly.graph_objects as go
from plotly.subplots import make_subplots


def combo_chart(title, name_line, bar_name, idx, val_line, val_bar):
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(
            name=name_line,
            x=idx,
            y=val_line,
            hovertemplate="R$%{y:,.2f}",
            texttemplate="R$%{y:,.2f}",
            line=dict(color="indianred", width=3)
        ), secondary_y=True)

    fig.add_trace(
        go.Bar(
            name=bar_name,
            x=idx,
            y=val_bar,
            texttemplate="%{y}",
            textposition="outside",
            marker_color="#36739a",
        ), secondary_y=False)

    fig.update_layout(
        title_text=title,
        legend=dict(
            orientation="h"
        ),
        xaxis=dict(
            tickformat="d",
            tickvals=idx.unique(),
            tickangle=30,
        ),
        yaxis=dict(
            showgrid=False
        ),
        # paper_bgcolor="rgb(248, 248, 255)",
        plot_bgcolor="rgb(248, 248, 255)",
        margin=dict(l=50, r=50, b=20, t=20),
    )

    fig.update_yaxes(title_text=bar_name, secondary_y=False)
    fig.update_yaxes(title_text=name_line, secondary_y=True)
    return fig


def stacked_bar(y_axis_name, pre, apos, money_values=False):
    fig = go.Figure(data=[
        go.Bar(
            name="Até 2016",
            y=y_axis_name,
            x=[pre],
            marker=dict(
                color='rgba(60, 114, 196, 0.8)',
                line=dict(color='rgb(248, 248, 249)', width=1)
            ),
            hovertemplate=f'{pre:,.0f}',
            orientation="h"
        ),
        go.Bar(
            name="Pós 2016",
            y=y_axis_name,
            x=[apos],
            marker=dict(
                color='rgba(112, 173, 71, 0.8)',
                line=dict(color='rgb(248, 248, 249)', width=1)
            ),
            hovertemplate=f'{apos:,.0f}',
            orientation="h")
    ])

    fig.update_layout(
        xaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
            domain=[0.15, 1]
        ),
        yaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
        ),
        barmode='stack',
        paper_bgcolor='rgb(248, 248, 255)',
        plot_bgcolor='rgb(248, 248, 255)',
        margin=dict(l=50, r=50, b=0, t=40, pad=0),
        height=75,
        showlegend=False,
    )

    fig.update_layout(
        annotations=[
            dict(xref='paper',
                 yref='y',
                 x=0.14,
                 y=0.00,
                 xanchor='right',
                 text=y_axis_name[0],
                 font=dict(family='Arial', size=12,
                           color='rgb(67, 67, 67)'),
                 showarrow=False,
                 align='right'),
            dict(xref='x',
                 yref='y',
                 x=pre / 2,
                 y=0.00,
                 text=f"{pre:,.0f}" if money_values else str(pre),
                 font=dict(family='Arial', size=12,
                           color='rgb(248, 248, 255)'),
                 showarrow=False),
            dict(xref='x',
                 yref='paper',
                 x=pre / 2,
                 y=1.5,
                 text="Pré 2016",
                 font=dict(family='Arial', size=12,
                           color='rgb(67, 67, 67)'),
                 showarrow=False)
            ,
            dict(xref='x',
                 yref='y',
                 x=pre + (apos / 2),
                 y=0.0,
                 text=f"{apos:,.0f}" if money_values else str(apos),
                 font=dict(family='Arial', size=12,
                           color='rgb(248, 248, 255)'),
                 showarrow=False),
            dict(xref='x',
                 yref='paper',
                 x=pre + (apos / 2),
                 y=1.5,
                 text="Pós 2016",
                 font=dict(family='Arial', size=12,
                           color='rgb(67, 67, 67)'),
                 showarrow=False)
        ]
    )
    return fig


def dot_line(x1, y1, x2, y2, height):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=x1,
        y=y1,
        marker=dict(color="white", size=5,
                    line=dict(color="DarkSlateGrey", width=1)),
        mode="markers",
        name="Data Lavratura",
    ))

    fig.add_trace(go.Scatter(
        x=x2,
        y=y2,
        marker=dict(color="rgba(156, 165, 196, 0.95)", size=5,
                    line=dict(color="DarkSlateGrey", width=1)),
        mode="markers",
        name="Data Situação Atual",
    ))

    fig.update_layout(
        yaxis=dict(
            tickfont=dict(size=10),
        ),
        xaxis=dict(
            side="top",
            showline=True,
            linecolor='rgb(102, 102, 102)',
        ),

        paper_bgcolor='rgb(248, 248, 255)',
        plot_bgcolor='rgb(248, 248, 255)',
        margin=dict(l=140, r=40, b=50, t=40),
        width=800,
        height=height,
        template="plotly_white",
    )
    return fig


def combo_and_stacked_bar(df):
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            name='Quit. + Parcel.',
            x=df.index.strftime('%b/%y'),
            y=df.Total,
            mode='lines+markers+text',
            textposition='top center',
            hovertemplate='R$%{y:,.2f}',
            texttemplate='%{y:,.0f}',
            line=dict(color='indianred', width=3),
        )
    )

    fig.add_trace(
        go.Bar(
            name='Quitado',
            x=df.index.strftime('%b/%y'),
            y=df.Quitado,
            hovertemplate='R$%{y:,.2f}',
            marker_color='#36739a',
        )
    )

    fig.add_trace(
        go.Bar(
            name='Parcelado',
            x=df.index.strftime('%b/%y'),
            y=df.Parcelado,
            hovertemplate='R$%{y:,.2f}',
            marker_color='#17becf',
        )
    )

    fig.update_layout(
        title_text='Linha do tempo - valores parcelados e quitados',
        # height=340,
        barmode='stack',
        font=dict(size=11, family='Arial'),
        yaxis=dict(showgrid=False, tickprefix='R$'),
        legend=dict(orientation='h'),
        plot_bgcolor='rgb(248, 248, 255)',
        margin=dict(l=0, r=0, t=50, b=0, pad=10),
    )
    return fig
