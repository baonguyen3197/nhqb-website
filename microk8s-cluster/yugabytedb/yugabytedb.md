## --- Exec --- ##

microk8s kubectl exec -n yugabytedb -it yb-tserver-0 -- ysqlsh -h yb-tserver-0.yb-tservers.yugabytedb

## --- CMD --- ##
# List tables
\l

# List databases
\dt 

# Connect to database
\c <database> 

## Example ##

\c app-web
\dt

## --- Stop & Delete --- ##
-- First, set the database to allow no new connections

    ALTER DATABASE mediago WITH ALLOW_CONNECTIONS = false;

-- Terminate all existing connections to the database
    SELECT pg_terminate_backend(pg_stat_activity.pid)
    FROM pg_stat_activity
    WHERE pg_stat_activity.datname = 'mediago'
    AND pid <> pg_backend_pid();

    DROP DATABASE "mediago";
    CREATE DATABASE "mediago";