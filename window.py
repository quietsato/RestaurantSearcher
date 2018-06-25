import attributes as att, keys, urls

print('Please run main.py')
exit(0)


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
        r = Result(result, cond)

    def onOptionClicked(self, cond):
        o = Option(caller=self, cond=cond)
        return cond

    def onClose(self):
        # TODO ダイアログを生成
        super().onClose()

    def getLatLonByCity(self, cityName):
        # TODO Geocoding APIを使用する
        location = [0, 0]
        return location

    def getRDataByLatLon(self, location):
        # TODO それぞれのレストランのデータをList<Data>としてreturn
        d = att.Data(json={'key': 'value'})
        return d


class Option(Window):
    # THINK ABOUT WHERE BY ALSO GOOD!!!

    def __init__(self, caller, cond):
        # TODO チェックボックスの状態をcondをもとに指定
        pass

    def onApplyClicked(self, caller, cond):
        # TODO チェックボックスをもとにcondのフィールドを指定
        if (caller is Search):
            # TODO condをcallerにreturn
            pass
        elif (caller is Result):
            # TODO callerを閉じてResultを再生成
            pass
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
        pass

    def onGSearchClicked(self, name):
        pass

    def onClose(self):
        pass
