
from app.dashboards.pnafm.components import dcc_embed, html_div
from dash import Input, Output

def callbacks(app):
    @app.callback(
    Output("datastudio-dashboard", "children"),
    Input("datastudio-url", "value"),
    )
    def update_datastudio_dashboard(datastudio_url):
        if datastudio_url is not None:
            return dcc_embed(
                id="datastudio-embed",
                url=datastudio_url,
                width="100%",
                height="600px",
            )
        else:
            return html_div()