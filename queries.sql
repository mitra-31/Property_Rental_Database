CREATE DATABASE propertyrental;


CREATE TABLE properties(
p_id INT NOT NULL AUTO_INCREMENT,
p_sellername VARCHAR(45),
p_address VARCHAR(220),
p_city VARCHAR(20),
p_state VARCHAR(20),
p_zipcode VARCHAR(20),
p_images VARCHAR(220),
p_cost VARCHAR(100),
p_thumbnail VARCHAR(45),
p_status VARCHAR(10),
PRIMARY KEY (p_id));

CREATE TABLE sold_properties(
sp_id INT NOT NULL AUTO_INCREMENT,
user_id INT ,
p_id INT,
date_solded_out DATE,
PRIMARY KEY(sp_id));

CREATE TABLE users(
user_id INT NOT NULL AUTO_INCREMENT,
user_name VARCHAR(20),
email_id VARCHAR(100),
phone BIGINT,
adress VARCHAR(100),
city VARCHAR(45)
password VARCHAR(100),
PRIMARY KEY(user_id));