Rendszerfejlesztés

Virtuális környezet használata: (Linux)
source ./.venv/bin/activate

export FLASK_APP=app/app.py

ezután lehet használni a migrációs parancsokat:

flask db init ( erre csak akkor van szükség ha nincs migrációs mappa)
flask db upgrade
flask db migrate -m "TÁBLA_NEVE table"

ha be van aktiválva a virtuális környezet akkor lehet indítani a webszervert:
flask run

Webszerver indítás dockerrel: (Linux)
sudo docker compose up
(Előtte minden táblának bent kell lennie a migrációs adatbázisban, különben hibát fog dobni.)

TODO:

- api végpontok folytatása
- meglévő oldalak kidolgozása
- kód rendberakása
