import dash_bootstrap_components as dbc
from dash import html

from app.dashboards.monitoramento.data import Dataset

data = Dataset()


def gera_cartoes(setor, concluidas, strat, seplag, pnafm, op):
    objetivos = data.dimensoes(setor=setor)

    if concluidas == "Não":
        cods = [cod for cod in objetivos['CD_OBJETIVO']
                if not data.info_objetivo(cod)['obj_status']]
    elif concluidas == '2022':
        cods = [cod for cod in objetivos['CD_OBJETIVO']
                if data.info_objetivo(cod)['obj_status']
                and data.info_objetivo(cod)['dt_max_tarefa_finaliz'].year ==
                2022
                ]
    elif concluidas == '2021':
        cods = [cod for cod in objetivos['CD_OBJETIVO']
                if data.info_objetivo(cod)['obj_status']
                and data.info_objetivo(cod)['dt_max_tarefa_finaliz'].year ==
                2021
                ]

    if strat == "SIM":
        cods = [cod for cod in cods if data.info_objetivo(cod)['estrat']]

    if seplag == "SIM":
        cods = [cod for cod in cods if data.info_objetivo(cod)['seplag']]

    if pnafm == "SIM":
        cods = [cod for cod in cods if data.info_objetivo(cod)['pnafm']]

    if op == "SIM":
        cods = [cod for cod in cods if data.info_objetivo(cod)['operacional']]

    cartoes, cartoes_bid = list(), list()
    for id_card, cd_obj in enumerate(cods):
        infos = data.info_objetivo(cd_obj)
        cartao = cartao_objetivo(id_card, infos)

        if "bid" in cartao.key:
            cartoes_bid.append(dbc.Col(cartao))
        else:
            cartoes.append(dbc.Col(cartao))

    class_name = "row row-cols-lg-3 row-cols-md-1 row gy-4 py-2"
    active_tab_class_name = "fw-bold fst-italic"
    if setor == "TRIBUTAÇÃO":
        tabs = dbc.Tabs(
            [
                dbc.Tab(
                    dbc.Row(cartoes_bid, className=class_name),
                    label="BID",
                    activeTabClassName=active_tab_class_name
                ),
                dbc.Tab(
                    dbc.Row(cartoes, className=class_name),
                    label="Outros Objetivos",
                    activeTabClassName=active_tab_class_name
                ),
            ],
            id="tab-tesouro",
            persistence=True
        )
        return tabs
    else:
        return dbc.Row(cartoes, className=class_name)


def cartao_objetivo(id_card, infos):
    if infos['obj_status']:
        cor = "success"
        btn_txt = "Finalizado"
        outline = True
    elif infos['suspenso']:
        cor = "secondary",
        btn_txt = "Suspenso"
        outline = False
    else:
        cor = "primary"
        btn_txt = "Ver Ações e Tarefas"
        outline = True

    total_tarefas = f"{infos['total_tarefas']} tarefas"
    status_msg = f"{infos['concluidas']} conc. | " \
                 f"{infos['atrasadas']} atras. | " \
                 f"{infos['andamento']} andam. | " \
                 f"{infos['iniciar']} a iniciar"

    if infos['seplag']:
        badge_seplag = html.H5(dbc.Badge("Seplag", color="secondary"))
    else:
        badge_seplag = None

    if infos['operacional']:
        badge_op = html.H5(dbc.Badge("Operacional", color="secondary"))
    else:
        badge_op = None

    if infos['estrat']:
        badge_estrat = html.H5(dbc.Badge("Estratégico", color="secondary")
                               )
    else:
        badge_estrat = None

    if infos['operacional']:
        badge_op = html.H5(dbc.Badge("Operacional", color="secondary"))
    else:
        badge_op = None

    if infos['pnafm']:
        badge_pnafm = html.H5(dbc.Badge("PNAFM", color="secondary")
        )
    else:
        badge_pnafm = None

    if infos['bid']:
        badge_bid = html.H5(dbc.Badge("BID", color="secondary")
        )
    else:
        badge_bid = None

    card = dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H5(infos['objetivo']),
                    html.Hr(),
                    html.H5(total_tarefas),
                    html.H6(status_msg),
                    html.Div(
                        dbc.Button(btn_txt,
                                   color=cor,
                                   outline=outline,
                                   id={'type': 'button-html',
                                       'index': id_card},
                                   key=infos['codigo'],
                                   n_clicks=0)
                    )
                ]
            ),
            dbc.CardFooter([
                html.H6(f"Prev. Início: {infos['prev_inicio']}"),
                html.H6(f"Prev. Término: {infos['prev_termino']}"),
                badge_seplag,
                badge_estrat,
                badge_pnafm,
                badge_op
            ])
        ],
        color=cor,
        outline=True,
        id=infos['codigo'],
        key=f"{infos['codigo']}{'-bid' if badge_bid else ''}"
        # style={"width": 300},
    )
    return card
