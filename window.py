import keys, urls
from attributes import *
import io, PIL.Image, re
from tkinter import *
from tkinter import ttk
import tkinter.messagebox as tkmsg
import requests as rq
import webbrowser as wb
import pprint

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
        self.cond = getCondition()
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
                             text='詳細検索',
                             command=lambda : self.onOptionClicked(cond=self.cond))
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
                             text='検索する',
                             command=
                             lambda: self.onSearchClicked(radio_value.get(), self.cond, entry))

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
        for num in range(len(result)):
            pprint.pprint(result[num])
        self.root.destroy()
        Result(result, cond)

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

        r_data = []
        for shop in res['results']['shop']:
            r_data.append(convertData(shop))

        for i in r_data:
            print(i.items())
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
            'ジャンル', 'Wi-fi', '飲み放題', '食べ放題',
            '個室の有無', '禁煙席の有無', '貸し切りの有無', '駐車場'
        ]
        label = [
            ttk.Label(root, text=t) for t in label_text
        ]
        combo = []  # コンボボックスが実際に格納されるリスト

        cancel = ttk.Button(root, text='キャンセル',
                            command=lambda: self.onCancelClicked())
        apply = ttk.Button(root, text='適用',
                           command=lambda: self.onApplyClicked(caller=self.caller, combo=combo))

        # region コンボボックスの定義

        for num in range(len(condition_keys)):
            c = ttk.Combobox(root, state='readonly')
            c['values'] = condition_values[num]
            current_value = self.cond[condition_keys[num]]
            # コンボボックスの初期値のインデックスをcondの値から設定
            c.current(condition_values[num].index(current_value))
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

    def onApplyClicked(self, caller, combo):
        cond = getCondition()
        for i in range(len(combo)):
            cond[condition_keys[i]] = combo[i].get()

        print(cond)

        if caller is Search:
            caller.cond = cond
            self.root.destroy()
        elif caller is Result:
            # TODO callerを閉じてResultを再生成
            r = caller.result
            caller.root.destroy()
            self.root.destroy()
            Result(result=r, cond=cond)

    def onCancelClicked(self):
        self.root.destroy()

    def onClose(self):
        tkmsg.showwarning(title='確認',
                          message='OKを押すと変更した内容は失われます')
        self.root.destroy()


class Result(Window):
    def __init__(self, result=None, cond=None):
        self.result = result
        for shop in self.result:
            print(shop['name'])
        self.cond = cond
        self.root = Tk()
        self.display_data = self.FindMatchResult(result=self.result, cond=self.cond)

        self.makeWindow(root=self.root)

    def makeWindow(self, root):

        # ウィジェットの定義
        shop_list = Listbox(root)
        shop_image = Canvas(root)
        shop_detail = Listbox(root)
        shop_others = Listbox(root)
        filter = Button(root,
                        text='フィルター',
                        command=lambda: self.onFilterClicked(cond=self.cond))
        web = Button(root,
                     text='Webページ',
                     command=lambda: self.onPageClicked(
                         self.display_data[shop_list.curselection()[0]]['url']))
        google = Button(root,
                        text='Google検索',
                        command=lambda: self.onGSearchClicked(
                            self.display_data[shop_list.curselection()[0]]['name']))

        shop_list.grid(column=0, columnspan=2, row=0, rowspan=2,
                       padx=5, pady=5)
        shop_image.grid(column=2, columnspan=2, row=0,
                        padx=5, pady=5)
        shop_detail.grid(column=4, columnspan=2, row=1,
                         padx=5, pady=5)
        shop_others.grid(column=4, columnspan=2, row=0, rowspan=2,
                         padx=5, pady=5)
        filter.grid(column=0, row=2, padx=5, pady=5, sticky=W + S)
        web.grid(column=4, row=2, padx=5, pady=5, sticky=E + S)
        google.grid(column=5, row=2, padx=5, pady=5, sticky=E + S)

        # TODO ListBoxの中身を絞り込まれたデータをもとに作成
        for shop in self.display_data:
            shop_list.insert(END, shop['name'])

        root.mainloop()

    def FindMatchResult(self, result, cond):
        # TODO condをもとにresult内のデータを絞り込む
        display_data = []
        flag = True
        for res in result:
            for key in condition_keys:
                if (cond[key] == '指定しない'):
                    continue
                else:
                    if (key == 'genre_name'):
                        if (cond[key] == '居酒屋以外'):
                            if ('居酒屋' in res.data[key]):
                                flag = False

                    else:
                        if (not cond[key] in res[key]):
                            flag = False
            if (flag == True):
                display_data.append(res)
            flag = True

        return display_data

    def onListItemClicked(self, itemNum):
        # TODO 表示する値を設定
        # TODO ImageをimageUrlから持ってくる
        pass

    def onFilterClicked(self, cond):
        Option(caller=self, cond=cond)

    def onPageClicked(self, url):
        wb.open(url=url)
        pass

    def onGSearchClicked(self, name):
        wb.open(url=urls.g_search + name)

    def onClose(self):
        pass
