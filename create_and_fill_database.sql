create table transactions (
WEEK_END_DATE date,
STORE_NUM INT,
UPC INT,
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



SELECT (store_num, SUM(spend)) from transactions where upc = 1111009477 GROUP BY store_num order by SUM(spend) desc;

