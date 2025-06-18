# Projet Git & CI - Groupe 7

## Installation 

```bash
docker-compose up -d
```


## Base de données
Si c'est le premier démarrage il faudra appliquer les migrations
```bash
docker-compose exec -it api-python bash
poetry run alembic upgrade head
exit
```

Si un quelconque problème survient avec la base de données, supprimez le fichier app.db et relancez la commande de migration.

## Tests
Pour lancer les tests, il faut d'abord se connecter au conteneur de l'API Python, puis exécuter les tests avec pytest. Assurez-vous que le répertoire de travail est correctement défini pour que les tests puissent être trouvés.

```bash
docker-compose exec -it api-python bash
export PYTHONPATH=/app
cd app/tests
pytest salles_routes.py
pytest reservation_routes.py
exit
```


