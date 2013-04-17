import pytality


class MessageLog(pytality.buffer.MessageBox):
    title = None
    def __init__(self, **kwargs):
        super(MessageLog, self).__init__(**kwargs)
        self.title = pytality.buffer.PlainText("[ Message Log ]", y=-1, fg=pytality.colors.WHITE)
        self.title.x = (self.inner_width / 2) - (self.title.width / 2) - 1

        self.scroll_cursor = pytality.buffer.NoScrollbar()

    def recalculate_buffers(self):
        super(MessageLog, self).recalculate_buffers()
        if self.title:
            self.children.append(self.title)
