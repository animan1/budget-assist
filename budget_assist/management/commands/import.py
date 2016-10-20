import csv
from collections import OrderedDict
from django.core.management.base import BaseCommand


class Transaction(object):

    def __init__(self, data):
        self.data = data

    @classmethod
    def from_csv_row(cls, header, row):
        data = OrderedDict(zip(header, row))
        return cls(data)


class Command(BaseCommand):
    help = 'Import a transactions CSV from Mint'

    def add_arguments(self, parser):
        parser.add_argument('transactions_filename', type=str)

    def handle(self, *args, **options):
        filename = options['transactions_filename']
        with open(filename) as transactions_file:
            reader = csv.reader(transactions_file)
            header = reader.next()
            transactions = [Transaction.from_csv_row(header, row) for row in reader]
        print transactions[0].data
