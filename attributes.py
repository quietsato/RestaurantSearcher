class Attributes:
    genre_name = ''
    close_day = ''
    wifi = ''
    free_drink = ''
    free_food = ''
    private_room = ''
    non_smoking = ''
    charter = ''
    parking = ''
    pass


class Condition(Attributes):
    # このクラスはAttributesのフィールドをそのまま持っている
    pass


class Data(Attributes):
    name = ''
    address = ''
    url = ''
    imageUrl = ''
    other_data = {
        'catch': '',
        'open': '',
        'course': '',
        'midnight': ''
    }

    def __init__(self, r_data):
        self.name = r_data['name']
        self.address = r_data['address']
        self.url = r_data['urls']['pc']
        self.imageUrl = r_data['photo']['pc']['l']

        self.genre_name = r_data['genre']['name']
        self.charter = r_data['charter']
        self.close_day = r_data['close']
        self.free_drink = r_data['free_drink']
        self.free_food = r_data['free_food']
        self.wifi = r_data['wifi']
        self.private_room = r_data['private_room']
        self.non_smoking = r_data['non_smoking']

        self.other_data['catch'] = r_data['catch']
        self.other_data['open'] = r_data['open']
        self.other_data['course'] = r_data['course']
        self.other_data['midnight'] = r_data['midnight']
