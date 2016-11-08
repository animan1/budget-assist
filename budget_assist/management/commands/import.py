import csv
from cached_property import cached_property
from collections import OrderedDict
from django.core.management.base import BaseCommand

from budget_assist.constants import Label, TransactionType


class Transaction(object):

    def __init__(self, data):
        self.data = data

    @cached_property
    def label_list(self):
        labels_str = self.data['Labels']
        label_list = []
        for label in Label.members():
            if label.canonical_name in labels_str:
                labels_str = labels_str.replace(label.canonical_name, '')
                label_list.append(label)
        return label_list

    @cached_property
    def type(self):
        return TransactionType.from_canonical(self.data['Transaction Type'])

    def has_label(self, label):
        return label in self.label_list

    def copy(self):
        return Transaction(self.data.copy())

    def inverse(self):
        inverse_data = self.data.copy()
        inverse_type = self.type.inverse()
        inverse_data['Transaction Type'] = inverse_type.canonical_name
        return Transaction(inverse_data)

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
        transaction = transactions[1]
        # print str((transaction.has_label(Label.WRONG_ACCOUNT), transaction.label_list))
        print transaction.data
        print transaction.inverse().data
