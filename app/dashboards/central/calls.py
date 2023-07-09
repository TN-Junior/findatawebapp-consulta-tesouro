from dash import Input, Output


def client_calls(app):
    app.clientside_callback(
        """
        function(n_clicks) {
            if (n_clicks > 0)
                document.querySelector("#tabela-painel-fiscal button.export").click()
            return ""
        }
        """,
        Output("btn-painel-fiscal", "data-btn-painel-fiscal"),
        [Input("btn-painel-fiscal", "n_clicks")],
    )

    app.clientside_callback(
        """
        function(n_clicks) {
            if (n_clicks > 0)
                document.querySelector("#tabela-ggaf button.export").click()
            return ""
        }
        """,
        Output("btn-ggaf", "data-btn-ggaf"),
        [Input("btn-ggaf", "n_clicks")],
    )

    app.clientside_callback(
        """
        function(n_clicks) {
            if (n_clicks > 0)
                document.querySelector("#tabela-rri button.export").click()
            return ""
        }
        """,
        Output("btn-rri", "data-btn-rri"),
        [Input("btn-rri", "n_clicks")],
    )

    app.clientside_callback(
        """
        function(n_clicks) {
            if (n_clicks > 0)
                document.querySelector("#tabela-rcl button.export").click()
            return ""
        }
        """,
        Output("btn-rcl", "data-btn-rcl"),
        [Input("btn-rcl", "n_clicks")],
    )

    app.clientside_callback(
        """
        function(n_clicks) {
            if (n_clicks > 0)
                document.querySelector("#tabela-liquidez button.export").click()
            return ""
        }
        """,
        Output("btn-liquidez", "data-btn-liquidez"),
        [Input("btn-liquidez", "n_clicks")],
    )
