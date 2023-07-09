import pandas as pd

REGIOES = {
    1100205: "Norte",
    1200401: "Norte",
    1302603: "Norte",
    1400100: "Norte",
    1501402: "Norte",
    1600303: "Norte",
    1721000: "Norte",
    2111300: "Nordeste",
    2211001: "Nordeste",
    2304400: "Nordeste",
    2408102: "Nordeste",
    2507507: "Nordeste",
    2611606: "Nordeste",
    2704302: "Nordeste",
    2800308: "Nordeste",
    2927408: "Nordeste",
    3106200: "Sudeste",
    3205309: "Sudeste",
    3304557: "Sudeste",
    3550308: "Sudeste",
    4106902: "Sul",
    4205407: "Sul",
    4314902: "Sul",
    5002704: "Centro-Oeste",
    5103403: "Centro-Oeste",
    5208707: "Centro-Oeste",
    53: "Centro-Oeste"
}

# importa a base de dados
arquivo = "app/dashboards/_datasets/stn/rreo_anexo3_stn.parquet.gzip"
df = pd.read_parquet(arquivo)
df = df.assign(regiao=df.cod_completo.map(REGIOES))
ano_max = df.ano.max()


# constroi tabela com série histórica de Recife
def serie_historica_recife_barras(data_agregacao, conta, ano, bimestre, mes):
    if data_agregacao == 'ano':
        ano = [2015, ano_max]

    dict_agregacao = {
        'ano': 'ano',
        'mes_ano': ['ano', 'mes_ano'],
        'ano_bimestre': ['ano', 'ano_bimestre']
    }

    intervalo_ano = list(range(ano[0], ano[1] + 1))
    intervalo_bimestre = list(range(bimestre[0], bimestre[1] + 1))
    intervalo_mes = list(range(mes[0], mes[1] + 1))

    query = "nome_municipio == 'Recife' and " \
            "conta == @conta and " \
            "ano == @intervalo_ano and " \
            "bimestre == @intervalo_bimestre and " \
            "mes_num == @intervalo_mes "

    df_rec_iptu = df.query(query)
    df_serie_historica_recife = df_rec_iptu.groupby(
        dict_agregacao[data_agregacao], sort=False, as_index=False).agg(
        {'valor': 'sum', 'populacao': 'mean', 'valor_deflac': 'sum'})

    df_serie_historica_recife['per_capita'] = df_serie_historica_recife[
                                                  'valor'] / \
                                              df_serie_historica_recife[
                                                  'populacao']

    df_serie_historica_recife['var_pct_valor'] = df_serie_historica_recife[
        'valor'].pct_change()
    df_serie_historica_recife['var_pct_per_capita'] = \
        df_serie_historica_recife['per_capita'].pct_change()

    return df_serie_historica_recife


def serie_historica_recife_linhas(data_agregacao, conta, ano, bimestre, mes):
    ano = [2015, ano_max]

    dict_agregacao = {
        'ano': 'ano',
        'mes_ano': ['ano', 'mes'],
        'ano_bimestre': ['ano', 'bimestre']
    }

    intervalo_ano = list(range(ano[0], ano[1] + 1))
    intervalo_bimestre = list(range(bimestre[0], bimestre[1] + 1))
    intervalo_mes = list(range(mes[0], mes[1] + 1))

    query = "nome_municipio == 'Recife' and " \
            "conta == @conta and " \
            "ano == @intervalo_ano and " \
            "bimestre == @intervalo_bimestre and " \
            "mes_num == @intervalo_mes "

    df_rec_iptu = df.query(query)
    df_serie_historica_recife = df_rec_iptu.groupby(
        dict_agregacao[data_agregacao], sort=False, as_index=False).agg(
        {'valor': 'sum', 'populacao': 'mean', 'valor_deflac': 'sum'})
    df_serie_historica_recife['per_capita'] = df_serie_historica_recife[
                                                  'valor'] / \
                                              df_serie_historica_recife[
                                                  'populacao']

    df_serie_historica_recife['var_pct_valor'] = df_serie_historica_recife[
        'valor'].pct_change()
    df_serie_historica_recife['var_pct_per_capita'] = \
        df_serie_historica_recife['per_capita'].pct_change()
    df_serie_historica_recife['var_pct_deflac'] =  \
        df_serie_historica_recife['valor_deflac'].pct_change()

    return df_serie_historica_recife


def ranking_capitais(conta, ano, bimestre, mes, regiao):
    if len(ano) == 1:
        ano_max = max(ano)
        ano_anterior = ano_max - 1
        lista_anos = [ano_anterior, ano_max]
    elif len(ano) > 1:
        lista_anos = sorted(ano)[-2:]
    else:
        lista_anos = sorted(df.ano.unique())[-2:]

    intervalo_bimestre = list(range(bimestre[0], bimestre[1] + 1))
    intervalo_mes = list(range(mes[0], mes[1] + 1))

    query = "conta == @conta and " \
        "ano == @lista_anos and " \
        "bimestre == @intervalo_bimestre and " \
        "mes_num == @intervalo_mes "

    if regiao is not None:
        query_regiao = "and regiao == @regiao "
        query = query + query_regiao

    df_anos_filtrados = df.query(query)

    df_grp_capitais_ano = df_anos_filtrados.groupby(
        ['nome_municipio', 'ano'], as_index=False).agg(
        {'valor': 'sum', 'populacao': 'mean', 'valor_deflac': 'sum'})

    assert (len(df_grp_capitais_ano.ano.unique()) >= 2), \
        "Não há valores suficientes para realizar a variação."

    df_pivot = df_grp_capitais_ano.pivot_table(
        index='nome_municipio',
        columns='ano',
        aggfunc='sum'
    )

    df_pivot['per_capita_ano_max'] = df_pivot[('valor', lista_anos[1])] / \
                                     df_pivot[('populacao', lista_anos[1])]

    coluna_ano_max = df_pivot[('valor', lista_anos[1])]
    coluna_ano_anterior = df_pivot[('valor', lista_anos[0])]

    df_pivot['var_pct'] = (coluna_ano_max / coluna_ano_anterior) - 1

    coluna_ano_max_deflac = df_pivot[('valor_deflac', lista_anos[1])]
    coluna_ano_anterior_deflac = df_pivot[('valor_deflac', lista_anos[0])]

    df_pivot['var_pct_deflac'] = (coluna_ano_max_deflac / coluna_ano_anterior_deflac) - 1

    return df_pivot


def df_receita_para_mapa(data_agregacao, conta, ano, bimestre, mes, regiao):
    dict_agregacao = {
        'ano': ['ano', 'cd_municipio', 'conta'],
        'mes_ano': ['ano', 'mes_ano', 'mes_num', 'cd_municipio', 'conta'],
        'ano_bimestre': ['ano', 'ano_bimestre', 'bimestre',
                         'cd_municipio', 'conta']
    }

    intervalo_ano = list(range(ano[0], ano[1] + 1))
    intervalo_bimestre = list(range(bimestre[0], bimestre[1] + 1))
    intervalo_mes = list(range(mes[0], mes[1] + 1))

    query = "conta == @conta and " \
            "ano == @intervalo_ano and " \
            "bimestre == @intervalo_bimestre and " \
            "mes_num == @intervalo_mes "

    if regiao is not None:
        query_regiao = "and regiao == @regiao "
        query = query + query_regiao

    df_rec = df.query(query).assign(valor=df.valor.abs())

    df_serie_historica = df_rec.groupby(
        dict_agregacao[data_agregacao], sort=False, as_index=False).agg(
        {'valor': 'sum', 'populacao': 'mean'})

    df_serie_historica['per_capita'] = df_serie_historica['valor'] / \
                                       df_serie_historica['populacao']

    ano_max = df_serie_historica.ano.max()
    df_serie_historica.query("ano == @ano_max", inplace=True)

    if data_agregacao == 'ano_bimestre':
        bimestre_max = df_serie_historica.bimestre.max()
        df_serie_historica.query("bimestre == @bimestre_max", inplace=True)

    if data_agregacao == 'mes_ano':
        mes_max = df_serie_historica.mes_num.max()
        df_serie_historica.query("mes_num == @mes_max", inplace=True)

    return df_serie_historica


def df_geo():
    geo_files = "app/dashboards/_datasets/stn/geoloc_capitais.gzip"
    df_geo_files = pd.read_parquet(geo_files)
    return df_geo_files
