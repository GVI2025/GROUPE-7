# Projet Git & CI - Groupe 7

## Installation 

```bash
docker-compose up -d
```

Si c'est le premier démarrage il faudra appliquer les migrations
```bash
docker-compose exec -it api-python bash
poetry run alembic upgrade head
exit
```
