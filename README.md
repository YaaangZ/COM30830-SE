# COM30830-SE
Dublin bike group work

# SQL STATEMENT:
-- create database dbbikes

create database if not exists dbbikes;

-- create table station

use dbbikes;
drop table if exists station;
create table station(
	`number` integer not null,
    `name` varchar(128),
    address varchar(128),
    position_lat decimal(8,6),
    position_lng decimal(9,6),
    banking integer,
    bonus integer,
    bike_stands integer,
    primary key(`number`),
    unique(`name`)
);

-- create table availability

drop table if exists availability;
create table availability(
	`number` integer not null,
    available_bike_stands integer,
    available_bikes integer,
    `status` varcharacter(128),
    last_update integer,
    primary key(`number`, last_update)
);

# Environment information
Yang's JCDecaux Key: 92a580e0a48e1f31ade6e2c8c40372a25f10c56e
Yang's Open Weather key: 8f2e40db6b1c4dcc89b68735362dbc56
Yang's RDS endpoint: dbbikes.cqqckwqnmywv.eu-west-1.rds.amazonaws.com
