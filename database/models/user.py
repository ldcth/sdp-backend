from datetime import datetime

class User:
    def __init__(self, role=0, name="", email="", password="", histories=None):
        self.role = role
        self.name = name
        self.email = email
        self.password = password
        self.histories = histories or []
        self._id = None
        self.createdAt = datetime.utcnow()
        self.updatedAt = datetime.utcnow()

    def to_dict(self):
        obj_dict = self.__dict__.copy()
        if self._id is None:
            obj_dict.pop('_id', None)
        return obj_dict 