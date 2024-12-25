## --- Activating the virtual environment --- ##

source venv/bin/activate

## --- Running the server --- ##

python3 manage.py runserver 8080

## --- Watch CSS change --- ##

npx tailwindcss -i ./static/src/input.css -o ./static/src/output.css --watch

## --- Migration --- ##

python3 manage.py makemigrations
python3 manage.py migrate

# if migration fails, delete the migration folder and the database file
# then, create a new migration folder with __init__.py file
# and run the migration commands again 

## --- Creating a superuser --- ##

python3 manage.py createsuperuser

## --- Docker build & push --- ##
# use the following command to build the docker image
# if Jenkins is not available
docker login
docker build -t nhqb3197/nhqb-mysite:latest .
docker push nhqb3197/nhqb-mysite:latest

## --- Kill all Caddy processes --- ##
# use the following command to kill all Caddy processes

kill -9 $(ps aux | grep '[c]addy')