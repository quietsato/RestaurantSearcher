class Attributes():
    pass


class Condition(Attributes):
    def __init__(self):
        # TODO set default value
        pass


class Data(Attributes):
    name = ''
    address = ''
    url = ''
    imageUrl = ''

    def __init__(self, json):
        # TODO set restaurant data from json
        pass
