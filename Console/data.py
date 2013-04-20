import os
import pytality

data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')


def load_buffer(file_name, x=0, y=0, **kwargs):
    with open(os.path.join(data_dir, file_name)) as f:
        buf = pytality.ansi.read_to_buffer(f, **kwargs)
        if x:
            buf.x = x
        if y:
            buf.y = y
        return buf
