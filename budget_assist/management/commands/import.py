from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Import a transactions CSV from Mint'

    def add_arguments(self, parser):
        parser.add_argument('transactions_filename', type=str)

    def handle(self, *args, **options):
        print 'Called the import command with %s' % options['transactions_filename']
