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

## Sync products

When we create a model method we can reuse that logic in a view or management command without duplicating code. For example, we can create a `sync` method on the `Product` model, and then reuse that logic in a management command to sync all products or a specific product.

```
python manage.py sync_product 1
```

We can also sync all products:

```
python manage.py sync_product --all
```

However, we can also expose this logic through a API endpoint. To do this, we can create a view that will trigger the sync process for a specific product as a background task using Celery. For example, if someone makes a GET request to `/zoey/sync/1/`, we can trigger the `sync_product` task to run in the background.

Note that both the management command and the view are doing the same thing: they are syncing a product using `sheetmusic.apps.zoey.models.Product.sync()`. However, the view is triggered by an HTTP request, and the management command is triggered by a command line command.
