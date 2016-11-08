from richenum import RichEnum, RichEnumValue


class LabelValue(RichEnumValue):

    def __init__(self, *args):
        super(LabelValue, self).__init__(*args)

    def __str__(self):
        return self.canonical_name

class Label(RichEnum):

    WRONG_ACCOUNT = LabelValue('Wrong account used', 'Wrong Account Used', '')

class TransactionTypeValue(RichEnumValue):

    def __init__(self, inverse_canonical_name, *args):
        super(TransactionTypeValue, self).__init__(*args)
        self.inverse_canonical_name = inverse_canonical_name

    def inverse(self):
        return TransactionType.from_canonical(self.inverse_canonical_name)

class TransactionType(RichEnum):

    CREDIT = TransactionTypeValue('debit', 'credit', 'credit', '')
    DEDIT = TransactionTypeValue('credit', 'debit', 'dedit', '')
