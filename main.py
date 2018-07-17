import io
import re
import tkinter as tk
import tkinter.ttk as ttk
import urllib.request as request
import webbrowser as wb
from tkinter.messagebox import showinfo, showwarning

import requests as rq
from PIL import Image

from attributes import *
from keys import *
from urls import *

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
                               command=lambda: make_option_window(None))
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
def make_option_window(shop_list):
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
                       command=lambda: apply_clicked(combo, root, shop_list))

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

    # root.mainloop()
    # endregion


def apply_clicked(combo, root, shop_list):
    for num in range(len(combo)):
        condition[condition_keys[num]] = combo[num].get()
    root.destroy()

    if shop_list is not None:
        set_display_data()
        set_shop_list(shop_list)
    # endregion


# endregion

# region 検索結果画面
def make_result_window():
    set_display_data()

    # region rootウィンドウの設定
    root = tk.Tk()
    root.title('検索結果')
    for column in range(6):
        if column != 2:
            root.columnconfigure(column, weight=1)
    for row in range(3):
        root.rowconfigure(row, weight=1)
    # endregion
    # region ウィジェットの定義
    shop_list = tk.Listbox(root)
    shop_detail = tk.Text(root)
    back_button = ttk.Button(root,
                            text='戻る',
                            command=lambda: back_clicked(root))
    filter_button = ttk.Button(root,
                               text='フィルター',
                               command=lambda: filter_clicked(shop_list, shop_detail))
    image_button = ttk.Button(root,
                              text='サムネイル画像',
                              command=lambda: image_clicked(shop_list))
    web_button = tk.Button(root,
                           text='Webページ',
                           command=lambda: page_clicked(shop_list))
    google = tk.Button(root,
                       text='Google検索',
                       command=lambda: google_search_clicked(shop_list))

    for rst in display_data:
        shop_list.insert(tk.END, rst['name'])
    shop_list.bind('<<ListboxSelect>>',
                   lambda event: shop_list_selected(
                       shop_list, shop_detail))
    # endregion
    # region ウィジェットの配置
    shop_list.grid(column=0, columnspan=2, row=0, rowspan=2, padx=5, pady=5, sticky=tk.N + tk.S + tk.W + tk.E)
    shop_detail.grid(column=3, columnspan=3, row=1, padx=5, pady=5, sticky=tk.N + tk.S + tk.W + tk.E)
    back_button.grid(column=0, row=2, padx=5, pady=5, sticky=tk.W + tk.S)
    filter_button.grid(column=, row=2, padx=5, pady=5, sticky=tk.W + tk.S)
    image_button.grid(column=3, row=2, padx=5, pady=5, sticky=tk.E + tk.S)
    web_button.grid(column=4, row=2, padx=5, pady=5, sticky=tk.E + tk.S)
    google.grid(column=5, row=2, padx=5, pady=5, sticky=tk.E + tk.S)

    root.mainloop()
    # endregion


def set_display_data():
    display_data.clear()
    # region conditionをもとにdisplay_dataを設定する
    flag = True
    for rst in rst_data:
        for key in condition_keys:
            # もし、条件の値が'指定しない'だったら無視する
            if condition[key] != '指定しない':
                # もし、検索条件がgenre_nameだったら、
                # '居酒屋'がrstに含まれていないかチェックする
                if key == 'genre_name':
                    flag = not ('居酒屋' in rst['genre_name'])
                # もし、検索条件がcharterだったら、
                # 貸し切り'不可’であるかどうかを返す
                elif key == 'charter':
                    if condition[key] == 'あり' and '不可' in rst['charter']:
                        flag = False
                    elif condition[key] == 'なし' and not ('不可' in rst['charter']):
                        flag = False
                # 検索条件がそれら以外なら、'あり', 'なし'がrstに含まれているか
                # チェックする
                elif not (condition[key] in rst[key]):
                    flag = False

        if flag:  # 条件を満たしているならdisplay_dataに追加
            display_data.append(rst)
        flag = True
    # endregion


def shop_list_selected(shop_list, detail):
    try:
        index = shop_list.curselection()[0]
    except IndexError:
        # shop_listで店舗が選択されてないときは処理を終了する
        return
    else:
        detail.config(state=tk.NORMAL)
        # Textを初期化する
        detail.delete(index1='1.0', index2=tk.END)
        # Textに値を追加
        for i in range(len(display_data_keys)):
            detail.insert(tk.END,
                          display_data_index[i] + ' : '
                          + display_data[index][display_data_keys[i]] + '\n')
        detail.config(state=tk.DISABLED)


def back_clicked(root):
    root.destroy()
    make_search_window()


def filter_clicked(shop_list, detail):
    # shop_detailの初期化
    detail.config(state=tk.NORMAL)
    detail.delete(index1='1.0', index2=tk.END)

    make_option_window(shop_list)


def set_shop_list(shop_list):
    # Listboxの初期化
    shop_list.delete(first=0, last=tk.END)
    # Listboxへ値の代入
    for rst in display_data:
        shop_list.insert(tk.END, rst['name'])


def image_clicked(shop_list):
    try:
        index = shop_list.curselection()[0]
    except IndexError:
        # shop_listで店舗が選択されてないときは処理を終了する
        return
    else:
        image_url = display_data[index]['image_url']
        # 店舗画像を取ってきてPILで表示
        f = io.BytesIO(request.urlopen(image_url).read())
        image = Image.open(f)
        image.show()


def page_clicked(shop_list):
    try:
        index = shop_list.curselection()[0]
    except IndexError:
        # shop_listで店舗が選択されてないときは処理を終了する
        return
    else:
        url = display_data[index]['url']
        wb.open(url=url)


def google_search_clicked(shop_list):
    try:
        index = shop_list.curselection()[0]
    except IndexError:
        # shop_listで店舗が選択されてないときは処理を終了する
        return
    else:
        name = display_data[index]['name']
        wb.open(url=g_search + name)


# endregion


make_search_window()
