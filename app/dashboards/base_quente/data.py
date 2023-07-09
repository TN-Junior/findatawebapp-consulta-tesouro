import pandas as pd

ARQUIVO = "app/dashboards/_datasets/base_quente/dam_pago.csv"


def base(rajada=False):
    df_ext = pd.read_csv(ARQUIVO, sep=";", decimal=".", thousands=",")
    df_ext['data'] = pd.to_datetime(df_ext['data'], format="%Y-%m-%d")
    df_ext.sort_values('data', inplace=True)

    # df sem rajada que será usada no dashboard
    if rajada:
        return df_ext
    return df_ext[df_ext.data < df_ext.data.max()]


def df_rajada():
    df = base(rajada=True)
    return df[df.data == df.data.max()]["receita"].sum()


def df_para_chart(rec_list):
    df = base()
    return df.query("cd_receita_local == @rec_list")


def df_sete_dias_uteis(df, timestamp):
    quinze_dias = pd.date_range(end=timestamp, periods=15, freq="D")
    sete_dias_uteis = df[df.data.isin(quinze_dias)
                        & df.dia_util == 1]['data'].unique()[-7:]
    return df[df.data.isin(sete_dias_uteis)]


def df_data_ref():
    df = base()
    return df.tail(1)


def mes_dia_ref():
    df_dt_ref = df_data_ref()
    mes_dia_num_ref = int(df_dt_ref['mes_dia_num'])
    return mes_dia_num_ref


def mes_num_ref():
    df_dt_ref = df_data_ref()
    return int(df_dt_ref['mes_num'])


def dia_ref():
    df_dt_ref = df_data_ref()
    return int(df_dt_ref['dia'])


def data_ref():
    df = base()
    return df.data.max()


def data_ref_str():
    return data_ref().strftime("%d/%m/%Y")


def data_arquivo():
    df = base()
    return df.data.max() + pd.DateOffset(days=1)


def data_arquivo_str():
    df = base()
    data = df.data.max() + pd.DateOffset(days=1)
    return data.strftime("%d/%m")


def data_ref_ano_anterior():
    return data_arquivo().strftime("%d/%m")


def dicionario():
    df = base()
    return df[
        ["cd_receita_local", "atribuicao", "data",
         "cd_nm_receita", "receita_contabil"]
    ].drop_duplicates().sort_values("cd_receita_local")


def input_para_rec_local(input_list):
    dic_receita = dicionario()
    query_list = list()
    cols = ["atribuicao", "receita_contabil", "cd_nm_receita"]
    for arg, col in zip(input_list, cols):
        if arg is not None and arg != []:
            query_list.append(f"{col} == {arg}")
    try:
        query = ' & '.join(query_list)
        result = dic_receita.query(query).index.to_list()
    except ValueError:
        result = dic_receita.index.to_list()
    return result


def filtra_base(calendario, atribuicao=None, grupo=None, receita_local=None):

    df = base()

    if calendario is not None:
        dt_ini, dt_fim = calendario

        df.query(
            "data >= @dt_ini and data <= @dt_fim",
            inplace=True
        )

    cols = {
        "atribuicao": atribuicao,
        "receita_contabil": grupo,
        "cd_nm_receita": receita_local
    }

    query_list = list()
    for col, arg in cols.items():
        if arg is not None and arg != []:
            query_list.append(f"{col} == {arg}")

    try:
        query = ' & '.join(query_list)
        return df.query(query)
    except ValueError:
        return df
