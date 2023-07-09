from dash import Input, Output
from app.dashboards.stn.dataset import serie_historica_recife_barras, df_geo, \
    serie_historica_recife_linhas, ranking_capitais, df_receita_para_mapa
from app.dashboards.stn.graficos import grafico_barras, grafico_linhas, \
    grafico_barras_ranking, \
    mapa_capitais, grafico_vazio_para_erro


def callbacks(app):
    @app.callback(
        Output("grafico-barras-recife-valores", "figure"),
        Input("agregacao-radio", "value"),
        Input("conta-dropdown", "value"),
        Input("ano-slider", "value"),
        Input("bimestre-slider", "value"),
        Input("mes-slider", "value"),
        Input("formato-radio", "value")
    )
    def gera_grafico_barras_recife(
            agregracao, conta, ano, bimestre, mes, formato):

        df_viz = serie_historica_recife_barras(
            agregracao,
            conta,  # coluna conta
            ano,  # coluna ano
            bimestre,  # bimestre
            mes  # mês
        )

        fig = grafico_barras(agregracao, df_viz, formato)
        return fig

    @app.callback(
        Output("grafico-linhas-recife-valores", "figure"),
        Input("agregacao-radio", "value"),
        Input("conta-dropdown", "value"),
        Input("ano-slider", "value"),
        Input("bimestre-slider", "value"),
        Input("mes-slider", "value"),
        Input("formato-radio", "value")
    )
    def gera_grafico_linhas_recife(
            agregracao, conta, ano, bimestre, mes, formato):

        df_viz = serie_historica_recife_linhas(
            agregracao,
            conta,  # coluna conta
            ano,  # coluna ano
            bimestre,  # bimestre
            mes  # mês
        )

        fig = grafico_linhas(agregracao, df_viz, formato)
        return fig

    @app.callback(
        Output("grafico-barras-ranking-capitais", "figure"),
        Input("conta-dropdown", "value"),
        Input("ano-slider", "value"),
        Input("bimestre-slider", "value"),
        Input("mes-slider", "value"),
        Input("formato-radio", "value"),
        Input("regioes-dropdown", "value")
    )
    def gera_grafico_barras_ranking_capitais(
            conta, ano, bimestre, mes, formato, regiao):
        try:
            df_viz = ranking_capitais(conta, ano, bimestre, mes, regiao)
            fig = grafico_barras_ranking(df_viz, formato, ano)
            return fig
        except AssertionError as e:
            fig = grafico_vazio_para_erro()
            return fig

    @app.callback(
        Output("mapa-capitais", "figure"),
        Input("agregacao-radio", "value"),
        Input("conta-dropdown", "value"),
        Input("ano-slider", "value"),
        Input("bimestre-slider", "value"),
        Input("mes-slider", "value"),
        Input("regioes-dropdown", "value")
    )
    def mapa(agregracao, conta, ano, bimestre, mes, regiao):

        df_geo_receita = df_receita_para_mapa(
            agregracao, conta, ano, bimestre, mes, regiao)
        df_lat_lng_capitais = df_geo()
        fig = mapa_capitais(agregracao, df_geo_receita, df_lat_lng_capitais)
        return fig
