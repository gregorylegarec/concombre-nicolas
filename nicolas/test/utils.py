from nicolas import ConcombreStore


class mocked_object:
    def __init__(self, id=None, name=None, display_name=None):
        self.id = id
        self.name = name
        self.display_name = display_name if display_name else name


def mock_user(id, name):
    return mocked_object(id, name=name)


def mock_channel(id):
    return mocked_object(id)
