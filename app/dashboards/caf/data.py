import os
import numpy as np
import pandas as pd

DATASET = "app/dashboards/_datasets/caf/caf.parquet.gzip"


def arquivos():
    df_raw = pd.read_parquet(DATASET)
    return df_raw


def data_arquivo():
    df = arquivos()
    data = df.data_arquivo.max()
    return pd.to_datetime(data, format="%Y%m%d").strftime("%d/%m/%Y")


def novos_processos():
    df = arquivos()
    dtmax = df.data_arquivo.max()
    pnewfile = df.query('data_arquivo == @dtmax')['cd_processo'].unique()
    poldfiles = df.query('data_arquivo < @dtmax')['cd_processo'].unique()
    novos_processos = list(set(pnewfile) - set(poldfiles))
    return df.\
        query('cd_processo == @novos_processos').\
        razao_social.\
        unique()


def dataset(todas_as_bases=False):
    df = arquivos()
    dtmax = df.data_arquivo.max()
    data_arquivos = arquivos()
    if not todas_as_bases:
        return df.query('data_arquivo == @dtmax')
    return df


def coluna_vals(coluna, df=None):
    if df is not None:
        return df[coluna].dropna().unique().tolist()
    df = dataset()
    return df[coluna].dropna().unique().tolist()


def df_com_totais(df, col_to_agg, cols_calculate, col_to_perc,
                    cols_to_rename):

    df_grp = df.groupby(col_to_agg).agg(cols_calculate)

    cols = list(cols_calculate.keys())
    cols.remove(col_to_perc)

    df_per = df_grp. \
        groupby(level=0). \
        apply(lambda x: x / float(df_grp[col_to_perc].sum())). \
        rename(columns={col_to_perc: "perc"}). \
        drop(cols, axis=1)

    df_per_ = df_per.join(df_grp).sort_values("perc", ascending=False)
    df_result = pd.concat([
            df_per_, df_per_.sum().rename('Total').to_frame().T
        ]).reset_index()

    if cols_to_rename:
        df_result.columns = cols_to_rename

    return df_result


def df_com_filtros(anos, meses, anos_sit_atual, meses_sit_atual, input_dict,
                   todas_as_bases=False):
    """
    :param todas_as_bases:
    :param anos: lista de anos do rangerslide
    :param meses: lista de meses do rangerslide
    :param anos_sit_atual: lista de anos da situação atual do rangerslide
    :param meses_sit_atual: lista de meses da situação atual do rangerslide
    :param input_dict: dict {coluna: [valores da coluna] dos dropdowns
    :param todas_as_bases: se todas os BDs estarão no dataset
    :return: df filtrado
    """

    df = dataset(todas_as_bases=todas_as_bases)

    anos = [ano for ano in range(anos[0], anos[1] + 1)]
    meses = [mes for mes in range(meses[0], meses[1] + 1)]
    anos_sit_atual = [ano for ano in range(
        anos_sit_atual[0], anos_sit_atual[1] + 1)]
    meses_sit_atual = [mes for mes in range(
        meses_sit_atual[0], meses_sit_atual[1] + 1)]

    df.query(
        "ano_lavratura == @anos and "
        "data_lavratura.dt.month == @meses and "
        "ano_sit_atual == @anos_sit_atual and "
        "data_sit_atual.dt.month == @meses_sit_atual",
        inplace=True
    )

    query_list = list()
    for k, v in input_dict.items():
        if v is not None and v != []:
            if len(v) == 1:
                v = list(v)
            query_list.append(f"{k} == {v}")
    try:
        query = ' & '.join(query_list)
        result = df.query(query)
    except ValueError:
        result = df

    return result


def df_contagem_por_datasets(df, agg):
    if agg == "cd_processo":
        dfc = df.groupby(["data_arquivo", "instancia", "procedencia"],
                         as_index=False, dropna=False)[agg].count()
        dfc = dfc.pivot(index=["instancia", "procedencia"],
                        columns="data_arquivo", values=agg)
    else:
        dfc = df.groupby(["data_arquivo", "instancia", "procedencia"],
                         as_index=False, dropna=False)[agg].sum()
        dfc = dfc.pivot(index=["instancia", "procedencia"],
                        columns="data_arquivo", values=agg)

    dfc.columns = dfc.columns.to_list()

    dfs_list = list()

    for ist in dfc.dropna().index.get_level_values("instancia").unique():
        grp_filtered_per_inst = dfc.query("instancia == @ist")

        grp_inst_total = dfc.query("instancia == @ist").groupby(
            ["instancia"]).sum()

        total = pd.DataFrame(
            data=grp_inst_total.values,
            index=pd.MultiIndex.from_tuples(
                [("", "".join(["Total ", ist]))],
                names=["instancia", "resultado"]),
            columns=grp_inst_total.columns
        )

        dfs_list.append(
            pd.concat([grp_filtered_per_inst, total])
        )

    df_result = pd.concat(dfs_list)

    # Total table
    df_total = pd.DataFrame(
        data=pd.concat(
            [dfc, dfc.sum().to_frame().T],
            ignore_index=True
        )[-1:].values,
        index=pd.MultiIndex.from_tuples([("TOTAL", "")],
                                        names=["instancia", "resultado"]),
        columns=df_result.columns
    )
    df_result = pd.concat([df_result, df_total])
    df_result.index.names = ["Instância", "Resultado"]
    df_result.columns = [d.strftime('%d/%b/%y') for d in df_result.columns]
    # df_result.reset_index(inplace=True)

    return df_result


def anos_intervalo():
    ano_min = min(coluna_vals("ano_lavratura"))
    ano_max = pd.Timestamp.now().year + 1
    return list(range(ano_min, ano_max))


def df_rs_quitado_parcelado(df, rotulo, tipo_valor):
    dt_col = 'data_arquivo'
    if tipo_valor == 'valor_quitado':
        dt_col = 'data_sit_terminativa'

        dt_max = df.data_arquivo.max()
        df.query('data_arquivo == @dt_max', inplace=True)

    df = df[df[dt_col].dt.strftime('%b/%y') == rotulo]
    df_rs = df[df[tipo_valor] > 0]

    df_rs = (
        df_rs.groupby(['razao_social', 'situacao_debito'], as_index=False)[
            tipo_valor
        ]
            .sum()
            .sort_values(tipo_valor, ascending=False)
    )

    col_valor = 'Quitado' if tipo_valor == 'valor_quitado' else 'Parcelado'
    df_rs.columns = ['Razão Social', 'Sit. Débito', col_valor]
    return df_rs


def df_tab_quitado_parcelado(df):
    # parcelados
    df_parc = df.filter(
        [
            'razao_social',
            'cd_processo',
            'cd_parcelamento',
            'data_arquivo',
            'data_parcelamento',
            'valor_parcelado',
        ]
    )

    df_parcel_pivot = pd.pivot_table(
        df_parc,
        values='valor_parcelado',
        index=['razao_social', 'cd_processo'],
        columns=['data_arquivo'],
        aggfunc=np.sum,
    )
    df_parcel_pivot.insert(0, '1a_col', 0)
    df_parcel_pivot_diff = df_parcel_pivot.diff(axis=1).drop('1a_col',
                                                             axis=1).sum()
    df_parcel_pivot_diff.name = 'Parcelado'

    # quitados
    dt_arq_max = df.data_arquivo.max()
    df_quit = df. \
        query("data_arquivo == @dt_arq_max and valor_quitado > 0"). \
        groupby(['data_sit_terminativa']). \
        valor_quitado.sum()

    df_quit.name = 'Quitado'

    # quitados + parcelados
    df_quit_parcel = pd.concat(
        [df_quit, df_parcel_pivot_diff], axis=1
    )

    df_quit_parcel_mes = df_quit_parcel. \
        groupby(df_quit_parcel.index.to_period('M'))[
        ['Quitado', 'Parcelado']
    ].sum()

    df_quit_parcel_total = df_quit_parcel_mes.assign(
        Total=(df_quit_parcel_mes.sum(axis=1))
    )
    return df_quit_parcel_total
