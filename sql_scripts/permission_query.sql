-- Consulta sobre roles de un usuario
SELECT rolname, rolsuper, rolinherit, rolcreaterole, rolcreatedb, rolcanlogin
FROM pg_roles
WHERE rolname = 'lucel_dasilva';


-- Consulta para Ver Privilegios sobre Tablas
SELECT 
    grantee, 
    table_schema, 
    table_name, 
    privilege_type
FROM 
    information_schema.role_table_grants
WHERE 
    grantee = 'lucel_dasilva'
    AND table_schema = 'public';