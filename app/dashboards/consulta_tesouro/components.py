import dash
from dash import dcc
from dash import html

def dcc_embed(id, url, width, height):
    return dcc.embed(
        id=id,
        url=url,
        width=width,
        height=height,
    )

def html_div(id, style):
    return html.Div(
        id=id,
        style=style,
    )