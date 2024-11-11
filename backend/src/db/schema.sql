DROP TABLE IF EXISTS users, rides, riders CASCADE;

CREATE TABLE users(
    id SERIAL PRIMARY KEY NOT NULL,
    name VARCHAR(255) NOT NULL,
    special_instructions VARCHAR(255) DEFAULT 'No special instructions',
    average_rating REAL DEFAULT 0,
    car_make VARCHAR(255),
    car_model VARCHAR(255),
    date_started TIMESTAMP,
    license_number VARCHAR(255),
    credit_number BIGINT,
    zip_code INTEGER DEFAULT 0,
    location_lat DECIMAL,
    location_long DECIMAL,
    is_driver BOOL NOT NULL,
    userID VARCHAR(255) NOT NULL
);

CREATE TABLE rides(
    id SERIAL PRIMARY KEY NOT NULL,
    driver_id INTEGER references users(id) ON DELETE CASCADE,
    dest_lat DECIMAL,
    dest_long DECIMAL,
    special_instructions VARCHAR(255),
    time TIMESTAMP,
    driver_rating VARCHAR(255),
    cost DECIMAL
);

CREATE TABLE riders(
    id SERIAL PRIMARY KEY NOT NULL,
    rider_id INTEGER references users(id) ON DELETE CASCADE,
    ride_id INTEGER references rides(id) ON DELETE CASCADE,
    review VARCHAR(255),
    driver_response VARCHAR(255),
    rating REAL,
    receipt REAL
);