import csv
from cached_property import cached_property
from collections import OrderedDict
from django.core.management.base import BaseCommand

from budget_assist.constants import Label, TransactionType


SIGNED_HEADER_NAME = 'Signed'


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

    @property
    def description(self):
        return self.data['Description']

    @property
    def amount(self):
        return float(self.data['Amount'])

    def value_of_header(self, header):
        if header in self.data:
            return self.data[header]
        if header == SIGNED_HEADER_NAME:
            return self.type.multiplier * self.amount

    def data_for_headers(self, headers):
        return [self.value_of_header(h) for h in headers]

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
        for label in self.label_list:
            if not label.transform:
                continue

            transaction_list = []
            for transaction in label.transform(self):
                transaction_list.extend(transaction.transform())
            return transaction_list
        return [self]

    @classmethod
    def from_csv_row(cls, header, row):
        data = OrderedDict(zip(header, row))
        return cls(data)


class Command(BaseCommand):
    help = 'Import a transactions CSV from Mint'

    def add_arguments(self, parser):
        parser.add_argument('gcash', type=str)
        parser.add_argument('tsx', type=str)

    def handle(self, *args, **options):
        gcash_filename = options['gcash']
        tsx_filename = options['tsx']

        gcash_transactions = self.handle_gcash_file(gcash_filename)
        self.output(gcash_transactions, out_filename)

    def handle_tsx_file(self, filename):
        with open(filename) as transactions_file:
            reader = csv.reader(transactions_file)
            header = next(reader)
            transactions = [Transaction.from_csv_row(header, row) for row in reader]

        transformed = []
        for transaction in transactions:
            transformed.extend(transaction.transform())
        return transformed

    def output(self, transformed, filename):
        header = list(transformed[0].data.keys()
        filename_no_extension = filename.rsplit('.csv')[0]
        header = [SIGNED_HEADER_NAME] + header
        with open('%s-out.csv' % filename_no_extension, 'w') as outfile:
            writer = csv.writer(outfile, quoting=csv.QUOTE_ALL)
            writer.writerow(header)
            for transaction in transformed:
                writer.writerow(transaction.data_for_headers(header))
