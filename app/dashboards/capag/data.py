import json
from datetime import datetime
import pandas as pd

pd.options.mode.chained_assignment = None

DIR = "app/dashboards/_datasets/capag/"


def _datas():
    arquivo = f"{DIR}/datas.json"
    with open(arquivo) as a:
        return json.load(a)


def ano_ref():
    datas = _datas()
    return datas["ano referencia"]


def data_ref():
    datas = _datas()
    return datas["data referencia"]


def data_ref_format():
    data = data_ref()
    return datetime.strptime(data, "%Y-%m").strftime("%b/%y")


def data_fim_ano():
    datas = _datas()
    return datas["data previsao"]


def data_fim_ano_format():
    data = data_fim_ano()
    return datetime.strptime(data, "%Y-%m").strftime("%b/%y")


def despesas():
    return pd.read_parquet(f'{DIR}desp_correntes.parquet.gzip')


def receitas():
    return pd.read_parquet(f'{DIR}rec_correntes.parquet.gzip')


def previsoes():
    df_rec_prev = pd.read_parquet(f'{DIR}rec_correntes_prev.parquet.gzip')
    df_desp_prev = pd.read_parquet(f'{DIR}cenarios_desp_correntes.parquet.gzip')
    df_prev = pd.concat([df_rec_prev, df_desp_prev], axis=1)
    return df_prev


def tab_endividamento():
    ano = ano_ref()
    df = pd.read_parquet(f'{DIR}endividamento.parquet.gzip')
    query = f'data.dt.year == {ano}'
    df.query(query, inplace=True)
    return df


def ind_poup_corr_ant(df_receitas, df_despesas, ano):
    ano_2 = ano - 2
    ano_1 = ano - 1

    multip = [0.2, 0.3]

    df_pc = pd.concat([
        df_receitas. \
            query("data.dt.year >= @ano_2 and data.dt.year < @ano"). \
            groupby("data")["rca"]. \
            sum().resample('y').sum(),
        df_despesas. \
            query("data.dt.year >= @ano_2 and data.dt.year < @ano"). \
            groupby("data")["empenho"]. \
            sum().resample('y').sum()
    ], axis=1)
    df_pc["ind_pc"] = df_pc.empenho / df_pc.rca

    result = {ano.year: i * m for (ano, i), m in
              zip(df_pc["ind_pc"].to_dict().items(), multip)}
    result.update({'ind_pc_anterior': sum(result.values())})

    return result


def tab_poup_corr(df_previsoes):
    df_receita, df_despesa = receitas(), despesas()
    data = data_ref()
    df_rca_emp = pd.concat([
        df_receita. \
            query("data <= @data"). \
            groupby("data")["rca"]. \
            sum(),
        df_despesa. \
            query("data <= @data"). \
            groupby("data")["empenho"]. \
            sum()
    ],
        axis=1)

    df = pd.concat([
        df_rca_emp,
        df_previsoes[["rca_prev", "emp_prev"]]. \
            rename({"rca_prev": "rca", "emp_prev": "empenho"}, axis=1). \
            query("data > @data")
    ])

    anos = df.index.year.unique()[-3:].to_list()

    dfs = list()
    for a in anos:
        ind_pc_ant = ind_poup_corr_ant(df_receita, df_despesa, a)
        df_ano = df.query("index.dt.year == @a").cumsum()
        df_ano["ind_pc"] = (df_ano.empenho / df_ano.rca * 0.5) + \
                           ind_pc_ant["ind_pc_anterior"]
        dfs.append(df_ano)

    df_result = pd.concat(dfs)
    df_result.columns = ["rca_acum_ano", "emp_acum_ano", "ind_pc"]
    df_result = df_result.join(df)
    df_result["nota"] = df_result["ind_pc"].apply(pc_nota)
    return df_result


def pc_nota(indice):
    if indice < 0.85:
        return "A"
    elif indice >= 0.95:
        return "C"
    else:
        return "B"


def tab_dc_rc():
    return pd.read_parquet(f'{DIR}desp_rec_correntes.parquet.gzip')


def tab_liquidez():
    df = pd.read_parquet(f"{DIR}liquidez.parquet.gzip")
    return df


def nota_geral(n1, n2, n3):

    if {n1, n2, n3} == {"A"}:
        return "A"
    elif {n2, n3} == "A" or {n2, n3} == {"B", "A"}:
        return "B"
    elif {n1, n2, n3} == {"C"}:
        return "D"
    else:
        return "C"


def pesquisa_nota(df, data):
    dt = datetime.strptime(data, "%Y-%m")
    nota = df.query("index.dt.month == @dt.month & "
                    "index.dt.year == @dt.year")["nota"]
    dt_format = dt.strftime("%b/%y")
    return nota[0], dt_format
