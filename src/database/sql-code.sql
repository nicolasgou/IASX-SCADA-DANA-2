/*
Server: MariaDB (mariadb-11.8.2-winx64.msi)
Vizulaizador: HeidiSQL (HeidiSQL_12.4_Portable.zip)
MySQL Clinet: mysql-8.0.33-winx64.msi

Server version: 11.8.2-MariaDB mariadb.org binary distribution
Usuario: root
Senha: T3cn0log!@
*/

-- A aplicacao nao devera criar o banco nem tabelas, somente armazenar as variaveis na estrutura previamente ja criada


CREATE DATABASE scada_dana; --Cria database
USE scada_dana;

CREATE TABLE historico ( --Cria tabela Historico
    time_stamp DATETIME PRIMARY KEY,
    IDProduto VARCHAR(255),
    CODCorrida VARCHAR(255),
    temperatura_forno FLOAT,
    pressao_carga FLOAT,
    corrente_motor FLOAT,
    altura_Matriz FLOAT
);
