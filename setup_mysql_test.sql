-- MySQL Script that prepares the server for this project

-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS hbnb_test_db;
-- Create the user if it doesn't exist and set the password
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';
-- Grant all privileges on hbnb_test_db to hbnb_test
GRANT ALL on hbnb_test_db.* TO 'hbnb_test'@'localhost';
-- Grant SELECT privilege on performance_schema to hbnb_test
GRANT SELECT on performance_schema.* TO 'hbnb_test'@'localhost';
