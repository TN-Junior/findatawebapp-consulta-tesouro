import dash_mantine_components as dmc

from app.dashboards.base_quente.data import dicionario

dic_receita = dicionario()

min_date = dic_receita.data.min()
max_date = dic_receita.data.max()

meses = ["jan", "fev", "mar", "abr", "mai", "jun",
         "jul", "ago", "set", "out", "nov", "dez"]

anos = list(range(2015, max_date.year + 1))

drop_atribuicao = dmc.MultiSelect(
    label="Atribuição",
    placeholder="Atribuição",
    id='drop-atribuicao',
    clearable=True,
    searchable=True,
    data=dic_receita["atribuicao"].unique()
)

drop_grupo_receita = dmc.MultiSelect(
    label="Grupo",
    placeholder="Grupo",
    id='drop-grupo',
    clearable=True,
    searchable=True,
    data=dic_receita["receita_contabil"].unique()
)

drop_nome_receita = dmc.MultiSelect(
    label="Receita Local",
    placeholder="Receita Local",
    id='drop-receita-local',
    clearable=True,
    searchable=True,
    data=dic_receita["cd_nm_receita"].unique()
)

calendar = dmc.DateRangePicker(
    id='calendario-date-range-picker',
    label='Calendário',
    description='Escolha uma data de início e fim para filtrar os dados.',
    placeholder='Selecione datas de início e fim.',
    minDate=min_date,
    maxDate=max_date,
    value=[min_date, max_date],
    inputFormat='DD/MM/YYYY',
    firstDayOfWeek='sunday',
    hideWeekdays=False,
    clearable=False
)

alerta_tabela = dmc.Alert(
    "Realize filtros com intervalo maior a 2 anos para gerar tabela "
    "comparativa.",
    title="Atenção:",
)
