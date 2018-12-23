CREATE TABLE symbol_prices.`Earliest_latest` (
  `earliest_5start` int(11) DEFAULT NULL,
  `latest_5start` int(11) DEFAULT NULL,
  `latest_5start_as_string` datetime DEFAULT NULL,
  `earliest_5start_as_string` datetime DEFAULT NULL
);

CREATE TABLE symbol_prices.`Five_mins` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `five_min_start` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `five_min_start` (`five_min_start`)
);

CREATE TABLE symbol_prices.`Symbol` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `symbol` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `symbol` (`symbol`)
);

CREATE TABLE symbol_prices.`Symbol_five_mins` (
	`symbol_id` int(11) NOT NULL,  
	`five_min_start_id` int(11) NOT NULL,
	`open` double DEFAULT NULL, 
	`high` double DEFAULT NULL,  
	`low` double DEFAULT NULL,  
	`close` double DEFAULT NULL,
	`volume` int(11) DEFAULT NULL,
	PRIMARY KEY (`symbol_id`,`five_min_start_id`)
);

LOAD DATA INFILE '/var/lib/mysql-files/earliest_latest.csv' 
INTO TABLE symbol_prices.Earliest_latest
FIELDS TERMINATED BY ';' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA INFILE '/var/lib/mysql-files/five_mins.csv' 
INTO TABLE symbol_prices.Five_mins
FIELDS TERMINATED BY ';' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA INFILE '/var/lib/mysql-files/symbol.csv' 
INTO TABLE symbol_prices.Symbol
FIELDS TERMINATED BY ';' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA INFILE '/var/lib/mysql-files/symbol_five_mins.csv' 
INTO TABLE symbol_prices.Symbol_five_mins
FIELDS TERMINATED BY ';' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;


-- ADD NEW COLUMN TO STORE TIMESTAMP
alter table symbol_prices.Symbol_five_mins
add column time_stamp int after symbol_id;

-- INSERT VALUES INTO TIMESTAMP COLUMN
update symbol_prices.Symbol_five_mins
join symbol_prices.Five_mins
on symbol_prices.Symbol_five_mins.five_min_start_id = symbol_prices.Five_mins.id
set symbol_prices.Symbol_five_mins.time_stamp=symbol_prices.Five_mins.five_min_start
where symbol_prices.Symbol_five_mins.five_min_start_id = symbol_prices.Five_mins.id;

alter table symbol_prices.Symbol_five_mins
drop primary key,
add primary key(symbol_id, time_stamp);

alter table symbol_prices.Symbol_five_mins
drop column five_min_start_id;

update symbol_prices.Symbol_five_mins
set symbol_prices.Symbol_five_mins.symbol_id = 9
where symbol_prices.Symbol_five_mins.symbol_id = 1403;