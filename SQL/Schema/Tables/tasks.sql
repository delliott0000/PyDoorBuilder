CREATE TABLE IF NOT EXISTS tasks (
    id INT PRIMARY KEY REFERENCES ids(id),
    completed_at TIMESTAMPTZ,
    assigned_to TEXT,
    CONSTRAINT completed_assigned_valid CHECK (
	completed_at IS NULL
	OR
	assigned_to IS NULL
    )
);