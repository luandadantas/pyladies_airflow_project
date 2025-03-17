import requests
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import unquote

from airflow.models import DAG
from airflow.decorators import task
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook


_CONN_ID = "my_postgres_conn"
_SCHEMA = "diarios_schema"
_TABLE = "mossoro_table"

with DAG(
    dag_id="diario_mossoro_dag",
    start_date=datetime(2022, 1, 1),
    schedule='@daily',
    catchup=False,
    template_searchpath=['include'],
) as dag:
    
    _create_table = SQLExecuteQueryOperator(
        task_id="create_table",
        conn_id=_CONN_ID,
        sql="create_table.sql",
        params={"schema": _SCHEMA, "table": _TABLE},
    )
    
    @task
    def extract():
        # Faz o  download de todas as edições do diário da primeira página
        response = requests.get("https://dom.mossoro.rn.gov.br/dom/edicoes")

        return response.text


    @task
    def transform(response_text):
        html_page = BeautifulSoup(response_text, 'html.parser')
        edicao_list = html_page.find('div', class_="edicoes-list")
    
        transformed_data = []
        for edicao in edicao_list.find_all("div", class_="edicao"):
            # url completa: https://dom.mossoro.rn.gov.br/pmm/uploads/publicacao/pdf/1281/DOM_-_N_308_-_Segunda-Feira%2C_08_de_Abril_de_2024.pdf
            
            numero_edicao = edicao.find('img').get('alt')
            print(numero_edicao)

            url_base = "https://dom.mossoro.rn.gov.br/pmm/uploads/publicacao/pdf"
            url_file_name = edicao.find('img').get('src').split('thumb')[-1].split('.png')[0]

            url_edicao = f"{url_base}{url_file_name}.pdf"
            url_edicao = unquote(url_edicao)
            print(url_edicao)

            file_name = f"{url_file_name.split('/')[-1]}.pdf"
            file_name = unquote(file_name)
            print(file_name)

            transformed_data.append({
                'numero_edicao': numero_edicao,
                'nome_documento': file_name,
                'url_edicao': url_edicao,
            })

        return transformed_data


    @task
    def load(transformed_data):
        hook = PostgresHook(postgres_conn_id=_CONN_ID)

        sql = f"""
        INSERT INTO {_SCHEMA}.{_TABLE} (numero_edicao, nome_documento, url_edicao)
        VALUES (%s, %s, %s)
        ON CONFLICT DO NOTHING
        """
        
        conn = hook.get_conn()
        cursor = conn.cursor()

        for item in transformed_data:
            data = (item['numero_edicao'], item['nome_documento'], item['url_edicao'])
            cursor.execute(sql, data)

        conn.commit()
        cursor.close()
        conn.close()


    _extract = extract()
    _transform = transform(response_text=_extract)
    _load = load(transformed_data=_transform)

    _create_table >> _extract >> _transform >> _load
