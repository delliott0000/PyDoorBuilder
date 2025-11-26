DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'permission_scope') THEN
        CREATE TYPE permission_scope AS ENUM (
        'safe',
        'company',
        'universal'
    );
    END IF;
END
$$;