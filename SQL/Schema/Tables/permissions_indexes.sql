CREATE INDEX IF NOT EXISTS idx_permissions_team_id ON permissions(team_id);

CREATE UNIQUE INDEX IF NOT EXISTS unique_idx_scope_null ON permissions (team_id, permission_type)
WHERE permission_type = 'create' AND permission_scope IS NULL;

CREATE UNIQUE INDEX IF NOT EXISTS unique_idx_scope_not_null ON permissions (team_id, permission_type, permission_scope)
WHERE permission_type <> 'create' AND permission_scope IS NOT NULL;