from dash import html
import dash_bootstrap_components as dbc
from app.dashboards.central import comps
from app.dashboards.utils import components

layout = html.Div([
    components.navbar,
    dbc.Container([
        dbc.Row(comps.intro),
        dbc.Row(comps.accor),
    ], style={
        "marginTop": 25, "marginBottom": 25
    }),
    components.footer
])
