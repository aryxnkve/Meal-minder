create database nutribuddy;

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

-- insert into users
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
	7,
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

select * from users;

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

insert into preferences(
	preference_id,
	user_id,
	is_vegetarian,
	cuisine,
	dishes,
	ingredients,
	allergies)
	values(
	2,
	7,
	false,
	'Indian, Mexican',
	'Curry, Pizza, Biryani',
	'Chicken, Onions, Tomatoes',
	'');
				

select * from preferences;

-- truncate table preferences;

-- truncate table users CASCADE;

-- drop table preferences;