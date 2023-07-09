from dash import Input, Output, html
import dash_bootstrap_components as dbc
from app.dashboards.capag.components import comps
from app.dashboards.capag import data
from app.dashboards.capag.graficos import linhas, bullet

# datas
ano_ref = data.ano_ref()
data_ref = data.data_ref()
data_ref_format = data.data_ref_format()
data_fim_ano = data.data_fim_ano()

# datasets
df_end = data.tab_endividamento()
df_prev = data.previsoes()
df_dc_rc = data.tab_dc_rc()
df_liq = data.tab_liquidez()


def callbacks(app):
    # nota geral
    @app.callback(
        [Output("nota-realizada", "children"),
         Output("nota-projetada", "children")],
        Input("poup-corr-radio-ano", "value"),
        Input("poup-corr-radio-cenarios", "value")
    )
    def nota_geral(value, cenario_option):
        n1_realiz, data_realiz = data.pesquisa_nota(df_end, data_ref)

        dt1 = f"{value}-{data_ref[-2:]}"

        df_prev_para_pc = df_prev[
            ["rca_prev", cenario_option]
        ].rename(columns={cenario_option: "emp_prev"})
        df_pc = data.tab_poup_corr(df_prev_para_pc)

        n2_realiz, _ = data.pesquisa_nota(df_pc, dt1)

        n3 = df_liq[-1:]["nota"][0]

        n_realiz = data.nota_geral(n1_realiz, n2_realiz, n3)

        ###
        n1_proj, data_proj = data.pesquisa_nota(df_end, data_fim_ano)
        dt2 = f"{value}-{data_fim_ano[-2:]}"
        n2_proj, _ = data.pesquisa_nota(df_pc, dt2)

        n_proj = data.nota_geral(n1_proj, n2_proj, n3)

        txt1 = f"Nota geral em {data_realiz}: {n_realiz}"
        txt2 = f"Nota projetada para {data_proj}: {n_proj}"

        return [txt1, txt2]

    # gráficos de poupanças corrente
    @app.callback(
        [Output("poup-corr_graf", "figure"),
         Output("desp-corr-rca-graf", "figure")],
        Input("poup-corr-radio-ano", "value"),
        Input("poup-corr-radio-cenarios", "value")
    )
    def graficos_pc(value, cenario_option):
        df_prev_para_pc = df_prev[
            ["rca_prev", cenario_option]
        ].rename(columns={cenario_option: "emp_prev"})
        df_pc = data.tab_poup_corr(df_prev_para_pc)
        df = df_pc.query("data.dt.year == @value")
        poup_corr = linhas.indicador(
            df,
            data_ref,
            "ind_pc",
            "Poupança Corrente",
            "Poup. corrente",
            "Previsto")
        rca_dc = linhas.componentes(
            df,
            data_ref,
            "rca_acum_ano",
            "emp_acum_ano",
            "Desp. Corrente x RC Ajustada",
            "RCA", "RCA prevista",
            "Desp. Corrente",
            "Desp. Corr. Prevista"
        )
        return poup_corr, rca_dc

    @app.callback(
        Output("poup-corr-radio-cenarios", "options"),
        Input("poup-corr-radio-ano", "value")
    )
    def cenarios_radio_button(value):
        opcoes = [
            'Var. Acumulada Ano',
            'Var. Média Histórica',
            'Var. Médias 3 anos'
        ]

        if value == 2022:
            return [{'label': op, 'value': op} for op in opcoes]
        else:
            return [
                {'label': op, 'value': op, 'disabled': True}
                for op in opcoes
            ]

    # nota de poupanças corrente
    @app.callback(
        Output("nota-poup-corr", "children"),
        Input("poup-corr-radio-ano", "value"),
        Input("poup-corr-radio-cenarios", "value")
    )
    def notas_pc(value, cenario_option):
        df_prev_para_pc = df_prev[
            ["rca_prev", cenario_option]
        ].rename(columns={cenario_option: "emp_prev"})
        df_pc = data.tab_poup_corr(df_prev_para_pc)
        df = df_pc.query("data.dt.year == @value")

        dt1 = f"{value}-{data_ref[-2:]}"
        nota1, dt_format1 = data.pesquisa_nota(df, dt1)

        dt2 = f"{value}-{data_fim_ano[-2:]}"
        nota2, dt_format2 = data.pesquisa_nota(df, dt2)

        return [comps.col_nota(dt_format1, nota1),
                comps.col_nota(dt_format2, nota2)]

    @app.callback(
        Output("meta-poup-corr", "children"),
        Input("poup-corr-radio-ano", "value"),
        Input("poup-corr-radio-cenarios", "value")
    )
    def bullet_pc(value, cenario_option):
        if value == 2022:
            dt = comps.dt
            rec = data.receitas()
            desp = data.despesas()

            df_prev_para_pc = df_prev[
                ["rca_prev", cenario_option]
            ].rename(columns={cenario_option: "emp_prev"})
            df_pc = data.tab_poup_corr(df_prev_para_pc)

            df = df_pc.copy()
            emp_atual = df.query(
                "data.dt.year == @dt.year and data.dt.month == @dt.month"). \
                emp_acum_ano.to_list()[0]
            ind_pc_meta = (0.9 - data.ind_poup_corr_ant(rec, desp, value)[
                "ind_pc_anterior"]) / 0.5
            pc_limite_a = df.tail(1)["rca_acum_ano"].to_list()[0] * ind_pc_meta

            pc_diff = pc_limite_a - emp_atual

            fig = bullet.bullet("Empenhos", emp_atual, pc_limite_a)

            meta_pc = comps.meta(fig,
                                 [emp_atual, pc_limite_a, pc_diff],
                                 "Total de empenhos")

            return meta_pc

    @app.callback(
        Output("meta-poup-corr", "style"),
        Input("poup-corr-radio-ano", "value")
    )
    def style_bullet(value):
        if value == 2022:
            return {"height": 220}
        else:
            return {"height": 0}

    # gráficos de dc/rc
    @app.callback(
        [Output("dc-rc-graf", "figure"),
         Output("desp-liq-rc-graf", "figure")],
        Input("dc-rc-radio", "value")
    )
    def graficos_dc_rc(value):
        df = df_dc_rc.query("data.dt.year == @value")
        dc = linhas.indicador(
            df,
            data_ref,
            "ind_liq_rc",
            "Desp. Corr. x Rec. Corr.",
            "DC x RC",
            "")
        rc = linhas.componentes_dc_rc(
            df,
            data_ref,
            "rc",
            "liquidado",
            "Desp. Corr. Liq. x Rec. Corr. (em 12 meses)",
            "Rec. Corr.",
            "Desp. Corr."
        )
        return dc, rc

    # resultado de dc x rc
    @app.callback(
        Output("nota-dc-rc", "children"),
        Input("dc-rc-radio", "value")
    )
    def notas_dc_rc(value):
        df = df_dc_rc.copy()

        dt = f"{value}-{data_ref[-2:]}"
        nota, dt_format = data.pesquisa_nota(df, dt)
        nota = "Habilitado" if nota == 1 else "Inabilitado"

        col = dbc.Col([
            html.H5(f"Resultado em {dt_format}: {nota}"),
        ], sm=12, lg=2, style={"background-color": "#EEEEEE",
                               "border-radius": 25,
                               "text-align": "center"})
        return [col]
