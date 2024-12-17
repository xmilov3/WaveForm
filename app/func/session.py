class UserSession:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UserSession, cls).__new__(cls)
            cls._instance.user_id = None
            cls._instance.username = None
        return cls._instance

    def set_user(self, user_id, username):
        self.user_id = user_id
        self.username = username

    def get_user_id(self):
        return self.user_id

    def get_username(self):
        return self.username

user_session = UserSession()
