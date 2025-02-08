from app.services.auth_service import AuthService
from flask import jsonify, make_response

class AuthController():
    def __init__(self):
        self.service = AuthService()


    def create_user(self, data):
        user_email = data.get('email')
        username = data.get('username')
        password = data.get('password')

        user = self.service.create_user(user_email, username, password)

        return jsonify({
            "success": True,
            "message": "User created successfully",
            "data": None,
            "error": None
        }), 200
    

    def login(self, data):
        user_email = data.get('email')
        password = data.get('password')

        token = self.service.login(user_email, password)

        response = make_response(jsonify({
            "success": True,
            "message": "Login realizado com sucesso",
            "data": {
                "token": token
            }, 
            "error": None
        }), 200)

        # Adiciona um cookie com o token JWT
        response.set_cookie('auth_token', token, httponly=True, secure=True, samesite='Lax')

        return response