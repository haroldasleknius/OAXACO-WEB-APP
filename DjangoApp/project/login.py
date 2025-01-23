class userlogin:
    def __init__(self):
        self.username = None
        self.password = None
        self.role = None
        self.status = False
        self.name = None
        self.surname = None
        self.order = None
        self.assistance = None

    def store_order(self,order):
        self.order = order

    def set_details(self,username,password,role,name,surname):
        self.username = username
        self.password = password
        self.role = role
        self.name = name
        self.surname = surname

    def login(self):
        self.status = True
        self.assistance = False

    def logout(self):
        self.status = False
        self.username = None
        self.password = None
        self.role = None
        self.name = None
        self.surname = None