import csv
from cached_property import cached_property
from collections import OrderedDict
from django.core.management.base import BaseCommand
from budget_assist.data import Transaction

SIGNED_HEADER_NAME = 'Signed'

class Command(BaseCommand):
    help = 'Import a transactions CSV from Mint'

    def add_arguments(self, parser):
        parser.add_argument('transactions_filename', type=str)

    def handle(self, *args, **options):
        filename = options['transactions_filename']
        with open(filename) as transactions_file:
            reader = csv.reader(transactions_file)
            header = next(reader)
            transactions = [Transaction.from_csv_row(header, row) for row in reader]

        transformed = []
        for transaction in transactions:
            transformed.extend(transaction.transform())

        filename_no_extension = filename.rsplit('.csv')[0]
        header = [SIGNED_HEADER_NAME] + header
        with open('%s-out.csv' % filename_no_extension, 'w') as outfile:
            writer = csv.writer(outfile, quoting=csv.QUOTE_ALL)
            writer.writerow(header)
            for transaction in transformed:
                writer.writerow(transaction.data_for_headers(header))
