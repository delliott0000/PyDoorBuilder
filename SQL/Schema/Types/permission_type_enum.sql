DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'permission_type') THEN
        CREATE TYPE permission_type AS ENUM (
        'create',
        'preview',
        'view',
        'acquire',
        'update',
        'generate',
        'delete',
        'reassign'
    );
    END IF;
END
$$;