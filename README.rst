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


If you want to change design, you should use session_replay.ui file. It can be opened by QtDesigner.
After changing and saving this file you should run ::

    pyuic5 session_replay.ui -o session_replay.py

Currently this script extracts requestr from selected file to directory with the same name,
then sends all requests from "*raw/NUMBER_c.txt*".
Supported HTTP-methods: GET, OPTIONS, POST, PUT, PATCH or DELETE.

