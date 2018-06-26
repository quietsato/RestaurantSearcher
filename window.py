import attributes as att, keys, urls
import io, PIL.Image
import tkinter as tk
import tkinter.messagebox as tkmsg
import requests as rq
import webbrowser as wb


# print('Please run main.py')
# exit(0)


class Window:
    size = ''

    def onClose(self):
        pass


class Search(Window):
    def __init__(self):
        self.size = ''
        isCityName = False

    def onSearchClicked(self, isCityName, cond, params):
        if (isCityName):
            params = self.getLatLonByCity(params[0])
            pass
        result = self.getRDataByLatLon(params)
        if result == 'NOT FOUND':
            return
        r = Result(result, cond)

    def onOptionClicked(self, cond):
        o = Option(caller=self, cond=cond)
        return cond

    def onClose(self):
        # TODO ダイアログを生成
        super().onClose()

    def getLatLonByCity(self, cityName):
        res = rq.get(urls.g_apiurl, {'address': cityName, 'key': keys.g_KEY}).json()
        if res['status'] != 'OK':
            tkmsg.showinfo('見つかりませんでした',
                           '異なるデータで再度お試しください')
            return 'NOT FOUND'

        location = [
            str(res['results'][0]['geometry']['location']['lat']),
            str(res['results'][0]['geometry']['location']['lng'])
        ]
        return location

    def getRDataByLatLon(self, location):
        # TODO それぞれのレストランのデータをList<Data>としてreturn
        d = att.Data(json={'key': 'value'})
        return d


class Option(Window):
    # THINK ABOUT WHERE BY ALSO GOOD!!!

    def __init__(self, caller, cond):
        self.cond = cond
        # TODO チェックボックスの状態をcondをもとに指定
        pass

    def onApplyClicked(self, caller, cond):
        # TODO チェックボックスをもとにcondのフィールドを指定
        if caller is Search:
            # TODO condをcallerにreturn
            pass
        elif caller is Result:
            # TODO callerを閉じてResultを再生成
            pass
        pass

    def onCancelClicked(self):
        pass

    def onClose(self):
        # TODO 何もいじっていないcondをcallerにreturn
        pass


class Result(Window):
    def __init__(self, result, cond):
        # TODO condをもとにresult内のデータを絞り込む
        # TODO ListBoxの中身を絞り込まれたデータをもとに作成
        pass

    def onListItemClicked(self, itemNum):
        # TODO 表示する値を設定
        # TODO ImageをimageUrlから持ってくる
        pass

    def onFilterClicked(self, cond):
        o = Option(caller=self, cond=cond)
        pass

    def onPageClicked(self, url):
        # TODO webbrowserで受け取ったurlを開く
        pass

    def onGSearchClicked(self, name):
        # TODO webbrowserで生成したurlを開く
        pass

    def onClose(self):
        pass
