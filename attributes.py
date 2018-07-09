# このファイルには変数定義のみが書かれている
# ここの変数の値は変更しないこと

default = '指定しない'
condition = {'genre_name': default,
             'wifi': default,
             'free_drink': default,
             'free_food': default,
             'private_room': default,
             'non_smoking': default,
             'charter': default,
             'parking': default
             }
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
        'imageUrl': '',
        'catch': '',
        'open': '',
        'course': '',
        'midnight': '',
        'close_day': ''}
data.update(condition)

for key in data.keys():
    data[key] = ''

