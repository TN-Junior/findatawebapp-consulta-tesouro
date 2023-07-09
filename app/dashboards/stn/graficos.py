import plotly.graph_objects as go  # que cria os gráficos
import plotly.express as px


def grafico_barras(agregacao, df, formato):
    dict_formato = {
        'per_capita': dict(col='per_capita', texttemplate='%{y:,.1f}',
                           title_text='Recife - Receita Per Capita'),
        'valor_deflac': dict(col='valor_deflac', texttemplate='%{y:,.6s}',
                             title_text='Recife - Receita'),
        'valor': dict(col='valor', texttemplate='%{y:,.6s}',
                      title_text='Recife - Receita')
    }

    formato = dict_formato[formato]

    if agregacao == 'ano':
        x = df['ano']
        y = df[formato['col']]
    else:
        df_viz = df.groupby([agregacao], sort=False)[formato['col']].sum()
        x = df_viz.index
        y = df_viz

    fig = go.Figure(
        [
            go.Bar(
                x=x,
                y=y,
                texttemplate=formato['texttemplate'],
                textposition='inside',
                marker_color='SlateBlue'
            )
        ]
    )

    fig.update_layout(
        title_text=formato['title_text'],
        xaxis=dict(
            type='category',
            nticks=15,
            tickfont=dict(size=10),
            color='black'
        )
    )

    return fig


def grafico_linhas(agregacao, df, formato):
    if formato == 'per_capita':
        valor = 'var_pct_per_capita'
    elif formato == 'valor_deflac':
        valor = 'var_pct_deflac'
    elif formato == 'valor':
        valor = 'var_pct_valor'

    if agregacao == 'ano':
        x = df['ano'][1:]
        y = df[valor][1:]

        legend_title_text = None

        fig = go.Figure(
            [
                go.Scatter(
                    x=x,
                    y=y,
                    mode="lines+markers+text",
                    hovertemplate='%{y:,.1%}',
                    texttemplate='%{y:,.0%}',
                    textposition='bottom right',
                    line=dict(
                        color='SlateBlue'
                    )
                )
            ]
        )

    else:
        dict_agregacao = {
            'mes_ano': 'mes',
            'ano_bimestre': 'bimestre'
        }
        col_agreg = dict_agregacao[agregacao]
        legend_title_text = 'Bimestre' if col_agreg == 'bimestre' else 'Mês'

        fig = go.Figure()

        for agreg in df[col_agreg].unique():
            x = df[df[col_agreg] == agreg]['ano']
            y = df[df[col_agreg] == agreg][valor]
            fig.add_trace(
                go.Scatter(
                    x=x,
                    y=y,
                    mode='lines+markers',
                    name=f'{agreg}'
                )
            )

    fig.update_layout(
        title=dict(
            text='Recife - Var. % da Receita',
            font=dict(
                size=16
            )
        ),
        font=dict(
            size=10
        ),
        legend_title_text=legend_title_text,
        xaxis=dict(
            tickformat="d",
            tickvals=x,
            color='black'
        ),
        yaxis_tickformat='.0%',
        margin=dict(pad=10),
    )

    return fig


def grafico_barras_ranking(df, formato, ano):
    ano_max = max(ano)
    ano_min = min(ano)

    if formato == 'per_capita':
        col = 'per_capita_ano_max'
        title_name = f'Receita Per Capita, {ano_max}'
        xaxis_tickformant = None
        texttemplate = "%{x:.1f}"
    elif formato == 'valor_deflac':
        col = 'var_pct_deflac',
        title_name = f'Ranking - Var. % entre capitais, {ano_min}/{ano_max} real'
        xaxis_tickformat = '.0%'
        texttemplate = "%{x:.0%}"
    elif formato == 'valor':
        col = 'var_pct'
        title_name = f'Ranking - Var. % entre capitais, {ano_min}/{ano_max}'
        xaxis_tickformat = '.0%'
        texttemplate = "%{x:.0%}"

    df.sort_values(col, ascending=True, inplace=True)
    colors = [
        'SlateBlue' if capital == 'Recife' else 'LightSkyBlue'
        for capital in df.index
    ]

    fig = go.Figure(
        [
            go.Bar(
                x=df[col],
                y=df.index,
                orientation='h',
                texttemplate=texttemplate,
                # textposition='outside',
                marker_color=colors
            )
        ]
    )

    fig.update_layout(
        autosize=False,
        title=dict(
            text=title_name,
            font=dict(
                size=16
            )
        ),
        font=dict(
            size=10
        ),
        xaxis=dict(
            visible=True,
            showticklabels=True,
            tickformat='.1%'
        ),
        height=900,
        margin=dict(
            l=20,
            r=20,
            pad=5
        )
    )

    return fig


def mapa_capitais(agregacao, df_receita, df_geo_capitais):
    with open('app/dashboards/_datasets/stn/mapbox_token.txt', 'r') as f:
        token = f.readlines()

    df_geo_capitais = df_geo_capitais.replace(530010, 53)[
        ['X', 'Y', 'NAME', 'codmun1']
    ]. \
        rename(columns={'codmun1': 'cd_municipio'}). \
        merge(df_receita, on=['cd_municipio'])

    df_geo_capitais.rename(
        columns={
            'NAME': 'Capital',
            'ano': 'Ano',
            'conta': 'Conta',
            'ano_bimestre': 'Ano/Bimestre',
            'mes_ano': 'Mês/Ano',
            'valor': 'Receita (R$)',
            'per_capita': 'Rec. Per Cap. (R$)'
        }, inplace=True
    )

    hover_data = {
            'Conta': True,
            'X': False,
            'Y': False,
            # 'Receita (R$)': ':,.0f',
            # 'Var. %': ':,.0%',
            'Rec. Per Cap. (R$)': ':,.1f',
            # 'Var. % Rec. Per Cap.': ':,.0%'
        }

    if agregacao == 'ano':
        hover_data.update({'Ano': True,})
    elif agregacao == 'ano_bimestre':
        hover_data.update({'Ano/Bimestre': True})
    elif agregacao == 'mes_ano':
        hover_data.update({'Mês/Ano': True})

    fig = px.scatter_mapbox(
        df_geo_capitais,
        lat="Y",
        lon="X",
        hover_name='Capital',
        hover_data=hover_data,
        # color_discrete_sequence=["fuchsia"],
        zoom=3,
        height=700,
        size='Rec. Per Cap. (R$)'
    )

    fig.update_layout(
        mapbox_style='basic',
        mapbox_accesstoken=token[0],
        margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )

    return fig


def grafico_vazio_para_erro():
    fig = go.Figure(
        data=[
            go.Bar(x=[0], y=[0])
        ]
    )
    fig.update_layout(
        title=dict(
            text="<i>Ranking - Sem valores suficientes para produzir o "
                 "gráfico.</i>",
            font=dict(
                size=12
            )
        )
    )
    return fig