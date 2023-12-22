from dataclasses import dataclass, replace
from typing import Set
from budget_assist.constants import Label, TransactionType

@dataclass(frozen=True)
class Transaction:
    date: str
    description: str
    original_description: str
    amount: float
    transaction_type: TransactionType
    category: str
    account_name: str
    labels: Set[str]
    notes: str

    def __post_init__(self):
        assert self.transaction_type in TransactionType

    @property
    def signed(self):
        return self.transaction_type.multiplier * self.amount

    #     def __init__(self, data):
    #         self.data = data
    #         self._label_list = None

    #     def __repr__(self):
    #         return str(self.data)

    #     @property
    #     def labels(self):
    #         return self.data['Labels']

    #     @labels.setter
    #     def labels(self, value):
    #         self.data['Labels'] = value
    #         self._label_list = None

    #     @property
    #     def category(self):
    #         return self.data['Category']

    #     @category.setter
    #     def category(self, value):
    #         self.data['Category'] = value

    #     @cached_property
    #     def type(self):
    #         return

    #     @property
    #     def description(self):
    #         return self.data['Description']

    #     @property
    #     def amount(self):
    #         return float(self.data['Amount'])

    #     def value_of_header(self, header):
    #         if header in self.data:
    #             return self.data[header]
    #         if header == SIGNED_HEADER_NAME:
    #             return self.type.multiplier * self.amount

    def format(self, col_data):
        if isinstance(col_data, set):
            return " ".join(str(item) for item in col_data)

        return col_data

    def data_for_headers(self, headers):
        return [self.format(getattr(self, self.attr_from_csv_col(h))) for h in headers]

    #     def has_label(self, label):
    #         return label in self.label_list

    def set_label(self, label, value):
        if (label in self.labels) == value:
            return self

        if value:
            new_labels = self.labels | {label}
        else:
            new_labels = self.labels - {label}

        return self.copy(labels=new_labels)

    def copy(self, **kwargs):
        return replace(self, **kwargs)

    def inverse(self):
        return replace(self, transaction_type=self.transaction_type.inverse())

    def transform(self):
        for label in self.labels:
            if not label.transform:
                continue

            transaction_list = []
            for transaction in label.transform(self):
                transaction_list.extend(transaction.transform())
            return transaction_list
        return [self]

    @classmethod
    def extract_labels(cls, labels_str):
        label_set = set()
        for label in Label.members():
            if label.canonical_name in labels_str:
                labels_str = labels_str.replace(label.canonical_name, '').strip()
                label_set.add(label)
        if len(labels_str) > 1:
            raise ValueError(labels_str)
        for label in Label.members():
            pass
        return label_set

    @classmethod
    def attr_from_csv_col(cls, h):
        return h.lower().replace(' ', '_')

    @classmethod
    def process_header(cls, header):
        for h in header:
            yield cls.attr_from_csv_col(h)

    @classmethod
    def from_csv_row(cls, header, row):
        data = dict(zip(cls.process_header(header), row))
        labels = cls.extract_labels(data.pop('labels'))
        transaction_type = TransactionType.from_canonical(data.pop('transaction_type'))
        amount = float(data.pop('amount'))
        return cls(labels=labels, transaction_type=transaction_type, amount=amount,**data)
