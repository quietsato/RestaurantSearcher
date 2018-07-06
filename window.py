import keys, urls
from attributes import *
import io, PIL.Image, re
from tkinter import *
from tkinter import ttk
import tkinter.messagebox as tkmsg
import requests as rq
import webbrowser as wb


# print('Please run main.py')
# exit(0)

# tkinterのルートウィンドウの変数名は"root"とする

class Window:
    size = ''
    title = ''

    def onClose(self):
        pass


class Search(Window):
    def __init__(self):
        self.size = '300x250'
        self.title = '検索'
        self.root = Tk()
        self.cond = Condition()
        self.makeWindow(root=self.root)

    def makeWindow(self, root):

        root.title(self.title)
        root.geometry(self.size)
        root.columnconfigure(1, weight=1)
        root.columnconfigure(2, weight=1)
        root.rowconfigure(8, weight=1)

        # ウィジェットの定義をまとめて行う
        label1 = ttk.Label(root,
                           text='検索条件：')
        oButton = ttk.Button(root,
                             text='詳細検索')
        radio_value = BooleanVar()

        lButton = ttk.Radiobutton(root,
                                  text='緯度・経度',
                                  variable=radio_value,
                                  value=False,
                                  )
        cButton = ttk.Radiobutton(root,
                                  text='都市名・建物名',
                                  variable=radio_value,
                                  value=True,
                                  )
        entryLabel = {
            'lat': ttk.Label(root, text='緯度'),
            'lng': ttk.Label(root, text='経度'),
            'city': ttk.Label(root, text='都市・建物')
        }
        entry = {
            'lat': ttk.Entry(root),
            'lng': ttk.Entry(root),
            'city': ttk.Entry(root)
        }
        sButton = ttk.Button(root,
                             text='検索する')

        # ウィジェットの配置
        label1.grid(column=0, row=0, padx=5, pady=5, sticky=W)
        oButton.grid(column=2, row=0, padx=5, pady=5, sticky=E)

        lButton.grid(column=0, columnspan=2, row=1, padx=10, pady=5, sticky=W)

        cButton.grid(column=0, columnspan=2, row=2, padx=10, sticky=W)

        entryLabel['lat'].grid(row=4, padx=5, pady=5, sticky=E)
        entry['lat'].grid(column=1, columnspan=2, row=4, padx=5, pady=5, sticky=W + E)

        entryLabel['lng'].grid(row=5, padx=5, pady=5, sticky=E)
        entry['lng'].grid(column=1, columnspan=2, row=5, padx=5, pady=5, sticky=W + E)

        entryLabel['city'].grid(row=7, padx=5, pady=5, sticky=E)
        entry['city'].grid(column=1, columnspan=2, row=7, padx=5, pady=5, sticky=W + E)

        sButton.grid(column=2, row=8, padx=5, pady=5, sticky=E + S)

        # ウィジェットのイベントバインディング
        sButton.configure(command=
                          lambda: self.onSearchClicked(radio_value.get(), self.cond, entry))

        # rootの表示続行処理
        root.mainloop()

    def onOptionClicked(self, cond):
        Option(caller=self, cond=cond)

    def onSearchClicked(self, isCityName, cond, entry):
        print('ここ来たよ')
        if (isCityName):
            print('都市調べるよ')
            print(entry['city'].get())
            params = self.getLatLngByCity(entry['city'].get())
            if params == 'NOT FOUND':
                return
        else:
            pattern = r'^([1-9]\d*|0)(\.\d+)?$'
            lat = re.match(pattern, entry['lat'].get())
            lng = re.match(pattern, entry['lng'].get())
            if lat is None or lng is None:
                tkmsg.showwarning(
                    title='入力値エラー',
                    message='値は整数または小数で入力してください'
                )
                return
            params = [float(lat.string),
                      float(lng.string)]

        result = self.getRDataByLatLng(params)
        if result is None:
            tkmsg.showinfo(
                title='検索結果',
                message=
                '検索地周辺の検索結果は0件でした\n' +
                '異なる地点を指定するか、入力値の精度を上げてみてください'
            )
            return
        r = Result(result, cond)
        return result

    def onClose(self):
        tkmsg.askokcancel(
            title='確認',
            message='終了しますか？'
        )
        self.root.destroy()

    def getLatLngByCity(self, cityName):
        res = rq.get(url=urls.g_apiurl, params={
            'address': cityName, 'key': keys.g_KEY
        }).json()
        if res['status'] != 'OK':
            tkmsg.showinfo('見つかりませんでした',
                           '異なるデータで再度お試しください')
            return 'NOT FOUND'

        location = [
            str(res['results'][0]['geometry']['location']['lat']),
            str(res['results'][0]['geometry']['location']['lng'])
        ]
        return location

    def getRDataByLatLng(self, location):
        print(location)
        res = rq.get(url=urls.h_apiurl, params={
            'key': keys.h_KEY,
            'lat': location[0],
            'lng': location[1],
            'format': 'json',
            'count': '50'
        }).json()

        print(res['results'])
        if res['results']['results_available'] == 0:
            return None

        r_data = [
            Data(shop)
            for shop in res['results']['shop']
        ]

        return r_data


class Option(Window):

    def __init__(self, caller, cond):
        self.root = Tk()
        self.cond = cond
        self.caller = caller
        self.makeWindow(root=self.root)
        pass

    def makeWindow(self, root):
        root.title(self.title)
        root.geometry(self.size)

        # ウィジェットの定義
        label1 = ttk.Label(root, text='検索項目')
        label2 = ttk.Label(root, text='条件')
        # コンボボックスの見出し
        label_text = [
            'ジャンル', '定休日', 'Wi-fi', '飲み放題', '食べ放題',
            '個室の有無', '禁煙席の有無', '貸し切りの有無', '駐車場'
        ]
        label = [
            ttk.Label(root, text=t) for t in label_text
        ]
        combo = []  # コンボボックスが実際に格納されるリスト

        cancel = ttk.Button(root, text='キャンセル',
                            command=lambda: self.onCancelClicked())
        apply = ttk.Button(root, text='適用',
                           command=lambda: self.onApplyClicked(caller=self.caller, cond=cond))

        # region コンボボックスの定義
        combo_keys = [
            'genre_name', 'close_day', 'wifi', 'free_drink', 'free_food',
            'private_room', 'non_smoking', 'charter', 'parking'
        ]
        combo_values = [
            ('指定しない', '居酒屋以外'),
            ('指定しない', '月', '火', '水', '木', '金', '土', '日'),
            ('指定しない', 'あり', 'なし'),
            ('指定しない', 'あり', 'なし'),
            ('指定しない', 'あり', 'なし'),
            ('指定しない', 'あり', 'なし'),
            ('指定しない', '分煙', '禁煙'),
            ('指定しない', 'あり', 'なし'),
            ('指定しない', 'あり', 'なし')
        ]
        for num in range(len(combo_keys)):
            c = ttk.Combobox(root, state='readonly')
            c['values'] = combo_values[num]
            current_value = self.cond.data[combo_keys[num]]
            # コンボボックスの初期値のインデックスをcondの値から設定
            c.current(combo_values[num].index(current_value))
            combo.append(c)
        # endregion

        label1.grid(column=0, columnspan=2, row=0, padx=5, pady=5)
        label2.grid(column=2, columnspan=2, row=0, padx=5, pady=5)

        for count in range(len(label_text)):
            label[count].grid(column=0, columnspan=2, row=count + 1, padx=10, pady=5, sticky=E)
            combo[count].grid(column=2, columnspan=2, row=count + 1, padx=10, pady=5, sticky=W)

        cancel.grid(column=2, row=len(label_text) + 1, padx=5, pady=5, sticky=S + E)
        apply.grid(column=3, row=len(label_text) + 1, padx=5, pady=5, sticky=S + E)

        # ウィジェットの伸縮の設定
        root.columnconfigure(2, weight=1)
        root.columnconfigure(3, weight=1)
        for row in range(len(label_text) + 2):
            root.rowconfigure(row, weight=1)

        root.mainloop()

    def onApplyClicked(self, caller, cond):
        # TODO チェックボックスをもとにcondのフィールドを指定
        if caller is Search:
            caller.cond = cond
        elif caller is Result:
            # TODO callerを閉じてResultを再生成
            r = caller.result
            caller.root.destroy()
            Result(result=r, cond=cond)
        self.root.destroy()

    def onCancelClicked(self):
        pass

    def onClose(self):
        tkmsg.showwarning(title='確認',
                          message='OKを押すと変更した内容は失われます')
        self.root.destroy()


class Result(Window):
    def __init__(self, result, cond):
        self.result = result
        self.cond = cond
        self.makeWindow(root=Tk())

    def makeWindow(self, root):
        # TODO condをもとにresult内のデータを絞り込む
        # TODO ListBoxの中身を絞り込まれたデータをもとに作成
        root.mainloop()

    def onListItemClicked(self, itemNum):
        # TODO 表示する値を設定
        # TODO ImageをimageUrlから持ってくる
        pass

    def onFilterClicked(self, cond):
        o = Option(caller=self, cond=cond)
        pass

    def onPageClicked(self, url):
        wb.open(url=url)
        pass

    def onGSearchClicked(self, name):
        wb.open(url=urls.g_search + name)

    def onClose(self):
        pass
