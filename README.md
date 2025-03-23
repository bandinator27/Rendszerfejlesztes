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

- Táblák összekapcsolása (Users.id -> Roles.id, Users.id -> Rentals.RenterId, Cars.Id -> Rentals.CarId)
- Szerver oldali session management tokennel
- Rentals táblából hiányzik a RentedAt oszlop, a datetimeot nem szerette a flask szóval ezt még meg kell oldani
- Teszt adatok a táblákhoz
- /cars implementálása
- jelszó titkosítás hashel és sózással
- project szétdarabolása blueprinttel
- admin felület implementálása
- config fájl készítése
