from richenum import RichEnum, RichEnumValue

class LabelValue(RichEnumValue):

    def __init__(self, *args):
        super(LabelValue, self).__init__(*args)

    def __str__(self):
        return self.canonical_name

class Label(RichEnum):

    WRONG_ACCOUNT = LabelValue('Wrong account used', 'Wrong Account Used', '')
