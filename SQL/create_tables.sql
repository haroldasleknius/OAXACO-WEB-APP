CREATE TABLE users (
       user_id serial PRIMARY KEY,
       first_name varchar(45) NOT NULL,
       last_name varchar(45) NOT NULL,
       role varchar(15) NOT NULL,
       username varchar(15) NOT NULL,
       password varchar(100) NOT NULL,
       salt_value varchar(100) NOT NULL;
);

CREATE TABLE complaints (
       complaint_id serial PRIMARY KEY,
       first_name varchar(100) NOT NULL,
       last_name varchar(100) NOT NULL,
       phone_no bigint NOT NULL,
       email varchar(100) NOT NULL,
       complaint_text text NOT NULL
);

CREATE TABLE menu_items (
  	item_id serial PRIMARY KEY,
       item_name varchar(50) NOT NULL,
  	price decimal NOT NULL,
       description text NOT NULL,
  	allergies text NOT NULL,
  	calories int NOT NULL,
       photo_name varchar(50) NOT NULL,
  	item_type varchar(50) NOT NULL
);

CREATE TABLE sales (
	sale_id serial PRIMARY KEY,
       user_id serial references users(user_id),
       total_expense decimal NOT NULL,
       status int NOT NULL,
       order_date DATE DEFAULT CURRENT_DATE,
       order_time TIME DEFAULT CURRENT_TIME,
       delivered bool NOT NULL
);

CREATE TABLE orders (
       order_id serial PRIMARY KEY,
       sale_id serial references sales(sale_id),
       item_id serial references menu_items(item_id),
       time_elapsed TIME NOT NULL,
       quantity int NOT NULL
);

CREATE TABLE tables (
	table_id serial PRIMARY KEY,
       clean bool NOT NULL,
       available bool NOT NULL,
       assistance bool NOT NULL, 
       assigned int references users(user_id),
       seats int NOT NULL,
       customer int references user(user_id)
);

