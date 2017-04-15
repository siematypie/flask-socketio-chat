class User:
    users = []
    def __init__(self, name, sid):
        self.name = name
        self.sid = sid
        self.users.append(self)

    @classmethod
    def get_user_by_sid(cls, sid):
        return next((usr for usr in cls.users if usr.sid == sid), None)

    @classmethod
    def get_user_by_name(cls, name):
        return next((usr for usr in cls.users if usr.name == name), None)
