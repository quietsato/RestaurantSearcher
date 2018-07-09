class Attributes:
    data = {'genre_name': '',
            'wifi': '',
            'free_drink': '',
            'free_food': '',
            'private_room': '',
            'non_smoking': '',
            'charter': '',
            'parking': ''
            }


class Condition(Attributes):
    def __init__(self):
        for key in self.data.keys():
            self.data[key] = '指定しない'


option_keys = [
    'genre_name', 'wifi', 'free_drink', 'free_food',
    'private_room', 'non_smoking', 'charter', 'parking'
]
option_values = [
    ('指定しない', '居酒屋以外'),
    ('指定しない', 'あり', 'なし'),
    ('指定しない', 'あり', 'なし'),
    ('指定しない', 'あり', 'なし'),
    ('指定しない', 'あり', 'なし'),
    ('指定しない', 'あり', 'なし'),
    ('指定しない', 'あり', 'なし'),
    ('指定しない', 'あり', 'なし')
]


class Data(Attributes):

    def __init__(self, r_data):
        additional = {'name': '',
                      'address': '',
                      'url': '',
                      'imageUrl': '',
                      'catch': '',
                      'open': '',
                      'course': '',
                      'midnight': ''}
        self.data.update(additional)

        self.data['name'] = r_data['name']
        self.data['address'] = r_data['address']
        self.data['url'] = r_data['urls']['pc']
        self.data['imageUrl'] = r_data['photo']['pc']['l']

        self.data['genre_name'] = r_data['genre']['name']
        self.data['charter'] = r_data['charter']
        self.data['close_day'] = r_data['close']
        self.data['free_drink'] = r_data['free_drink']
        self.data['free_food'] = r_data['free_food']
        self.data['wifi'] = r_data['wifi']
        self.data['private_room'] = r_data['private_room']
        self.data['non_smoking'] = r_data['non_smoking']

        self.data['catch'] = r_data['catch']
        self.data['open'] = r_data['open']
        self.data['course'] = r_data['course']
        self.data['midnight'] = r_data['midnight']
