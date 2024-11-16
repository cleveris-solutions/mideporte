-- Drop databases if they exist
DROP DATABASE IF EXISTS mideportedb;
DROP DATABASE IF EXISTS mideportedb_test;

-- Create databases
CREATE DATABASE mideportedb;
CREATE DATABASE mideportedb_test;

-- Drop user if exists and create new one
DROP USER IF EXISTS 'mideporte_user'@'localhost';
CREATE USER 'mideporte_user'@'localhost' IDENTIFIED BY 'mideporte_password';

-- Set privileges over databases
GRANT ALL PRIVILEGES ON mideportedb.* TO 'mideporte_user'@'localhost';
GRANT ALL PRIVILEGES ON mideportedb_test.* TO 'mideporte_user'@'localhost';

-- Apply changes
FLUSH PRIVILEGES;
