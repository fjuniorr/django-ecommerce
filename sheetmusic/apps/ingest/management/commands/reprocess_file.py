from django.core.management.base import BaseCommand
from ...models import InboundFile
from ...tasks import demo_process_inbound_file_hourly


class Command(BaseCommand):
    help = "Reprocess a stored file by UUID"

    def add_arguments(self, parser):
        parser.add_argument("file_id")

    def handle(self, file_id, **options):
        # In reality, enqueue a task to process the file again.
        demo_process_inbound_file_hourly.delay()
        self.stdout.write(f"requeued {file_id}")
