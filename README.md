# Docs

Make sure the database and redis are running by running the following commands:

```
docker compose up
psql -h localhost  -U postgres
redis-cli -h localhost ping
```

Load the fixtures:

```
python manage.py loaddata products
```
