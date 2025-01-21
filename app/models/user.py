class User():
    def __init__(self, username, password, name, email, email_token, tasks=[]):
        self.username = username
        self.password = password
        self.name = name
        self.email = email
        self.email_token = email_token
        self.tasks = tasks