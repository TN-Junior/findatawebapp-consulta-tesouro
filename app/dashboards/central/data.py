# import locale
from datetime import datetime
import pandas as pd

# locale.setlocale(locale.LC_ALL, 'pt_BR')

prefix_arquivos = 'app/dashboards/_datasets/central_previsoes/'
arquivo_data_ref = f'{prefix_arquivos}data_ref.txt'

with open(arquivo_data_ref, 'r') as f:
    d = f.readlines()[0]

data_ref = datetime.strptime(d, '%m/%Y')
data_ref_str = data_ref.strftime('%b/%y').capitalize()

df_pf = pd.read_parquet(f'{prefix_arquivos}pf.parquet.gzip')
df_ggaf = pd.read_parquet(f'{prefix_arquivos}ggaf.parquet.gzip')
df_rri = pd.read_parquet(f'{prefix_arquivos}rri.parquet.gzip')
df_rcl = pd.read_parquet(f'{prefix_arquivos}rcl.parquet.gzip')
df_liquidez = pd.read_parquet(f'{prefix_arquivos}liquidez.parquet.gzip')


def formatacao_cabecalho(n):
    meses = [
        'Janeiro',
        'Fevereiro',
        'Março',
        'Abril',
        'Maio',
        'Junho',
        'Julho',
        'Agosto',
        'Setembro',
        'Outubro',
        'Novembro',
        'Dezembro',
    ]
    formatacao = [
        {
            'if': {'column_id': meses[: n - 1]},
            'color': 'gray',
        }
    ]
    return formatacao


estilo_cabecalho = formatacao_cabecalho(data_ref.month)
