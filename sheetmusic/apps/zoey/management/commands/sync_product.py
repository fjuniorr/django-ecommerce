from django.core.management.base import BaseCommand, CommandError
from sheetmusic.apps.zoey.models import Product

class Command(BaseCommand):
    help = 'Syncs products. Can sync a specific product, multiple products, or all products.'

    def add_arguments(self, parser):
        parser.add_argument('product_ids', nargs='*', type=int, help='ID(s) of the product(s) to sync. If not provided, syncs all products.')
        parser.add_argument('--all', action='store_true', help='Sync all products')

    def handle(self, *args, **options):
        if options['all']:
            products = Product.objects.all()
        elif options['product_ids']:
            products = Product.objects.filter(id__in=options['product_ids'])
            if not products.exists():
                raise CommandError('No products found with the provided ID(s)')
        else:
            raise CommandError('Please provide product ID(s) or use --all to sync all products')

        for product in products:
            self.stdout.write(self.style.SUCCESS(f'Starting sync for product "{product.title}" (ID: {product.id})'))
            try:
                product.sync()
                self.stdout.write(self.style.SUCCESS(f'Successfully synced product "{product.title}" (ID: {product.id})'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error syncing product "{product.title}" (ID: {product.id}): {str(e)}'))

        self.stdout.write(self.style.SUCCESS('Sync process completed'))
