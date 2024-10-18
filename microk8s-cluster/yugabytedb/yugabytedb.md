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