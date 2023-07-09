from app.dashboards.base_quente.calls.filtros import filtros
from app.dashboards.base_quente.calls.kpis import kpis
from app.dashboards.base_quente.calls.barras import barras
from app.dashboards.base_quente.calls.linhas import linhas
from app.dashboards.base_quente.calls.tabelas import tabelas
from app.dashboards.base_quente.calls.rajada import rajada


def callbacks(app):
    filtros(app)
    kpis(app)
    barras(app)
    linhas(app)
    tabelas(app)
    rajada(app)