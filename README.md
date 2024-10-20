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

## Background Tasks

You can manually add tasks to the queue by running the following inside a django shell like `python manage.py shell`:

```python
from zoey.tasks import add_numbers
result = add_numbers.delay(4, 4)
result.id
```

You can monitor the task execution in the Flower web interface. Open a web browser and go to http://localhost:5555. However because we still don't have a celery worker running, you will see that the task is not listed anywhere. To start a worker, run the following command:

```
celery -A sheetmusic.celery:app worker --loglevel=info
```

You should see the worker picking up the task and executing it.
