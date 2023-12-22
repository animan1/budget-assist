from richenum import RichEnum, RichEnumValue


TRANSFER_TYPE = 'Transfer'

def _is_external(transaction) -> str:
    while True:
        prompt = (
                'Whose transaction is %s: "%s"? (p)ersonal / (e)xternal '
                % (transaction.category, transaction.description)
        )
        whose_transaction = input(prompt)
        if whose_transaction == 'e':
            return True
        elif whose_transaction != 'p':
            print(f'Invalid choice: {whose_transaction}')
        else:
            return False

def wrong_account_transform(transaction):
    new_labels = set(transaction.labels)
    new_labels.remove(Label.WRONG_ACCOUNT)

    # inverse_transaction = transaction.inverse()
    # copied_transaction = transaction.copy()

    should_be_joint = Label.JOINT_ACCOUNT not in transaction.labels

    transformed_transaction = transaction.copy(
        labels=set(),
        category=TRANSFER_TYPE
    ).set_label(Label.JOINT_ACCOUNT, not should_be_joint)

    if not should_be_joint and _is_external(transaction):
        return [transformed_transaction]

    copied_transaction = transaction.set_label(Label.JOINT_ACCOUNT, should_be_joint).set_label(Label.WRONG_ACCOUNT, False)

    inverse_transaction = transaction.copy(
        category = TRANSFER_TYPE,
        labels = set(),
    ).inverse().set_label(Label.JOINT_ACCOUNT, should_be_joint)

    return [transformed_transaction, inverse_transaction, copied_transaction]

class LabelValue(RichEnumValue):

    def __init__(self, canonical_name, display_name, description, transform=None):
        super(LabelValue, self).__init__(canonical_name, display_name, description)
        self.transform = transform

    def __str__(self):
        return self.canonical_name

class Label(RichEnum):

    WRONG_ACCOUNT = LabelValue('Wrong account used', 'Wrong Account Used', '', transform=wrong_account_transform)
    JOINT_ACCOUNT = LabelValue('Joint Account', 'Joint Account', '')
    MISC_SPENDING = LabelValue('Misc Spending', 'Misc Spending', '')
    REIMBURSABLE = LabelValue('Reimbursable', 'Reimbursable', '')

class TransactionTypeValue(RichEnumValue):

    def __init__(self, inverse_canonical_name, multiplier, *args):
        super(TransactionTypeValue, self).__init__(*args)
        self.inverse_canonical_name = inverse_canonical_name
        self.multiplier = multiplier

    def inverse(self):
        return TransactionType.from_canonical(self.inverse_canonical_name)

class TransactionType(RichEnum):

    CREDIT = TransactionTypeValue('debit', 1, 'credit', 'credit', '')
    DEDIT = TransactionTypeValue('credit', -1, 'debit', 'dedit', '')
