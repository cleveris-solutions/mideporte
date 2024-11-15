--Drop database if exists
DROP DATABASE IF EXISTS mideportedb;
DROP DATABASE IF EXISTS mideportedb_test;

-- Create database
CREATE DATABASE mideportedb;
CREATE DATABASE mideportedb_test;

-- Create user and password
CREATE USER 'mideporte_user'@'localhost' IDENTIFIED BY 'mideporte_password';

-- Set privileges over databases
GRANT ALL PRIVILEGES ON mideportedb.* TO 'mideporte_user'@'localhost';
GRANT ALL PRIVILEGES ON mideportedb_test.* TO 'mideporte_user'@'localhost';

-- Apply changes
FLUSH PRIVILEGES;
