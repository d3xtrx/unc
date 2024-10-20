CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    sentiment INT,
    avatar INT,
    avatar_name VARCHAR(50),
    weight INT,
    calories_burned DECIMAL(10, 2)
);

CREATE TABLE shop (
    item_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(50),
    price DECIMAL(10, 2),
    image_url VARCHAR(255)
);

CREATE TABLE exercises (
    exercise_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    exercise_type VARCHAR(50),
    duration INTEGER NOT NULL  -- Duration in minutes
);

INSERT INTO users (username, first_name, last_name)
VALUES
    ('testuser6',   'Test', 'User6')
ON CONFLICT (username) DO NOTHING;

INSERT INTO shop (name, description, category, price, image_url)
VALUES
    ('pink unc', 'unc but pink', 'avatar', '10', 'img/2Pink.png'),
    ('blue unc', 'unc but blue', 'avatar', '10', 'img/2Blue.png'),
    ('green unc', 'unc but green', 'avatar', '10', 'img/2Green.png'),
    ('purple unc', 'unc but purple', 'avatar', '10', 'img/2Purple.png'),
    ('red unc', 'unc but red', 'avatar', '10', 'img/2Red.png'),
    ('yellow unc', 'unc but yellow', 'avatar', '10', 'img/2Yellow.png'),
    ('jeff', 'head empty, no thoughts', 'avatar', '10', 'img/2AltPink.png')
