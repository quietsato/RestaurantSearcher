print('Please run main.py')


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

    def __init__(self, json):
        # TODO 店舗データをjsonから設定
        pass
