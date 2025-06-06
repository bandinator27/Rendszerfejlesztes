# Advanced methods of system development
## Car rental

Create & activate a virtual environment then install dependencies:
```
python -m venv venv  
(Windows) .\.venv\Scripts\activate
(Linux) source .venv/bin/activate
pip install -r requirements.txt
```

Migration commands (if there's no `migration` folder already):
```
flask db init
flask db migrate -m "your comment"
flask db upgrade
```

With an active virtual environment you can start the webserver: `flask run` or `python run_app.py`