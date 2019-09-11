CREATE DATABASE expenses;
CREATE TABLE transactions(
id INT AUTO_INCREMENT,
amount FLOAT,
category VARCHAR(45),
date_month DATE,
date_transaction DATE,
merchant VARCHAR(45),
card VARCHAR(45),
PRIMARY KEY(id));