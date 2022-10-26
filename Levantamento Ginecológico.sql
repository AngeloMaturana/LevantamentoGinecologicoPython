create database levantamento_ginecologico;
use levantamento_ginecologico;

create table vacas(
Id int not null auto_increment primary key,
Nome varchar(15) not null default'',
Dia_Inseminacao date not null,
Estimativa_Parto date not null
);
select * from vacas;
