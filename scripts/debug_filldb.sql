CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    phone_number VARCHAR(20),
    sentiment INT,
    weight NUMERIC,
    date_recorded TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP WITH TIME ZONE
);

CREATE TABLE shop (
    item_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(50),
    condition VARCHAR(50),
    price DECIMAL(10, 2),
    image_url VARCHAR(255),
);

CREATE TABLE exercises (
    exercise_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    date DATE NOT NULL,
    exercise_type VARCHAR(50) NOT NULL,
    duration INTEGER NOT NULL,  -- Duration in minutes
    calories_burned DECIMAL(10, 2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (username, email, password_hash, first_name, last_name, phone_number)
VALUES
    ('testuser6', 'test6@example.com', 'hashedpassword6', 'Test', 'User6', '1234567895'),
    ('testuser7', 'test7@example.com', 'hashedpassword7', 'Test', 'User7', '1234567896'),
    ('testuser8', 'test8@example.com', 'hashedpassword8', 'Test', 'User8', '1234567897'),
    ('testuser9', 'test9@example.com', 'hashedpassword9', 'Test', 'User9', '1234567898'),
    ('testuser10', 'test10@example.com', 'hashedpassword10', 'Test', 'User10', '1234567899')
ON CONFLICT (username) DO NOTHING;
