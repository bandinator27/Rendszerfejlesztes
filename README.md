# Rendszerfejlesztés
## Bérautó

Virtuális környezet indítás projektkönyvtárban:  
```
python -m venv env  
(Windows) .\env\Scripts\activate
(Linux) source env/bin/activate
pip install -r requirements.txt
```

Ezután lehet használni a migrációs parancsokat:  
```
flask db init (erre csak akkor van szükség ha nincs migration mappa)  
flask db upgrade  
flask db migrate -m "TÁBLA_NEVE table"
```

Ha aktív a virtuális környezet akkor lehet indítani a webszervert:  
`flask run` vagy `python run_app.py`