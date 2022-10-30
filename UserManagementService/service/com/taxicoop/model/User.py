class User:
    def __init__(self, name, email, mobile,
                 user_id=str(uuid.uuid4()),
                 ):
        self.user_id = user_id
        self.email = email
        self.mobile = mobile
        self.name = name
