#!/bin/bash

set -e

until mysql -h localhost -u root -p${MYSQL_ROOT_PASSWORD} -e 'SELECT 1'; do
    echo "waiting for mysql server to be ready"
    sleep 1
done

mysql -h localhost -u root -p${MYSQL_ROOT_PASSWORD} <<EOF
CREATE DATABASE IF NOT EXISTS ${MYSQL_DB};
USE ${MYSQL_DB};

CREATE TABLE IF NOT EXISTS mysql_model (
    id INT AUTO_INCREMENT PRIMARY KEY,
    data VARCHAR(64)
);

CREATE TABLE IF NOT EXISTS employee (
    employeeNumber INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    position VARCHAR(50),
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS clock_record (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employeeNumber INT,
    clockIn DATETIME,
    clockOut DATETIME,
    update_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (employeeNumber) REFERENCES employee(employeeNumber)
);

EOF

EXIST=$(mysql -h localhost -u root -p${MYSQL_ROOT_PASSWORD} -se "SELECT EXISTS(SELECT 1 FROM mysql.user WHERE user = 'devyang')")

# Create the user if it doesn't exist
if [ "$EXIST" = "0" ]
then
    mysql -h localhost -u root -p${MYSQL_ROOT_PASSWORD} <<EOF
    CREATE USER 'devyang'@'%' IDENTIFIED BY 'devyang';
EOF
fi

# Always grant the permissions to the user
mysql -h localhost -u root -p${MYSQL_ROOT_PASSWORD} <<EOF
GRANT ALL ON ${MYSQL_DB}.* TO 'devyang'@'%';
FLUSH PRIVILEGES;
EOF
