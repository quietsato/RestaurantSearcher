import keys, urls
from attributes import *
import io, PIL.Image
import tkinter as tk
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
        self.size = ''
        isCityName = False
        self.makeWindow(root=tk.Tk())

    def makeWindow(self, root):
        # TODO ウィンドウの中身をここに記述
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
        self.root = tk.Tk()
        self.cond = cond
        self.makeWindow(root=tk.Tk())
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
        self.makeWindow(root=tk.Tk())

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
