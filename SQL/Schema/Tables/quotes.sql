CREATE TABLE IF NOT EXISTS quotes (
    id INT PRIMARY KEY REFERENCES ids(id),
    owner_id INT REFERENCES users(id)
);