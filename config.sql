-- auto-generated definition
create user odoo11
    superuser
    createdb
    createrole;

CREATE ROLE postgres LOGIN PASSWORD 'password';

create database dump;

\c dump
