create table transactions (
WEEK_END_DATE date,
STORE_NUM BIGINT,
UPC BIGINT,
UNITS INT,
VISITS INT,
HHS INT,
SPEND FLOAT,
PRICE FLOAT,
BASE_PRICE FLOAT,
FEATURE INT,
DISPLAY INT,
TPR_ONLY INT);


COPY transactions(WEEK_END_DATE,STORE_NUM,UPC,UNITS,VISITS,HHS,SPEND,PRICE,BASE_PRICE,FEATURE,DISPLAY,TPR_ONLY) from '/home/olksndr/project/transactions.csv' DELIMITER ',' CSV HEADER;

create table products (U
PC BIGINT, 
DESCRIPTION TEXT, 
MANUFACTURER TEXT, 
CATEGORY TEXT, 
SUB_CATEGORY TEXT,
PRODUCT_SIZE TEXT);


COPY transactions(UPC,DESCRIPTION,MANUFACTURER,CATEGORY,SUB_CATEGORY,PRODUCT_SIZE) from '/home/olksndr/project/transactions.csv' DELIMITER ',' CSV HEADER;

select * from transactions LEFT JOIN products on transactions.UPC = products.UPC limit 25 ## left join


SELECT (store_num, SUM(spend)) from transactions where upc = 1111009477 GROUP BY store_num order by SUM(spend) desc;

