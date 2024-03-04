
/* 
se déplacer dans la base mysql
cd /usr/local/mysql/bin
./mysql -uroot -p

*/

/*afficher la liste des bases de données */
show databases;

/*selection une base de données */
use churn_finance;

/* Afficher la liste des tables */
show tables;



-- CREATE TABLE tasks (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     task VARCHAR(255) NOT NULL
-- );


CREATE TABLE churn (
    RowNumber INT AUTO_INCREMENT PRIMARY KEY,
    CustomerId VARCHAR(255),
    Surname VARCHAR(255),
    CreditScore INT,
    Geography VARCHAR(255),
    Gender VARCHAR(255),
    Age INT,
    Tenure INT,
    Balance FLOAT,
    NumOfProducts INT,
    HasCrCard INT,
    IsActiveMember INT,
    EstimatedSalary FLOAT,
    Exited INT
);


