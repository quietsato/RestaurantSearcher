import tkinter as tk
import tkinter.ttk as ttk
from tkinter.messagebox import showinfo, showwarning
from PIL import Image
import re, io
import urllib.request as request
import requests as rq
import webbrowser as wb

from attributes import *
from urls import *
from keys import *

condition = get_condition()
rst_data = []
display_data = []


# region 検索画面
def make_search_window():
    # region rootウィンドウの設定
    root = tk.Tk()
    root.title('検索')
    root.columnconfigure(1, weight=1)
    root.columnconfigure(2, weight=1)
    root.rowconfigure(8, weight=1)
    # endregion

    # region ウィジェットの定義
    top_label = ttk.Label(root,
                          text='検索条件：')
    option_button = ttk.Button(root,
                               text='詳細検索',
                               command=lambda: make_option_window())
    is_city_name = tk.BooleanVar()
    city_radio = ttk.Radiobutton(root,
                                 text='都市名・建物名',
                                 variable=is_city_name,
                                 value=True)
    location_radio = ttk.Radiobutton(root,
                                     text='緯度・経度',
                                     variable=is_city_name,
                                     value=False)
    is_city_name.set(False)
    entry_label = [
        ttk.Label(root, text='緯度'),
        ttk.Label(root, text='経度'),
        ttk.Label(root, text='都市・建物')
    ]
    entry = []
    for i in range(len(entry_label)):
        entry.append(ttk.Entry(root))
    search_button = ttk.Button(root,
                               text='検索する',
                               command=lambda: search_clicked(is_city_name.get(), entry, root))
    # endregion

    # region ウィジェットの配置
    top_label.grid(column=0, row=0, padx=5, pady=5, sticky=tk.W)
    option_button.grid(column=2, row=0, padx=5, pady=5, sticky=tk.E)

    location_radio.grid(column=0, columnspan=2, row=1, padx=10, pady=5, sticky=tk.W)

    city_radio.grid(column=0, columnspan=2, row=2, padx=10, pady=5, sticky=tk.W)

    for row in range(4, 8):
        if 4 <= row < 6:
            # 4,5行目に緯度・経度検索用のLabel, Entryを置く
            entry_label[row - 4].grid(
                column=0, row=row, padx=5, pady=5, sticky=tk.E)
            entry[row - 4].grid(
                column=1, columnspan=2, row=row, padx=5, pady=5, sticky=tk.W + tk.E)

        elif row == 7:
            # 7行目に都市名検索用のLabel, Entryを置く
            entry_label[2].grid(
                column=0, row=7, padx=5, pady=5, sticky=tk.E)
            entry[2].grid(
                column=1, columnspan=2, row=7, padx=5, pady=5, sticky=tk.W + tk.E)

    search_button.grid(column=2, row=8, padx=5, pady=5, sticky=tk.E + tk.S)

    root.mainloop()
    # endregion


def search_clicked(city, entry, root):
    # region 位置情報を変数に格納
    if city:
        # ジオコーディング
        city_name = entry[2].get()
        geo_res = rq.get(g_apiurl, params={
            'address': city_name, 'key': g_KEY
        }).json()
        if geo_res['status'] != 'OK':
            showinfo(title='見つかりませんでした',
                     message='異なるデータで再度お試しください')
            return
        location = [str(geo_res['results'][0]['geometry']['location']['lat']),
                    str(geo_res['results'][0]['geometry']['location']['lng'])]
    else:
        # 入力値チェック
        pattern = r'^([1-9]\d*|0)(\.\d+)?$'  # 小数を表す正規表現
        lat = re.match(pattern, entry[0].get())
        lng = re.match(pattern, entry[1].get())
        if lat is None or lng is None:
            showwarning(title='入力値エラー',
                        message='値は整数または小数で入力してください')
            return
        # 値をリストに格納
        location = [lat.string,
                    lng.string]
    # endregion

    res = rq.get(url=h_apiurl, params={
        'key': h_KEY,
        'lat': location[0],
        'lng': location[1],
        'format': 'json',
        'count': '50'
    }).json()

    if res['results']['results_available'] == 0:
        showinfo(title='検索結果',
                 message='検索地周辺の検索結果は0件でした\n' +
                         '異なる地点を指定するか、入力値の精度を上げてみてください')
        return

    global rst_data
    rst_data = [convert_data(rst) for rst in res['results']['shop']]
    root.destroy()
    make_result_window()


# endregion

# region 条件定義画面
def make_option_window():
    # region rootウィンドウの設定
    root = tk.Tk()
    root.title('検索条件')
    root.columnconfigure(2, weight=1)
    root.columnconfigure(3, weight=1)
    for row in range(9):
        # すべての行を伸縮可能にする
        root.columnconfigure(row, weight=1)

    # endregion

    # region ウィジェットの定義
    top_labels = [ttk.Label(root, text='検索項目'),
                  ttk.Label(root, text='条件')]
    combo_index = ['ジャンル', 'Wi-Fi', '飲み放題', '食べ放題',
                   '個室', '禁煙席', '貸し切り', '駐車場']
    combo_label = [ttk.Label(root, text=index) for index in combo_index]
    combo = []
    for i in range(len(combo_index)):
        combo.append(ttk.Combobox(root, state='readonly'))
    cancel = ttk.Button(root,
                        text='キャンセル',
                        command=lambda: root.destroy())
    apply = ttk.Button(root,
                       text='適用',
                       command=lambda: apply_clicked(combo, root))

    for num in range(len(combo)):
        combo[num]['values'] = condition_values[num]
        current_value = condition[condition_keys[num]]
        # コンボボックスの初期値をconditionを読み込んで指定
        combo[num].current(newindex=(condition_values[num].index(current_value)))
        pass
    # endregion

    # region ウィジェットの配置
    top_labels[0].grid(column=0, columnspan=2, row=0, padx=5, pady=5)
    top_labels[1].grid(column=2, columnspan=2, row=0, padx=5, pady=5)

    for row in range(1, len(combo_index) + 1):
        combo_label[row - 1].grid(column=0, columnspan=2, row=row, padx=10, pady=5, sticky=tk.E)
        combo[row - 1].grid(column=2, columnspan=2, row=row, padx=10, pady=5, sticky=tk.W + tk.E)

    cancel.grid(column=2, row=len(combo_label) + 1, padx=5, pady=5, sticky=tk.S + tk.E)
    apply.grid(column=3, row=len(combo_label) + 1, padx=5, pady=5, sticky=tk.S + tk.E)

    root.mainloop()
    # endregion


def apply_clicked(combo, root):
    for num in range(len(combo)):
        condition[condition_keys[num]] = combo[num].get()
    root.destroy()

    # endregion


# endregion

# region 検索結果画面
def make_result_window():
    # region conditionをもとにdisplay_dataを設定する
    flag = True
    for rst in rst_data:
        for key in condition_keys:
            # もし、条件の値が'指定しない'だったら無視する
            if condition[key] != '指定しない':
                # もし、条件の値が'指定しない'でない、つまり'居酒屋以外'であるなら
                # '居酒屋'がrstに含まれていないかチェックする

                if key == 'genre_name' and '居酒屋' in rst[key]:
                    flag = False
                # 検索条件が居酒屋以外なら、'あり', 'なし'がrstに含まれているか
                # チェックする
                if not condition[key] in rst[key]:
                    flag = False
        if flag:  # 条件を満たしているならdisplay_dataに追加
            display_data.append(rst)
        flag = True
    # endregion

    # region rootウィンドウの設定
    root = tk.Tk()
    root.title('検索結果')
    for column in range(6):
        root.columnconfigure(column, weight=1)
    for row in range(3):
        root.rowconfigure(row, weight=1)
    # endregion
    # region ウィジェットの定義
    shop_list = tk.Listbox(root)
    shop_image = tk.Canvas(root)
    shop_detail = tk.Listbox(root)
    shop_others = tk.Listbox(root)
    filter_button = tk.Button(root,
                              text='フィルター',
                              command=lambda: filter_clicked())
    web_button = tk.Button(root,
                           text='Webページ',
                           command=lambda: page_clicked(url=None))
    google = tk.Button(root,
                       text='Google検索',
                       command=lambda: google_search_clicked(name=None))

    for rst in display_data:
        shop_list.insert(tk.END, rst['name'])
    shop_list.bind('<<ListboxSelect>>',
                   lambda event: shop_list_selected(
                       shop_list.curselection()[0],
                       shop_image, shop_detail, shop_others))
    # endregion
    # region ウィジェットの配置
    shop_list.grid(column=0, columnspan=2, row=0, rowspan=2, padx=5, pady=5, sticky=tk.N + tk.S + tk.W + tk.E)
    shop_image.grid(column=2, columnspan=2, row=0, padx=5, pady=5, sticky=tk.N + tk.S + tk.W + tk.E)
    shop_detail.grid(column=2, columnspan=2, row=1, padx=5, pady=5, sticky=tk.N + tk.S + tk.W + tk.E)
    shop_others.grid(column=4, columnspan=2, row=0, rowspan=2, padx=5, pady=5, sticky=tk.N + tk.S + tk.W + tk.E)
    filter_button.grid(column=0, row=2, padx=5, pady=5, sticky=tk.W + tk.S)
    web_button.grid(column=4, row=2, padx=5, pady=5, sticky=tk.E + tk.S)
    google.grid(column=5, row=2, padx=5, pady=5, sticky=tk.E + tk.S)

    root.mainloop()
    # endregion


def shop_list_selected(num, image, detail, others):
    # Listboxの初期化
    detail.delete(first=0, last=tk.END)
    others.delete(first=0, last=tk.END)
    # Listboxに値を追加
    important_keys = ['name', 'address', 'open', 'catch']
    for key in important_keys:
        detail.insert(tk.END, display_data[num][key])

    for key in list(set(data_keys) -
                    (set(important_keys) & {'url', 'imageUrl'})):
        others.insert(tk.END, display_data[num][key])

    # 店舗画像を取ってきてCanvasに表示
    f = io.BytesIO(request.urlopen(display_data[num]['imageUrl']).read())
    i = Image.open(f)
    # imageにiをセットする

    pass


def filter_clicked():
    # 仕様変更というタブーを使うならこれは削除するΣ(￣ロ￣lll)ｶﾞｰﾝ
    make_option_window()


def page_clicked(url):
    wb.open(url=url)


def google_search_clicked(name):
    wb.open(url=g_search + name)


# endregion


make_search_window()
