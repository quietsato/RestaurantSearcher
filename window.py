import attributes as att, keys

class Window():
    size = ''

    def onClose(self):
        pass


class Search(Window):
    def __init__(self):
        self.size = ''
        isCityName = False

    def onSearchClicked(self, isCityName, cond, params):
        if (isCityName):
            # TODO call Geocoding API
            pass
        # TODO make a Result Instance

    def onOptionClicked(self, cond):
        # TODO make a Option Instance
        return cond

    def onClose(self):
        super().onClose()


class Option(Window):
    def __init__(self, host, cond):
        pass

    def onApplyClicked(self, cond):
        pass

    def onClose(self):
        pass


class Result(Window):
    def __init__(self, result, cond):
        pass

    def onListItemClicked(self, itemNum):
        pass

    def onFilterClicked(self, cond):
        pass

    def onPageClicked(self, url):
        pass

    def onGSearchClicked(self, name):
        pass

    def onClose(self):
        pass
