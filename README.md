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

## Periodic tasks

The periodic tasks still need ‘workers’ to execute them. So make sure the default Celery package is installed. Both the worker and beat services need to be running at the same time. As a separate process, start the beat service (specify the Django scheduler):

```
celery -A sheetmusic.celery:app beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

See the [docs](https://django-celery-beat.readthedocs.io/en/latest/#example-running-periodic-tasks) for other options such as running the worker and beat services with only one command for development.

## Omnichannel Order Normalization

Two new apps provide a minimal framework for normalizing orders from many storefronts.

### Adapter Keys

Adapters are looked up by semantic keys of the form:
`<provider>.<api_version>.<kind>[.<channel>][.<program>][@<ingest>][#<schema_version>][:<format>][+<flags>...]`.
The resolver progressively drops specificity (+flags → :format → #schema → @ingest → .program → .channel → provider.api_version.kind → provider.api_version.* → provider.* → *).

### Ingestion Envelopes

Transport and trigger metadata travel alongside payloads and stay out of the adapter key. Example envelopes:

```json
{"adapter_key":"shopify.v2025_04.standard","transport":"webhook","trigger":{"mode":"push"},"flags":[]}
{"adapter_key":"shopify.v2025_04.subscription.recharge","transport":"webhook","trigger":{"mode":"push"},"flags":["split-bundles"]}
{"adapter_key":"shopify.v2025_04.subscription.recharge","transport":"http_api","trigger":{"mode":"periodic","schedule":"*/15 * * * *","cursor":{"since":"2025-09-01T00:00:00Z"}}}
{"adapter_key":"magento.v2.standard","transport":"http_api","trigger":{"mode":"periodic","schedule":"0 * * * *"}}
{"adapter_key":"shopify.na.subscription.recharge@s3#v2025_09:csv+gzip+utf8-bom","transport":"s3","trigger":{"mode":"periodic"},"flags":["gzip","utf8-bom"]}
{"adapter_key":"distributor_abc.na.standard@sftp#spec3:tsv","transport":"sftp","trigger":{"mode":"manual","actor":"user:francisco"},"flags":["headerless","pipe-delim"]}
```

### Quickstart

Run a worker and beat:

```
celery -A sheetmusic.celery:app worker --loglevel=info
celery -A sheetmusic.celery:app beat --loglevel=info
```

Post a webhook:

```
curl -X POST http://localhost:8000/ingest/webhook/ \
  -H 'Content-Type: application/json' \
  -d '{"adapter_key":"shopify.v2025_04.standard","transport":"webhook","trigger":{"mode":"push"},"payload":{"id":"1"},"flags":[]}'
```

### Job naming convention

Celery beat entries follow `job::<provider>.<kind>[.<channel>][.<program>]@<transport>.<mode>[.<freq>]`.
Examples:
- `job::shopify.subscription.recharge@http_api.periodic.15m`
- `job::distributor_abc.standard@sftp.manual`
