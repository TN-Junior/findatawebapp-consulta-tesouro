import pandas as pd
pd.options.mode.chained_assignment = None

ARQUIVO = "app/dashboards/_datasets/monitoramento/df.parquet.gzip"
NO_STATUS = ["CANCELADO", "CANCELADA"]


class Dataset:
    def __init__(self):
        self.df = pd.read_parquet(ARQUIVO).query(
            "STATUS != @NO_STATUS"
        )

    def data_arquivo(self):
        return self.df.DT_ARQUIVO.max()

    def data_arquivo_str(self):
        data = self.df.DT_ARQUIVO.max()
        return data.strftime("%d/%m/%y %H:%M")

    def dimensoes(self, setor=None, ):
        cols = ["PLANILHA", "OBJETIVO", "CD_OBJETIVO",
                "AÇÃO", "TAREFA", "STATUS"]
        df = self.df
        if setor:
            df = self.df_setor(setor)
        return {col: df[col].unique() for col in cols}

    def df_setor(self, setor):
        return self.df.query("PLANILHA == @setor")

    def df_obj(self, cod_obj):
        return self.df.query("CD_OBJETIVO == @cod_obj")

    def info_objetivo(self, cod_obj):
        df_obj = self.df_obj(cod_obj)

        obj_info = dict()

        obj_info['tabela'] = df_obj

        obj_info['codigo'] = cod_obj

        obj_info["objetivo"] = \
            df_obj["OBJETIVO"].unique()

        obj_info["descricao"] = \
            df_obj["DESCRIÇÃO DO OBJETIVO"].unique()

        obj_info["responsavel"] = \
            df_obj["RESPONSÁVEL PELO OBJETIVO"].unique()

        obj_info["executiva"] = \
            df_obj["EXECUTIVA RESPONSÁVEL PELO OBJETIVO"].unique()

        obj_info["total_tarefas"] = df_obj.shape[0]

        obj_info["atrasadas"] = df_obj.query(
            "STATUS == 'ATRASADA'")['STATUS'].count()

        obj_info["concluidas"] = df_obj.query(
            "STATUS == 'CONCLUÍDA'")['STATUS'].count()

        obj_info["andamento"] = df_obj.query(
            "STATUS == 'EM ANDAMENTO'")['STATUS'].count()

        obj_info["iniciar"] = df_obj.query(
            "STATUS == 'A INICIAR'")['STATUS'].count()

        obj_info["suspenso"] = df_obj.query(
            "STATUS == 'SUSPENSO'")['STATUS'].count()

        if obj_info["total_tarefas"] == obj_info["concluidas"]:
            obj_info["obj_status"] = True
        else:
            obj_info["obj_status"] = False

        if "SIM" in df_obj["ESTRATÉGICO"].unique():
            obj_info["estrat"] = True
        else:
            obj_info["estrat"] = False

        if "SIM" in df_obj["OPERACIONAL"].unique():
            obj_info["operacional"] = True
        else:
            obj_info["operacional"] = False

        if "SIM" in df_obj["SEPLAG"].unique():
            obj_info["seplag"] = True
        else:
            obj_info["seplag"] = False

        if "SIM" in df_obj["PNAFM"].unique():
            obj_info["pnafm"] = True
        else:
            obj_info["pnafm"] = False

        if "SIM" in df_obj["BID"].unique():
            obj_info["bid"] = True
        else:
            obj_info["bid"] = False

        try:
            obj_info["prev_inicio"] = \
                df_obj['PREVISÃO DE INÍCIO'].min().strftime("%d/%m/%y")
        except ValueError:
            obj_info["prev_inicio"] = None

        try:
            obj_info["prev_termino"] = \
                df_obj['PREVISÃO DE TÉRMINO'].max().strftime("%d/%m/%y")
        except ValueError:
            obj_info["prev_termino"] = None

        try:
            obj_info["dt_max_tarefa_finaliz"] = \
                df_obj['FIM EXECUÇÃO'].max()
        except ValueError:
            obj_info["dt_max_tarefa_finaliz"] = None

        return obj_info
