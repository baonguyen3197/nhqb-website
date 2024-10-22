## --- Activating the virtual environment --- ##

source venv/bin/activate

## --- Running the server --- ##

python3 manage.py runserver 8080

## --- Watch CSS change --- ##

npx tailwindcss -i ./static/src/input.css -o ./static/src/output.css --watch

## --- Migration --- ##

python3 manage.py makemigrations
python3 manage.py migrate
