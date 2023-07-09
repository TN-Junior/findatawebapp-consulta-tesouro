from dash import callback_context, Input, Output, State, ALL
from app.dashboards.monitoramento.graficos.cartoes import gera_cartoes
from app.dashboards.monitoramento.graficos.modais import gera_modal


def callbacks(app):
    @app.callback(
        Output("modal-obj", "children"),
        [Input({"type": "button-html", "index": ALL}, "n_clicks"),
         Input({"type": "button-html", "index": ALL}, "key")],
        State("modal", "is_open")
    )
    def exibe_modal(click, key, is_open):
        ctx = callback_context
        if sum(click):
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]
            obj_id = (key[eval(button_id)["index"]])
            return gera_modal(not is_open, obj_id)
        else:
            return gera_modal(is_open, None)

    @app.callback(
        Output("cards-obj", "children"),
        [Input("drop-setor", "value"),
         Input("drop-concluidas", "value"),
         Input("drop-estrategia", "value"),
         Input("drop-seplag", "value"),
         Input("drop-pnafm", "value"),
         Input("drop-operacional", "value")]
    )
    def cards_objetivos(setor, concluidas, strat, seplag, pnafm, op):
        return gera_cartoes(setor, concluidas, strat, seplag, pnafm, op)

    @app.callback(
        Output("drop-operacional", "disabled"),
        Input("drop-setor", "value")
    )
    def disable_operacional_dropdown(value):
        if value != "TRIBUTAÇÃO":
            return True
