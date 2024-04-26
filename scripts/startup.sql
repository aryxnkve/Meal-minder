-- create database nutribuddy;


drop table weekly_calories;
drop table preferences;
drop table users CASCADE;

create table users(
	ID serial primary key,
	username varchar(50) unique not null,
	enc_password varchar(200) not null,
	first_name varchar(100) not null,
	last_name varchar(100) not null,
	age integer not null,
	gender varchar(20) not null,
	height integer not null,
	weight integer not null,
	activity_level varchar(100) not null,
	calorie_goal integer not null,
	bmi decimal not null
	
);


create table preferences(
	preference_id serial primary key,
	user_id integer not null,
	is_vegetarian boolean,
	cuisine varchar(255),
	dishes varchar(255),
	ingredients varchar(255),
	allergies varchar(255),
	CONSTRAINT fk_user
      FOREIGN KEY(user_id) 
        REFERENCES users(ID)
);


create table weekly_calories(
	weekly_calories_id serial primary key,
	user_id integer not null,
	dish_name varchar(255),
	file_link varchar(255),
	calories integer,
	timestamp timestamp,
	CONSTRAINT fk_user
      FOREIGN KEY(user_id) 
        REFERENCES users(ID)
);



INSERT INTO users (
	ID,
    username,
    enc_password,
    first_name,
    last_name,
    age,
    gender,
    height,
    weight,
    activity_level,
    calorie_goal,
    bmi
) VALUES (
	91,
    'sayali@gmail.com',
    '$2b$12$l1O0mnbJXrK9OKou9rT9XuzfJZTetIAtqGpvSPijiSyWyzLdDD8Mm',
    'Sayali',
    'Dalvi',
    26,
    'Female',
    161,
    69,
    '🧘 Lightly active',
    1906,
    26.61934338952972
);

insert into preferences(
	preference_id,
	user_id,
	is_vegetarian,
	cuisine,
	dishes,
	ingredients,
	allergies)
	values(
	1,
	91,
	false,
	'Indian, Mexican',
	'Curry, Pizza, Biryani',
	'Chicken, Onions, Tomatoes',
	'');
	
insert into weekly_calories(
	user_id,
	dish_name,
	file_link,
	calories,
	timestamp
) values(
	91, 'Chicken Tikka Masala', 'https://storage.cloud.google.com/bdia-bucket/images/20240425143613_a726ce46-7acd-4e97-8220-8791120326d3.png', 800, '2024-04-22 18:10:57'
);

insert into weekly_calories(
	user_id,
	dish_name,
	file_link,
	calories,
	timestamp
) values(
	91, 'Avacado Toast', 'https://storage.cloud.google.com/bdia-bucket/images/20240425143613_a726ce46-7acd-4e97-8220-8791120326d3.png', 270, '2024-04-23 07:10:57'
);

insert into weekly_calories(
	user_id,
	dish_name,
	file_link,
	calories,
	timestamp
) values(
	91, 'Cheese Burger', 'https://storage.cloud.google.com/bdia-bucket/images/20240425143613_a726ce46-7acd-4e97-8220-8791120326d3.png', 1126, '2024-04-23 07:10:57'
);

insert into weekly_calories(
	user_id,
	dish_name,
	file_link,
	calories,
	timestamp
) values(
	91, 'Avocado Salad', 'https://storage.cloud.google.com/bdia-bucket/images/20240425143613_a726ce46-7acd-4e97-8220-8791120326d3.png', 945, '2024-04-24 23:10:57'
);

insert into weekly_calories(
	user_id,
	dish_name,
	file_link,
	calories,
	timestamp
) values(
	91, 'Creamy Chicken Pasta with Broccoli', 'https://storage.cloud.google.com/bdia-bucket/images/20240425143613_a726ce46-7acd-4e97-8220-8791120326d3.png', 1002, '2024-04-24 23:10:57'
);

insert into weekly_calories(
	user_id,
	dish_name,
	file_link,
	calories,
	timestamp
) values(
	91, 'Pepperoni Pizza', 'https://storage.cloud.google.com/bdia-bucket/images/20240425143613_a726ce46-7acd-4e97-8220-8791120326d3.png', 800, '2024-04-25 23:10:57'
);

insert into weekly_calories(
	user_id,
	dish_name,
	file_link,
	calories,
	timestamp
) values(
	91, 'Oreo Sundae', 'https://storage.cloud.google.com/bdia-bucket/images/20240425143613_a726ce46-7acd-4e97-8220-8791120326d3.png', 804, '2024-04-25 23:10:57'
);

insert into weekly_calories(
	user_id,
	dish_name,
	file_link,
	calories,
	timestamp
) values(
	91, 'Cheese Burger', 'https://storage.cloud.google.com/bdia-bucket/images/20240425143613_a726ce46-7acd-4e97-8220-8791120326d3.png', 1126, '2024-04-25 07:10:57'
);


select * from users;
select * from preferences;
select * from weekly_calories;





