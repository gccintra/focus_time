import bcrypt


class User:
    def __init__(self, identificator, username, email, password, status=None, hashed=False):
        self.identificator = identificator
        self.username = username
        self.email = email
        self.password = password if hashed else self.generate_password_hash(password)
        self.status = status or 'active'

    def generate_password_hash(self, password):
        """Gera um hash seguro para a senha"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def verify_password(self, password):
        """Verifica se a senha digitada corresponde ao hash salvo"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    def to_dict(self):
        """Retorna um dicionário representando o usuário"""
        return {
            "identificator": self.identificator,
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "status": self.status
        } 
    


