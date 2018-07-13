condition_default = '指定しない'
condition_keys = [
    'genre_name', 'wifi', 'free_drink', 'free_food',
    'private_room', 'non_smoking', 'charter', 'parking'
]

condition_values = [
    ('指定しない', '居酒屋以外'),
    ('指定しない', 'あり', 'なし'),
    ('指定しない', 'あり', 'なし'),
    ('指定しない', 'あり', 'なし'),
    ('指定しない', 'あり', 'なし'),
    ('指定しない', 'あり', 'なし'),
    ('指定しない', 'あり', 'なし'),
    ('指定しない', 'あり', 'なし')
]

data = {'name': '',
        'address': '',
        'url': '',
        'image_url': '',
        'catch': '',
        'open': '',
        'course': '',
        'midnight': '',
        'close_day': ''}
data_keys = ['name', 'address', 'url', 'image_url', 'catch',
             'open', 'course', 'midnight', 'close_day'] + condition_keys


def get_condition():
    # 戻り値のテンプレートの作成
    cond = {
        key: condition_default for key in condition_keys
    }

    return cond


def convert_data(res=None):
    # 戻り値のテンプレートの作成
    r_data = {
        key: '' for key in data_keys
    }

    r_data['name'] = res['name']
    r_data['address'] = res['address']
    r_data['url'] = res['urls']['pc']
    r_data['image_url'] = res['photo']['pc']['l']

    r_data['genre_name'] = res['genre']['name']
    r_data['charter'] = res['charter']
    r_data['close_day'] = res['close']
    r_data['free_drink'] = res['free_drink']
    r_data['free_food'] = res['free_food']
    r_data['wifi'] = res['wifi']
    r_data['private_room'] = res['private_room']
    r_data['non_smoking'] = res['non_smoking']

    r_data['catch'] = res['catch']
    r_data['open'] = res['open']
    r_data['course'] = res['course']
    r_data['midnight'] = res['midnight']

    return r_data
