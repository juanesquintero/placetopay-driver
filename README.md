# PlaceToPay Virtual Shop 

This project is a simple web app develop in Python Flask framework, to simulate a virtual shop integrated
with the PlaceToPay Web Checkout service. 
This project  is based on a Flask Monolithic template/skeleton develop by @juanesquintero, you can find the Flask templates here:

https://gitlab.com/juanesquintero/flask-monolithic-template

https://gitlab.com/juanesquintero/

<br>

This is the PlacetoPay WebCheckOut documentation

https://placetopay.github.io/web-checkout-api-docs/#webcheckout

<br>

To run the project you have to...
1. Install Python 3.8 and pip  
2. Create and activate a virtual env
3. Install dependencies with the requirements-dev.txt
4. Run the project with flask run command on the root folder

Down here are more specification about the project base and the steps mencionated before 


## Template:

### Folder structure:

    ├───.vscode
    ├───app
    │   ├───models
    │   ├───forms
    │   ├───static
    │   │   └───dist
    │   │   └───uploads
    │   ├───templates
    │   │   ├───admin
    │   │   ├───auth
    │   │   └───components
    │   ├───utils
    │   ├───views
    │   └───__init__.py
    ├───db
    ├───logs
    ├───tests
    │   └───test_use_case.py
    ├───venv
    ├───.env
    ├───.flaskenv
    ├───.gitignore
    ├───requirements.txt
    ├───README.md
    ├───config.py
    ├───run.py / wsgi.py

### Define your environment:

    $ pip install virtualenv
    $ virtualenv venv
    $ source venv/Scripts/activate

### Install it:

    (venv) $ pip install -r requirements-dev.txt
    (venv) $ pip freeze

### Define environment variables:

    (venv) $ touch .env
        API_PATH = ""
        SECRET_KEY = "secret"

### Run it:

    (venv) $ flask run --reload --with-threads

### Parepare your Editor:

Git Extensions:
<br>
https://marketplace.visualstudio.com/items?itemName=eamodio.gitlens

https://marketplace.visualstudio.com/items?itemName=donjayamanne.githistory

https://marketplace.visualstudio.com/items?itemName=mhutchie.git-graph

<br>
Python Extensions:
<br>

https://marketplace.visualstudio.com/items?itemName=ms-python.python

https://marketplace.visualstudio.com/items?itemName=LittleFoxTeam.vscode-python-test-adapter

https://marketplace.visualstudio.com/items?itemName=njpwerner.autodocstring

https://marketplace.visualstudio.com/items?itemName=mgesbert.python-path

<br>
Flask Extensions:
<br>

https://marketplace.visualstudio.com/items?itemName=cstrap.flask-snippets

https://marketplace.visualstudio.com/items?itemName=wholroyd.jinja

https://marketplace.visualstudio.com/items?itemName=samuelcolvin.jinjahtml

<br>
Linters Extensions:
<br>

https://marketplace.visualstudio.com/items?itemName=usernamehw.errorlens

https://marketplace.visualstudio.com/items?itemName=streetsidesoftware.code-spell-checker-spanish

<br>
HTML Templates Extensions:
<br>

https://marketplace.visualstudio.com/items?itemName=formulahendry.auto-close-tag

https://marketplace.visualstudio.com/items?itemName=formulahendry.auto-rename-tag

https://marketplace.visualstudio.com/items?itemName=vincaslt.highlight-matching-tag

<br>
Extras:
<br>

https://marketplace.visualstudio.com/items?itemName=vscode-icons-team.vscode-icons

https://marketplace.visualstudio.com/items?itemName=TabNine.tabnine-vscode

https://marketplace.visualstudio.com/items?itemName=Gruntfuggly.todo-tree

https://marketplace.visualstudio.com/items?itemName=mikestead.dotenv

https://marketplace.visualstudio.com/items?itemName=CoenraadS.bracket-pair-colorizer


<br>

### DocString template 

For Python Docstring Generator VSCode extension

Function

    '''
    [Summary].

    :param   [name]<type>:  [description].

    :returns [name]<type>:  [description].
    '''

Class

    '''
    [Summary].
    '''

### That's it!!
