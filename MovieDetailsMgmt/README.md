# Requirement for this project for setup

-> Create a vitual environment.<br/>
== virtualenv -p python3.6 venv<br/>
-> Activate your virtual environment using this command<br/>
== source venv/bin/activate<br/>
-> Install required python libraries by using pip installer.<br/>
== pip install -r requirements.txt<br/>
-> Migrate database.<br/>
== python manage.py migrate<br/>
-> Finally, run your django runserver.<br/>
== python manage.py runserver<br/>

# Scraping movies using managment command scrap.py and parameter link

ex- ./manage.py scrap https://www.imdb.com/chart/top/
or
ex - ./manage.py scrap https://www.imdb.com/india/top-rated-indian-movies/

# User Whistlist and Watched movies is maintained

# Authentication and Consistency of data

# Procfile is used to deploy on heroku cloud

ex- https://fast-caverns-34044.herokuapp.com/
