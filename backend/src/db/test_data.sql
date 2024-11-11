INSERT INTO users (name, special_instructions, average_rating, is_driver, userID)
VALUES ('Tom Magliozzi', 'Don''t drive like my brother', 3.2, true, 'Tom123');

INSERT INTO users (name, special_instructions, average_rating, is_driver, userID)
VALUES ('Ray Magliozzi', 'Don''t drive like my brother', 3.4, true, 'Ray456');

INSERT INTO users (name, average_rating, is_driver, userID)
VALUES ('Mike Easter', 4.3, false, 'michael78');

INSERT INTO users (name, average_rating, is_driver, userID)
VALUES ('Darren Jiang', 5.0, false, 'DJL');

INSERT INTO rides(driver_id, cost)
VALUES(1, 10);

INSERT INTO rides(driver_id, cost)
VALUES(2, 12);

INSERT INTO rides(driver_id, cost)
VALUES(1, 8);

INSERT INTO riders(rider_id, ride_id)
VALUES(3, 1);

INSERT INTO riders(rider_id, ride_id)
VALUES(3, 2);

INSERT INTO riders(rider_id, ride_id)
VALUES(2, 3);

INSERT INTO riders(rider_id, ride_id)
VALUES(4, 1)