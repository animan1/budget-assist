from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Import a transactions CSV from Mint'

    def handle(self, *args, **options):
        print 'Called the import command'
