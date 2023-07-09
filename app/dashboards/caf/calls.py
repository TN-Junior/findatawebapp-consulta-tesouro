from dash import Input, Output
from app.dashboards.caf.data import df_com_filtros, df_com_totais, \
    df_rs_quitado_parcelado, df_tab_quitado_parcelado
from app.dashboards.caf.charts.charts import combo_chart, stacked_bar, \
    dot_line, combo_and_stacked_bar
from app.dashboards.caf.charts.tables import tab_ranking, tab_razao_social, \
    tab_contagem_por_datasets, tab_rs_quitado_parcelado
from app.dashboards.caf import comps


def callbacks(app):
    @app.callback(
        Output("drop-razao-social", "options"),
        Input("slide-anos", "value"),
        Input("slide-meses", "value"),
        Input("slide-anos-sit-atual", "value"),
        Input("slide-meses-sit-atual", "value"),
        Input("drop-razao-social-processo", "value"),
        Input("drop-situacao-atual", "value"),
        Input("drop-situacao-debito", "value"),
        Input("drop-mudanca-status", "value"),
        Input("drop-instancia", "value"),
        Input("drop-finalizado", "value"),
        Input("drop-fora-caf", "value")
    )
    def drp_rs(anos, meses, anos_sit_atual, meses_sit_atual, raz_social_proc,
               sit_atual, sit_debito, ms, inst, finaliz, fora):
        input_dict = {
            "razao_social_process": raz_social_proc,
            "desc_sit_atual": sit_atual,
            "situacao_debito": sit_debito,
            "mudanca_status": ms,
            "instancia": inst,
            "flag_sit_terminativa": finaliz,
            "flag_sit_fora_caf": fora
        }
        df = df_com_filtros(anos, meses, anos_sit_atual, meses_sit_atual,
                            input_dict)
        rs = df["razao_social"].unique().tolist()
        drp_razao_social = [{'label': i, 'value': i} for i in rs]

        return drp_razao_social

    @app.callback(
        Output("drop-razao-social-processo", "options"),
        Input("slide-anos", "value"),
        Input("slide-meses", "value"),
        Input("slide-anos-sit-atual", "value"),
        Input("slide-meses-sit-atual", "value"),
        Input("drop-razao-social", "value"),
        Input("drop-situacao-atual", "value"),
        Input("drop-situacao-debito", "value"),
        Input("drop-mudanca-status", "value"),
        Input("drop-instancia", "value"),
        Input("drop-finalizado", "value"),
        Input("drop-fora-caf", "value")
    )
    def drp_rs_proc(anos, meses, anos_sit_atual, meses_sit_atual, rs,
                    sit_atual, sit_debito, ms, inst, finaliz, fora):
        input_dict = {
            "razao_social": rs,
            "desc_sit_atual": sit_atual,
            "situacao_debito": sit_debito,
            "mudanca_status": ms,
            "instancia": inst,
            "flag_sit_terminativa": finaliz,
            "flag_sit_fora_caf": fora
        }
        df = df_com_filtros(anos, meses, anos_sit_atual, meses_sit_atual,
                            input_dict)
        rs_proc = df["razao_social_process"].unique().tolist()
        drp_razao_social_proc = [{'label': i, 'value': i} for i in rs_proc]

        return drp_razao_social_proc

    @app.callback(
        Output("drop-situacao-atual", "options"),
        Input("slide-anos", "value"),
        Input("slide-meses", "value"),
        Input("slide-anos-sit-atual", "value"),
        Input("slide-meses-sit-atual", "value"),
        Input("drop-razao-social-processo", "value"),
        Input("drop-razao-social", "value"),
        Input("drop-situacao-debito", "value"),
        Input("drop-mudanca-status", "value"),
        Input("drop-instancia", "value"),
        Input("drop-finalizado", "value"),
        Input("drop-fora-caf", "value")
    )
    def drp_sa(anos, meses, anos_sit_atual, meses_sit_atual, raz_social_proc,
               rs, sit_debito, ms, inst, finaliz, fora):

        input_dict = {
            "razao_social": rs,
            "razao_social_process": raz_social_proc,
            "situacao_debito": sit_debito,
            "mudanca_status": ms,
            "instancia": inst,
            "flag_sit_terminativa": finaliz,
            "flag_sit_fora_caf": fora
        }
        df = df_com_filtros(anos, meses, anos_sit_atual, meses_sit_atual,
                            input_dict)
        sa = df["desc_sit_atual"].unique().tolist()
        return [{'label': i, 'value': i} for i in sa]

    @app.callback(
        Output("drop-situacao-debito", "options"),
        Input("slide-anos", "value"),
        Input("slide-meses", "value"),
        Input("slide-anos-sit-atual", "value"),
        Input("slide-meses-sit-atual", "value"),
        Input("drop-razao-social-processo", "value"),
        Input("drop-razao-social", "value"),
        Input("drop-situacao-atual", "value"),
        Input("drop-mudanca-status", "value"),
        Input("drop-instancia", "value"),
        Input("drop-finalizado", "value"),
        Input("drop-fora-caf", "value")
    )
    def drp_sd(anos, meses, anos_sit_atual, meses_sit_atual, raz_social_proc,
               rs, sit_atual, ms, inst, finaliz, fora):

        input_dict = {
            "razao_social": rs,
            "razao_social_process": raz_social_proc,
            "desc_sit_atual": sit_atual,
            "mudanca_status": ms,
            "instancia": inst,
            "flag_sit_terminativa": finaliz,
            "flag_sit_fora_caf": fora
        }
        df = df_com_filtros(anos, meses, anos_sit_atual, meses_sit_atual,
                            input_dict)
        sd = df["situacao_debito"].unique().tolist()
        return [{'label': i, 'value': i} for i in sd]

    @app.callback(
        Output("drop-mudanca-status", "options"),
        Input("slide-anos", "value"),
        Input("slide-meses", "value"),
        Input("slide-anos-sit-atual", "value"),
        Input("slide-meses-sit-atual", "value"),
        Input("drop-razao-social-processo", "value"),
        Input("drop-razao-social", "value"),
        Input("drop-situacao-atual", "value"),
        Input("drop-situacao-debito", "value"),
        Input("drop-instancia", "value"),
        Input("drop-finalizado", "value"),
        Input("drop-fora-caf", "value")
    )
    def drp_ms(anos, meses, anos_sit_atual, meses_sit_atual, raz_social_proc,
               rs, sit_atual, sit_debito, inst, finaliz, fora):
        input_dict = {
            "razao_social": rs,
            "razao_social_process": raz_social_proc,
            "desc_sit_atual": sit_atual,
            "situacao_debito": sit_debito,
            "instancia": inst,
            "flag_sit_terminativa": finaliz,
            "flag_sit_fora_caf": fora
        }
        df = df_com_filtros(anos, meses, anos_sit_atual, meses_sit_atual,
                            input_dict)
        ms = df["mudanca_status"].unique().tolist()
        return [{'label': t, 'value': t} for t in ms]

    @app.callback(
        Output("drop-instancia", "options"),
        Input("slide-anos", "value"),
        Input("slide-meses", "value"),
        Input("slide-anos-sit-atual", "value"),
        Input("slide-meses-sit-atual", "value"),
        Input("drop-razao-social-processo", "value"),
        Input("drop-razao-social", "value"),
        Input("drop-situacao-atual", "value"),
        Input("drop-situacao-debito", "value"),
        Input("drop-mudanca-status", "value"),
        Input("drop-finalizado", "value")
    )
    def drp_inst(anos, meses, anos_sit_atual, meses_sit_atual, raz_social_proc,
                 rs, sit_atual, sit_debito, ms, finaliz):
        input_dict = {
            "razao_social": rs,
            "razao_social_process": raz_social_proc,
            "desc_sit_atual": sit_atual,
            "situacao_debito": sit_debito,
            "mudanca_status": ms,
            "flag_sit_terminativa": finaliz
        }
        df = df_com_filtros(anos, meses, anos_sit_atual,
                            meses_sit_atual, input_dict)
        istancia = df["instancia"].dropna().unique().tolist()
        return [{'label': i, 'value': i} for i in istancia]

    @app.callback(
        Output("drop-finalizado", "options"),
        Input("slide-anos", "value"),
        Input("slide-meses", "value"),
        Input("slide-anos-sit-atual", "value"),
        Input("slide-meses-sit-atual", "value"),
        Input("drop-razao-social-processo", "value"),
        Input("drop-razao-social", "value"),
        Input("drop-situacao-atual", "value"),
        Input("drop-situacao-debito", "value"),
        Input("drop-mudanca-status", "value"),
        Input("drop-instancia", "value"),
        Input("drop-fora-caf", "value")
    )
    def drp_sit_term(anos, meses, anos_sit_atual, meses_sit_atual,
                     raz_social_proc, rs, sit_atual, sit_debito, ms, inst,
                     fora):
        input_dict = {
            "razao_social": rs,
            "razao_social_process": raz_social_proc,
            "desc_sit_atual": sit_atual,
            "situacao_debito": sit_debito,
            "mudanca_status": ms,
            "instancia": inst,
            "flag_sit_fora_caf": fora
        }
        df = df_com_filtros(anos, meses, anos_sit_atual,
                            meses_sit_atual, input_dict)
        st = df["flag_sit_terminativa"].unique().tolist()
        return [{'label': i, 'value': i} for i in st]

    @app.callback(
        Output("drop-fora-caf", "options"),
        Input("slide-anos", "value"),
        Input("slide-meses", "value"),
        Input("slide-anos-sit-atual", "value"),
        Input("slide-meses-sit-atual", "value"),
        Input("drop-razao-social-processo", "value"),
        Input("drop-razao-social", "value"),
        Input("drop-situacao-atual", "value"),
        Input("drop-situacao-debito", "value"),
        Input("drop-mudanca-status", "value"),
        Input("drop-instancia", "value"),
        Input("drop-finalizado", "value")
    )
    def drp_fc(anos, meses, anos_sit_atual, meses_sit_atual, raz_social_proc,
               rs, sit_atual, sit_debito, ms, inst, finaliz):
        input_dict = {
            "razao_social": rs,
            "razao_social_process": raz_social_proc,
            "desc_sit_atual": sit_atual,
            "situacao_debito": sit_debito,
            "mudanca_status": ms,
            "instancia": inst,
            "flag_sit_terminativa": finaliz
        }
        df = df_com_filtros(anos, meses, anos_sit_atual, meses_sit_atual,
                            input_dict)
        fc = df["flag_sit_fora_caf"].unique().tolist()
        return [{'label': i, 'value': i} for i in fc]

    @app.callback(
        Output('kpi-cabecalho', 'children'),
        Input('slide-anos', 'value'),
        Input('slide-meses', 'value'),
        Input('slide-anos-sit-atual', 'value'),
        Input('slide-meses-sit-atual', 'value'),
        Input('drop-razao-social', 'value'),
        Input('drop-razao-social-processo', 'value'),
        Input('drop-situacao-atual', 'value'),
        Input('drop-situacao-debito', 'value'),
        Input('drop-mudanca-status', 'value'),
        Input('drop-instancia', 'value'),
        Input('drop-finalizado', 'value'),
        Input('drop-fora-caf', 'value'),
    )
    def kpi_cabecalho(
            anos,
            meses,
            anos_sit_atual,
            meses_sit_atual,
            rs,
            raz_social,
            sit_atual,
            sit_debito,
            ms,
            inst,
            finaliz,
            fora,
    ):
        input_dict = {
            'razao_social': rs,
            'razao_social_process': raz_social,
            'desc_sit_atual': sit_atual,
            'situacao_debito': sit_debito,
            'mudanca_status': ms,
            'instancia': inst,
            'flag_sit_terminativa': finaliz,
            'flag_sit_fora_caf': fora,
        }
        df = df_com_filtros(
            anos, meses, anos_sit_atual, meses_sit_atual, input_dict
        )

        global_qtd = df.shape[0]
        global_valor = df['valor_total'].sum()
        global_dias = df['dias_sit_atual_lavr'].mean()

        ativos = df.query('ativo == True')
        ativos_qtd = ativos.shape[0]
        ativos_valor = ativos['valor_total'].sum()
        ativos_dias = ativos['dias_sit_atual_lavr'].mean()

        tram = df.query("mudanca_status == 'Sim'")
        tram_qtd = tram.shape[0]
        tram_valor = tram['valor_total'].sum()
        tram_dias = tram['dias_sit_atual_lavr'].mean()

        finaliz = df.query('finalizado == True')
        finaliz_qtd = finaliz.shape[0]
        finaliz_valor = finaliz['valor_total'].sum()
        finaliz_dias = finaliz['dias_sit_atual_lavr'].mean()

        div_ativa = df.query('div_ativa == True')
        div_ativa_qtd = div_ativa.shape[0]
        div_ativa_valor = div_ativa['valor_total'].sum()
        div_ativa_dias = div_ativa['dias_sit_atual_lavr'].mean()

        kpis = comps.kpis(
            [
                global_qtd,
                global_valor,
                global_dias,
                ativos_qtd,
                ativos_valor,
                ativos_dias,
                tram_qtd,
                tram_valor,
                tram_dias,
                finaliz_qtd,
                finaliz_valor,
                finaliz_dias,
                div_ativa_qtd,
                div_ativa_valor,
                div_ativa_dias,
            ]
        )
        return kpis

    @app.callback(
        Output('tab-resultado', 'children'),
        Input('slide-anos', 'value'),
        Input('slide-meses', 'value'),
        Input('slide-anos-sit-atual', 'value'),
        Input('slide-meses-sit-atual', 'value'),
        Input('drop-razao-social', 'value'),
        Input('drop-razao-social-processo', 'value'),
        Input('drop-situacao-atual', 'value'),
        Input('drop-situacao-debito', 'value'),
        Input('drop-mudanca-status', 'value'),
        Input('drop-instancia', 'value'),
        Input('drop-finalizado', 'value'),
        Input('drop-fora-caf', 'value'),
        Input('radio-tab-cont-datasets', 'value'),
    )
    def tab_evolucao_por_data_extracao(
            anos,
            meses,
            anos_sit_atual,
            meses_sit_atual,
            rs,
            raz_social,
            sit_atual,
            sit_debito,
            ms,
            inst,
            finaliz,
            fora,
            agg,
    ):
        input_dict = {
            'razao_social': rs,
            'razao_social_process': raz_social,
            'desc_sit_atual': sit_atual,
            'situacao_debito': sit_debito,
            'mudanca_status': ms,
            'instancia': inst,
            'flag_sit_terminativa': finaliz,
            'flag_sit_fora_caf': fora,
        }
        df = df_com_filtros(
            anos,
            meses,
            anos_sit_atual,
            meses_sit_atual,
            input_dict,
            todas_as_bases=True,
        )

        table = tab_contagem_por_datasets(df, agg=agg)

        return table

    @app.callback(
        Output('bar-quitados-parcelados', 'figure'),
        Input('slide-anos', 'value'),
        Input('slide-meses', 'value'),
        Input('slide-anos-sit-atual', 'value'),
        Input('slide-meses-sit-atual', 'value'),
        Input('drop-razao-social', 'value'),
        Input('drop-razao-social-processo', 'value'),
        Input('drop-situacao-atual', 'value'),
        Input('drop-situacao-debito', 'value'),
        Input('drop-mudanca-status', 'value'),
        Input('drop-instancia', 'value'),
        Input('drop-finalizado', 'value'),
        Input('drop-fora-caf', 'value'),
    )
    def bar_quitados_parcelados(
            anos,
            meses,
            anos_sit_atual,
            meses_sit_atual,
            rs,
            raz_social,
            sit_atual,
            sit_debito,
            ms,
            inst,
            finaliz,
            fora,
    ):
        input_dict = {
            'razao_social': rs,
            'razao_social_process': raz_social,
            'desc_sit_atual': sit_atual,
            'situacao_debito': sit_debito,
            'mudanca_status': ms,
            'instancia': inst,
            'flag_sit_terminativa': finaliz,
            'flag_sit_fora_caf': fora,
        }
        df = df_com_filtros(
            anos,
            meses,
            anos_sit_atual,
            meses_sit_atual,
            input_dict,
            todas_as_bases=True,
        )

        df_quit_parcel_total = df_tab_quitado_parcelado(df)
        df_quit_parcel_total.query('index > "2021-07"', inplace=True)
        fig = combo_and_stacked_bar(df_quit_parcel_total)
        return fig

    @app.callback(
        Output('tab-output', 'children'),
        Input('slide-anos', 'value'),
        Input('slide-meses', 'value'),
        Input('slide-anos-sit-atual', 'value'),
        Input('slide-meses-sit-atual', 'value'),
        Input('drop-razao-social', 'value'),
        Input('drop-razao-social-processo', 'value'),
        Input('drop-situacao-atual', 'value'),
        Input('drop-situacao-debito', 'value'),
        Input('drop-mudanca-status', 'value'),
        Input('drop-instancia', 'value'),
        Input('drop-finalizado', 'value'),
        Input('drop-fora-caf', 'value'),
        Input('bar-quitados-parcelados', 'clickData'),
    )
    def tab_quitados_parcelados(
            anos,
            meses,
            anos_sit_atual,
            meses_sit_atual,
            rs,
            raz_social,
            sit_atual,
            sit_debito,
            ms,
            inst,
            finaliz,
            fora,
            click_data,
    ):
        input_dict = {
            'razao_social': rs,
            'razao_social_process': raz_social,
            'desc_sit_atual': sit_atual,
            'situacao_debito': sit_debito,
            'mudanca_status': ms,
            'instancia': inst,
            'flag_sit_terminativa': finaliz,
            'flag_sit_fora_caf': fora,
        }
        df = df_com_filtros(
            anos,
            meses,
            anos_sit_atual,
            meses_sit_atual,
            input_dict,
            todas_as_bases=True,
        )

        if click_data is not None:
            try:
                curve = click_data['points'][0]['curveNumber']
                rotulo = click_data['points'][0]['label']

                if curve == 1:
                    tipo_valor = 'valor_quitado'
                else:
                    tipo_valor = 'valor_parcelado'

                df_rs = df_rs_quitado_parcelado(df, rotulo, tipo_valor)
                return tab_rs_quitado_parcelado(df_rs)
            except KeyError:
                return None

    @app.callback(
        Output('combo-chart', 'figure'),
        Input('slide-anos', 'value'),
        Input('slide-meses', 'value'),
        Input('slide-anos-sit-atual', 'value'),
        Input('slide-meses-sit-atual', 'value'),
        Input('drop-razao-social', 'value'),
        Input('drop-razao-social-processo', 'value'),
        Input('drop-situacao-atual', 'value'),
        Input('drop-situacao-debito', 'value'),
        Input('drop-mudanca-status', 'value'),
        Input('drop-instancia', 'value'),
        Input('drop-finalizado', 'value'),
        Input('drop-fora-caf', 'value'),
    )
    def combo_evolucao_por_lavratura(
            anos,
            meses,
            anos_sit_atual,
            meses_sit_atual,
            rs,
            raz_social,
            sit_atual,
            sit_debito,
            ms,
            inst,
            finaliz,
            fora,
    ):
        input_dict = {
            'razao_social': rs,
            'razao_social_process': raz_social,
            'desc_sit_atual': sit_atual,
            'situacao_debito': sit_debito,
            'mudanca_status': ms,
            'instancia': inst,
            'flag_sit_terminativa': finaliz,
            'flag_sit_fora_caf': fora,
        }

        df = df_com_filtros(
            anos, meses, anos_sit_atual, meses_sit_atual, input_dict
        )

        df_ativos_grp_ano = df.groupby('ano_lavratura').agg(
            {'valor_total': 'sum', 'cd_processo': 'count'}
        )

        fig = combo_chart(
            None,
            'Valor em R$',
            'Processos',
            df_ativos_grp_ano.index,
            df_ativos_grp_ano.valor_total,
            df_ativos_grp_ano.cd_processo,
        )
        return fig

    @app.callback(
        Output('stacked-bar-processos', 'figure'),
        Output('stacked-bar-valor', 'figure'),
        Input('slide-anos', 'value'),
        Input('slide-meses', 'value'),
        Input('slide-anos-sit-atual', 'value'),
        Input('slide-meses-sit-atual', 'value'),
        Input('drop-razao-social', 'value'),
        Input('drop-razao-social-processo', 'value'),
        Input('drop-situacao-atual', 'value'),
        Input('drop-situacao-debito', 'value'),
        Input('drop-mudanca-status', 'value'),
        Input('drop-instancia', 'value'),
        Input('drop-finalizado', 'value'),
        Input('drop-fora-caf', 'value'),
    )
    def stacked_distribuicao_processos(
            anos,
            meses,
            anos_sit_atual,
            meses_sit_atual,
            rs,
            raz_social,
            sit_atual,
            sit_debito,
            ms,
            inst,
            finaliz,
            fora,
    ):
        input_dict = {
            'razao_social': rs,
            'razao_social_process': raz_social,
            'desc_sit_atual': sit_atual,
            'situacao_debito': sit_debito,
            'mudanca_status': ms,
            'instancia': inst,
            'flag_sit_terminativa': finaliz,
            'flag_sit_fora_caf': fora,
        }
        df = df_com_filtros(
            anos, meses, anos_sit_atual, meses_sit_atual, input_dict
        )
        # df.query("ativo == True", inplace=True)
        df_ativos_grp_ano = df.groupby('ano_lavratura').agg(
            {'valor_total': 'sum', 'cd_processo': 'count'}
        )

        processos = ['Qtd Processos']
        processos_pre = df_ativos_grp_ano.query(
            'index < 2016'
        ).cd_processo.sum()
        processos_apos = df_ativos_grp_ano.query(
            'index >= 2016'
        ).cd_processo.sum()

        fig1 = stacked_bar(processos, processos_pre, processos_apos)

        valor = ['Valor (R$)']
        valor_pre = df_ativos_grp_ano.query('index < 2016').valor_total.sum()
        valor_pos = df_ativos_grp_ano.query('index >= 2016').valor_total.sum()

        fig2 = stacked_bar(valor, valor_pre, valor_pos, True)
        return fig1, fig2

    @app.callback(
        Output('dot-line-chart', 'figure'),
        Input('slide-anos', 'value'),
        Input('slide-meses', 'value'),
        Input('slide-anos-sit-atual', 'value'),
        Input('slide-meses-sit-atual', 'value'),
        Input('drop-razao-social', 'value'),
        Input('drop-razao-social-processo', 'value'),
        Input('drop-situacao-atual', 'value'),
        Input('drop-situacao-debito', 'value'),
        Input('drop-mudanca-status', 'value'),
        Input('drop-instancia', 'value'),
        Input('radio-dot-chart', 'value'),
        Input('drop-finalizado', 'value'),
        Input('drop-fora-caf', 'value'),
    )
    def dots_data_lavratura_vs_data_situacao_atual(
            anos,
            meses,
            anos_sit_atual,
            meses_sit_atual,
            rs,
            raz_social,
            sit_atual,
            sit_debito,
            ms,
            inst,
            radio_value,
            finaliz,
            fora,
    ):
        input_dict = {
            'razao_social': rs,
            'razao_social_process': raz_social,
            'desc_sit_atual': sit_atual,
            'situacao_debito': sit_debito,
            'mudanca_status': ms,
            'instancia': inst,
            'flag_sit_terminativa': finaliz,
            'flag_sit_fora_caf': fora,
        }
        df = df_com_filtros(
            anos, meses, anos_sit_atual, meses_sit_atual, input_dict
        )

        if radio_value == 'intervalo':
            df = df.query('dias_sit_atual_lavr >= 1500').nsmallest(
                50, 'data_lavratura'
            )
            chart_title = (
                'Processos com diferença entre datas ' 'acima de 1500 dias'
            )
        else:
            df = df.sort_values('data_sit_atual').head(50)
            chart_title = 'Processos com data de situação mais antigas'

        df = df.reindex(index=df.index[::-1])

        chart_height = len(df) * 20 if (len(df) * 20) > 420 else 580

        fig = dot_line(
            df.data_lavratura,
            df.razao_social_process,
            df.data_sit_atual,
            df.razao_social_process,
            chart_height,
        )
        return fig

    @app.callback(
        Output('tabs-caf-conteudo', 'children'),
        Input('tabs-caf', 'value'),
        Input('slide-anos', 'value'),
        Input('slide-meses', 'value'),
        Input('slide-anos-sit-atual', 'value'),
        Input('slide-meses-sit-atual', 'value'),
        Input('drop-razao-social', 'value'),
        Input('drop-razao-social-processo', 'value'),
        Input('drop-situacao-atual', 'value'),
        Input('drop-situacao-debito', 'value'),
        Input('drop-mudanca-status', 'value'),
        Input('drop-instancia', 'value'),
        Input('drop-finalizado', 'value'),
        Input('drop-fora-caf', 'value'),
    )
    def tabs_detalhe_processos(
            tab,
            anos,
            meses,
            anos_sit_atual,
            meses_sit_atual,
            rs,
            raz_social,
            sit_atual,
            sit_debito,
            ms,
            inst,
            finaliz,
            fora,
    ):

        input_dict = {
            'razao_social': rs,
            'razao_social_process': raz_social,
            'desc_sit_atual': sit_atual,
            'situacao_debito': sit_debito,
            'mudanca_status': ms,
            'instancia': inst,
            'flag_sit_terminativa': finaliz,
            'flag_sit_fora_caf': fora,
        }
        df = df_com_filtros(
            anos, meses, anos_sit_atual, meses_sit_atual, input_dict
        )

        if tab == 'tab-1':
            df = df[
                [
                    'cd_processo',
                    'razao_social',
                    'data_lavratura',
                    'data_sit_atual',
                    'valor_total',
                    'dias_sit_atual_lavr',
                ]
            ]
            df.sort_values('data_lavratura', ascending=False, inplace=True)

            for col in ['data_lavratura', 'data_sit_atual']:
                df[col] = df[col].dt.strftime('%Y/%m/%d')

            df.columns = [
                'Cód',
                'Razão Social',
                'Lavratura',
                'Últ. moviment.',
                'Valor',
                'Duração (média, em dias)',
            ]

            return tab_razao_social(df)
        elif tab == 'tab-2':
            df_to_table = df_com_totais(
                df,
                ['desc_sit_atual'],
                {'cd_processo': 'count', 'valor_total': 'sum'},
                'cd_processo',
                ['Situação Atual', '% de Process.', 'Qtd Process.', 'Valor'],
            )
            return tab_ranking(df_to_table)
