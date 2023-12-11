from dash import html, dcc
from app.dashboards.utils import components
from app.dashboards.pnafm.components import dcc_embed

margens_div_principais = {'marginTop': 25, 'marginBottom': 35}

layout = html.Div([
    components.navbar,
    dcc.Loading(
        id="loading",
        type="circle",
    ),
    html.Iframe(
        id="datastudio-dashboard",
        src="https://lookerstudio.google.com/embed/reporting/ae144129-aec1-4b65-8220-6c5aa61302e9/page/Du4PD",
        style={"height": "1067px", "width": "100%"},
    ),
    components.footer,
])
