import csv
from cached_property import cached_property
from collections import OrderedDict
from django.core.management.base import BaseCommand

from budget_assist.constants import Label, TransactionType


class Transaction(object):

    def __init__(self, data):
        self.data = data
        self._label_list = None

    def __repr__(self):
        return str(self.data)

    @property
    def labels(self):
        return self.data['Labels']

    @labels.setter
    def labels(self, value):
        self.data['Labels'] = value
        self._label_list = None

    @property
    def label_list(self):
        if self._label_list is not None:
            return self._label_list

        labels_str = self.labels
        self._label_list = []
        for label in Label.members():
            if label.canonical_name in labels_str:
                labels_str = labels_str.replace(label.canonical_name, '')
                self._label_list.append(label)
        return self._label_list

    @property
    def category(self):
        return self.data['Category']

    @category.setter
    def category(self, value):
        self.data['Category'] = value

    @cached_property
    def type(self):
        return TransactionType.from_canonical(self.data['Transaction Type'])

    def has_label(self, label):
        return label in self.label_list

    def set_label(self, label, value):
        if self.has_label(label) == value:
            return

        label_str = self.labels
        if value:
            label_str += ' %s' % label
        else:
            label_str = label_str.replace(label.canonical_name, '').replace('  ', ' ').strip()

        self.labels = label_str

    def copy(self):
        return Transaction(self.data.copy())

    def inverse(self):
        inverse_data = self.data.copy()
        inverse_type = self.type.inverse()
        inverse_data['Transaction Type'] = inverse_type.canonical_name
        return Transaction(inverse_data)

    def transform(self):
        transaction_list = []
        for label in self.label_list:
            transaction_list.append([transaction for transaction in label.transform(self)])
        return transaction_list

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
