Simple parsing and replaying Fiddler's session
==============================================
It works with Python3.

It's recommended to setup virtual environment. Some links:
https://docs.python.org/3/library/venv.html
https://virtualenv.pypa.io/en/stable/userguide/

Commands for Windows: ::

    python -m venv env
    call env/scripts/activate.bat



Then it's necessary to setup modules: ::

    pip install -r requirements.txt


After it you can run the script: ::

    python main.py

Currently this script extracts file "*FiddlerSession2.saz*" to "*FiddlerSession2*"-directory,
then sends all requests from "*raw/NUMBER_c.txt*".
Supported HTTP-methods: GET, OPTIONS, POST, PUT, PATCH or DELETE.

