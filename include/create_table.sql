CREATE SCHEMA IF NOT EXISTS {{ params.schema }};

CREATE TABLE IF NOT EXISTS {{ params.schema }}.{{ params.table }} (
    numero_edicao TEXT NOT NULL,
    nome_documento TEXT NOT NULL,
    url_edicao TEXT NOT NULL,
    PRIMARY KEY (numero_edicao, nome_documento, url_edicao)
);
