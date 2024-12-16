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

## --- Delete table and migrate again --- ##

-- Drop table
DROP TABLE IF EXISTS <table_name>;

## --- Delete migrations --- ##

DELETE FROM django_migrations WHERE app = ' <app_name> ';

example:
DELETE FROM django_migrations WHERE app = 'Airports';

rm -rf app/<app_name>/migrations/*
touch app/<app_name>/migrations/__init__.py

example:
rm -rf app/Airports/migrations/*
touch app/Airports/migrations/__init__.py

rm -rf app/Bookings/migrations/*
touch app/Bookings/migrations/__init__.py

## --- Migrate again --- ##

python3 manage.py makemigrations <app_name>
python3 manage.py migrate <app_name>

example:
python3 manage.py makemigrations Airports
python3 manage.py migrate Airports

python3 manage.py migrate auth --fake
python3 manage.py migrate admin --fake
python3 manage.py migrate contenttypes --fake
python3 manage.py migrate sessions --fake
python3 manage.py migrate socialaccount --fake
python3 manage.py migrate account --fake
python3 manage.py migrate Airports --fake
python3 manage.py migrate Bookings --fake
python3 manage.py migrate Users --fake

UPDATE "Users_user"
SET "isLogin" = false
WHERE "id" = '9a939b77-787b-4ebb-a15a-8425feae7882';

UPDATE "Users_user"
SET "is_staff" = true
WHERE "id" = 'd8da2ae3-43d6-4e28-88eb-58d983d9d1d2';

