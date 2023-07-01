![Screenshot](python-flask.svg)

# Why this project ?

    Global recap from different training cycles about Flask.
    This could be a skeleton for general purposes or proof of concepts.

# Quick intro

    Developped with **python3**.
    You will certainly have a straight understanding.
    Summarized tree structure:
        flask_app_cleanblog
          flask_app
              __init__.py     # instantiate database and serve the "init_the_db" cli command
              tests
              topblog
                settings.py  # load your system-user ENV, notice 'load_dotenv(".envrc")' and the app.config definitions
                (...)
          .envrc             # set the SECRET_KEY
          .flaskenv          # set some "FLASK env vars" (FLASK_APP, FLASK_DEBUG, etc..,)
          run.py
          (...)

# Dependencies

    For a development perspective, a post image is suggested, based on a random image from https://picsum.photos/

# How use this project ?

1. Clone the repository

    `git clone https://github.com/memphis-tools/memphis-tools-flask_app_cleanblog.git`

    `cd flask_app_cleanblog`

2. Setup a virtualenv

    `python -m venv env`

    `source env/bin/activate`

    `pip install -U pip`

    `pip install -r requirements.txt`

3. Setup a .envrc

    Your file (flask_app_cleanblog/.envrc) just need this:

    `SECRET_KEY = '68a6b0ebf514c05f999888d61a09c36970ead72313d5fa55558f4ea866a90d44'`

    **NB**: generate your own fixed SECRET_KEY (**module**: 'secrets', **function**: 'token_hex()')

4. Init the database (this will destroy & create database)

    Notice that we create 4 dummy users, admin included. The admin user as the id 1. We create donald.duck's first project. 
    If you decide to start app from scratch, you must set a first user "admin". The id 1 is reserved for our LoginManager permission.

    `flask --app flask_app/ init_the_db`

5. Run app

    `python run.py`

# Versioning

| Annoucement | Description |
| ----------- | ----------- |
| **2023/06/30 - init** | Description: we start with a simple app. We use a simple template "startbootstrap Clean Blog". <br>Notice the design pattern which allows to separate modules : views, models, forms.<br>No SMTP servers set, the contact form will just log into logs.<br>Sources:<br>https://startbootstrap.com/theme/clean-blog<br>https://dev.to/jakewitcher/using-env-files-for-environment-variables-in-python-applications-55a1<br>https://www.udemy.com/course/100-days-of-code/<br>https://python-adv-web-apps.readthedocs.io/en/latest/flask_forms.html<br>https://openclassrooms.com/fr/courses/4425066-concevez-un-site-avec-flask<br>https://unsplash.com/photos/npxXWgQ33ZQ<br>https://unsplash.com/photos/DqWEAOHsAvc |
| **2023/07/01 - add Post CRUD features**| Description: we now possess a "Post CRUD feature" which allows for any user connected to publish or edit a post. The admin is the only one able to update an delete any post.<br>Project can be initialized with dummy datas through the "init_the_db" flask cli command.<br>More sources: https://unsplash.com/photos/s9CC2SKySJM<br>https://picsum.photos|
|||



# At work
   ⛩️
