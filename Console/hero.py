import pytality


class StatDisplay(pytality.buffer.Box):
    def __init__(self, **kwargs):
        super(StatDisplay, self).__init__(**kwargs)
        self.title = pytality.buffer.PlainText("[ Hero Stats ]", y=-1, fg=pytality.colors.WHITE)
        self.title.x = (self.inner_width / 2) - (self.title.width / 2)
        self.children.append(self.title)

