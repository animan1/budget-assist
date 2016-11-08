from richenum import RichEnum, RichEnumValue


TRANSFER_TYPE = 'Transfer'

def wrong_account_transform(transaction):
    transaction = transaction.copy()
    transaction.set_label(Label.WRONG_ACCOUNT, False)

    inverse_transaction = transaction.inverse()
    copied_transaction = transaction.copy()

    transaction.category = TRANSFER_TYPE

    should_be_joint = Label.JOINT_ACCOUNT not in transaction.label_list

    if not should_be_joint:
        whose_transaction = None
        while whose_transaction is None:
            prompt = (
                    'Whose transaction is %s: "%s"? (p)ersonal / (e)xternal '
                    % (copied_transaction.category, transaction.description)
            )
            whose_transaction = raw_input(prompt)
            if whose_transaction == 'e':
                return [transaction]
            elif whose_transaction != 'p':
                whose_transaction = None

    copied_transaction.set_label(Label.JOINT_ACCOUNT, should_be_joint)
    inverse_transaction.set_label(Label.JOINT_ACCOUNT, should_be_joint)
    inverse_transaction.category = TRANSFER_TYPE

    return [transaction, inverse_transaction, copied_transaction]

class LabelValue(RichEnumValue):

    def __init__(self, canonical_name, display_name, description, transform=None):
        super(LabelValue, self).__init__(canonical_name, display_name, description)
        self.transform = transform

    def __str__(self):
        return self.canonical_name

class Label(RichEnum):

    WRONG_ACCOUNT = LabelValue('Wrong account used', 'Wrong Account Used', '', transform=wrong_account_transform)
    JOINT_ACCOUNT = LabelValue('Joint Account', 'Joint Account', '')

class TransactionTypeValue(RichEnumValue):

    def __init__(self, inverse_canonical_name, *args):
        super(TransactionTypeValue, self).__init__(*args)
        self.inverse_canonical_name = inverse_canonical_name

    def inverse(self):
        return TransactionType.from_canonical(self.inverse_canonical_name)

class TransactionType(RichEnum):

    CREDIT = TransactionTypeValue('debit', 'credit', 'credit', '')
    DEDIT = TransactionTypeValue('credit', 'debit', 'dedit', '')
