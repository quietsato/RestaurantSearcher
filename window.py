import keys, urls
from attributes import *
import io, PIL.Image
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

    def onClose(self):
        pass


class Search(Window):
    def __init__(self):
        self.size = '300x250'
        self.isCityName = False
        self.makeWindow(root=Tk())

    def makeWindow(self, root):
        # TODO ウィンドウの中身をここに記述

        root.geometry(self.size)
        root.columnconfigure(1, weight=1)
        root.columnconfigure(2, weight=1)
        root.rowconfigure(8, weight=1)

        # TODO ラジオボタンの初期値を設定する

        label1 = ttk.Label(root,
                           text='検索条件：').grid(column=0, row=0, padx=5, pady=5, sticky=W)
        oButton = ttk.Button(root,
                             text='詳細検索').grid(column=2, row=0, padx=5, pady=5, sticky=E)

        lButton = ttk.Radiobutton(root,
                                  text='緯度・経度',
                                  value=False,
                                  variable=self.isCityName).grid(column=0, columnspan=2, row=1,
                                                                 padx=10, pady=5, sticky=W)

        cButton = ttk.Radiobutton(root,
                                  text='都市名・建物名',
                                  value=True,
                                  variable=self.isCityName).grid(column=0, columnspan=2, row=2, padx=10, sticky=W)

        latLabel = ttk.Label(root,
                             text='緯度').grid(row=4, padx=5, pady=5, sticky=E)
        self.latEntry = ttk.Entry(root
                             ).grid(column=1, columnspan=2, row=4, padx=5, pady=5, sticky=W + E)
        lngLabel = ttk.Label(root,
                             text='経度').grid(row=5, padx=5, pady=5, sticky=E)
        self.lngEntry = ttk.Entry(root,
                                  ).grid(column=1, columnspan=2, row=5, padx=5, pady=5, sticky=W + E)

        cityLabel = ttk.Label(root,
                              text='都市・建物').grid(row=7, padx=5, pady=5, sticky=E)
        self.cityEntry = ttk.Entry(root
                                   ).grid(column=1, columnspan=2, row=7, padx=5, pady=5, sticky=W + E)

        sButton = ttk.Button(root,
                             text='検索する').grid(column=2, row=8, padx=5, pady=5, sticky=E + S)

        root.mainloop()

    def onSearchClicked(self, isCityName, cond, params):
        if (isCityName):
            params = self.getLatLngByCity(params[0])
            if params == 'NOT FOUND':
                return
        result = self.getRDataByLatLng(params)
        # r = Result(result, cond)
        return result

    def onOptionClicked(self, cond):
        Option(caller=self, cond=cond)

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
        res = rq.get(url=urls.h_apiurl, params={
            'key': keys.h_KEY,
            'lat': location[0],
            'lng': location[1],
            'format': 'json',
            'count': '100'
        }).json()
        r_data = [
            Data(shop)
            for shop in res['results']['shop']
        ]
        return r_data


class Option(Window):
    # THINK ABOUT WHERE BY ALSO GOOD!!!

    def __init__(self, caller, cond):
        self.root = Tk()
        self.cond = cond
        self.makeWindow(root=Tk())
        # TODO チェックボックスの状態をcondをもとに指定
        pass

    def makeWindow(self, root):
        # TODO チェックボックスの状態をcondをもとに指定
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
