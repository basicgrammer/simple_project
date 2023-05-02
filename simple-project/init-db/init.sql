grant all privileges on test_db to test;

alter role test_db set client_encoding to 'utf-8'; 
alter database test_db set timezone to 'Asia/Seoul';