-- ADD NEW COLUMN TO STORE TIMESTAMP
alter table symbol_prices.symbol_five_mins
add column time_stamp int after symbol_id;

-- INSERT VALUES INTO TIMESTAMP COLUMN
update symbol_prices.symbol_five_mins
join symbol_prices.five_mins
on symbol_prices.symbol_five_mins.five_min_start_id = symbol_prices.five_mins.id
set symbol_prices.symbol_five_mins.time_stamp=symbol_prices.five_mins.five_min_start
where symbol_prices.symbol_five_mins.five_min_start_id = symbol_prices.five_mins.id;

alter table symbol_prices.symbol_five_mins
drop column five_min_start_id;