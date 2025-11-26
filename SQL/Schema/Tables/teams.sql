CREATE TABLE IF NOT EXISTS teams (
    id INT PRIMARY KEY REFERENCES ids(id),
    company_id INT NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    hierarchy_index INT NOT NULL,
    CONSTRAINT unique_company_team_names UNIQUE (company_id, name),
    CONSTRAINT unique_company_team_hierarchy_indexes UNIQUE (company_id, hierarchy_index)
);