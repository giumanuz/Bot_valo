class MockUser:
    def __init__(self,
                 user_id=-1,
                 first_name=""):
        self._id = user_id
        self._first_name = first_name

    @property
    def id(self):
        return self._id

    @property
    def first_name(self):
        return self._first_name
