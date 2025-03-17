Pyladies Airflow Project - ETL Diario Oficial de Mossoró
========

#### Dentro dos slides da apresentação você encontra o tutorial em passos de como criar e rodar esse projeto localmente.

Projeto criado pra uma apresentação no Meetup Pyladies Florianópolis/SC.
Foi construido uma dag chamada `diario_mossoro_dag.py` que faz a raspagem dos Diários Oficiais da primeira página do site (https://dom.mossoro.rn.gov.br/dom/edicoes). 

A dag é dividida em 3 principais passos, o ETL:
- Extract - Uma requisição será feita pra o link acima e vamos raspar tudo que tem nessa página
- Transform - Iremos manipular os dados extraidos e filtar 3 informações de cada diário oficial dessa página:
  - numero_edicao
  - nome_documento
  - url_edicao
- Load - Vamos salvar essas informações transformadas dentro do nosso banco local postgreSQL.



