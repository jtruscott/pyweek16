import os
import pytality

data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')


def load_buffer(file_name, **kwargs):
    with open(os.path.join(data_dir, file_name)) as f:
        return pytality.ansi.read_to_buffer(f, **kwargs)
