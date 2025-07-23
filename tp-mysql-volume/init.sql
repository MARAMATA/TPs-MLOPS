USE testdb;

CREATE TABLE IF NOT EXISTS users_testing (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100)
);

INSERT INTO users_testing (name) VALUES ('Bob'), ('Alice');
