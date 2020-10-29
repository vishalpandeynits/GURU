# GURU
AN ONLINE CLASS PORTAL<br
This portal provides all functionalities for conduction of a smooth online classroom by school/College

## Please don't mess up with MASTER BRANCH

**Installation**

<h4> Make sure python and pip is already installed in your system </h4>

1. Clone the repo *Or* Run `git pull origin master` if already cloned.
2. Visit the root directory. Root directory is the directory where manage.py file located.
3. delete db.sqlite file if present in root.
4. open cmd in this root. Run `pip install -r requirements.txt` in cmd to install all dependancies.
5. Run `python manage.py makemigrations` 
6. Run `python manage.py migrate --run-syncdb`
7. Run `python manage.py runserver`

## Don't try to use login with google functionality, it will give error. It is left intentionally for now.
