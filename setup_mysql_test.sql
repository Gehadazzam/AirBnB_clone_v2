-- Write a script that prepares a MySQL server for the project:
-- A database hbnb_test_db
CREATE DATABASE IF NOT EXISTS hbnb_test_db;
-- A new user hbnb_test (in localhost)
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost'
-- The password of hbnb_test should be set to hbnb_test_pwd
IDENTIFIED BY 'hbnb_test_pwd';
-- hbnb_test should have all privileges on the database hbnb_test_db (and only this database)
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';
-- hbnb_test should have SELECT privilege on the database performance_schema (and only this database)
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost';
-- If the database hbnb_test_db or the user hbnb_test already exists, your script should not fail
FLUSH PRIVILEGES;
