Rendszerfejlesztés

Virtuális környezet használata: (Windows)
.\env\Scripts\activate

(export FLASK_APP=app/app.py)

ezután lehet használni a migrációs parancsokat:

flask db init ( erre csak akkor van szükség ha nincs migrációs mappa)
flask db upgrade
flask db migrate -m "TÁBLA_NEVE table"

ha be van aktiválva a virtuális környezet akkor lehet indítani a webszervert:
flask run

VAGY
Visaul Studio Start Without Debugging aktív run_app.py fájlban