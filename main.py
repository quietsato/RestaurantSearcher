import tkinter as tk
import tkinter.ttk as ttk

import attributes as at

condition = at.get_condition()


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
                               command=lambda: option_clicked())
    radio_value = tk.BooleanVar()
    city_radio = ttk.Radiobutton(root,
                                 text='都市名・建物名',
                                 variable=radio_value,
                                 value=True)
    location_radio = ttk.Radiobutton(root,
                                     text='緯度・経度',
                                     variable=radio_value,
                                     value=False)
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
                               command=lambda: search_clicked())
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


def option_clicked():
    pass


def search_clicked():
    pass


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
                        command=lambda: cancel_clicked())
    apply = ttk.Button(root,
                       text='適用',
                       command=lambda: apply_clicked())
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


def cancel_clicked():
    pass


def apply_clicked():
    pass

    # endregion


# endregion

# region 検索結果画面
def make_result_window():
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
                           command=lambda: page_clicked())
    google = tk.Button(root,
                       text='Google検索',
                       command=lambda: google_search_clicked())
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


def filter_clicked():
    pass


def page_clicked():
    pass


def google_search_clicked():
    pass


# endregion


make_result_window()
