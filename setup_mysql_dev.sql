-- MySQL Script that prepares the server for this project

-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;
-- Create the user if it doesn't exist and set the password
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';
-- Grant all privileges on hbnb_dev_db to hbnb_dev
GRANT ALL on hbnb_dev_db.* TO 'hbnb_dev'@'localhost';
-- Grant SELECT privilege on performance_schema to hbnb_dev
GRANT SELECT on performance_schema.* TO 'hbnb_dev'@'localhost';
-- Flush Privileges
FLUSH PRIVILEGES;
