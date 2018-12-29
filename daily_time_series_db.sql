CREATE TABLE `symbol_prices`.`Symbol_daily` (
  `symbol_id` INT NOT NULL,
  `date` DATE NOT NULL,
  `open` DOUBLE NULL,
  `high` DOUBLE NULL,
  `low` DOUBLE NULL,
  `close` DOUBLE NULL,
  `volume` INT(11) NULL,
  PRIMARY KEY (`symbol_id`, `date`));

