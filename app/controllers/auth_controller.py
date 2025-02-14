from app.services.auth_service import AuthService
from flask import jsonify, make_response
from ..models.exceptions import UserNotFoundError, InvalidPasswordError
from ..utils.logger import logger


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
            "message": "Account created successfully",
            "data": None,
            "error": None
        }), 200
    
    # Tratativa, e se não tiver sido enviado o email e password corretamente? e se ficar como none ... vai dar erro quando tentar instanciar
    def login(self, data):
        try:
            user_email = data.get('email')
            password = data.get('password')

            token = self.service.login(user_email, password)

            response = make_response(jsonify({
                "success": True,
                "message": "Login realizado com sucesso",
                "data": None, 
                "error": None
            }), 200)

            response.set_cookie('auth_token', token, httponly=True, secure=True, samesite='Strict')

            return response
        except (UserNotFoundError, InvalidPasswordError):
            return jsonify({
                "success": False,
                "message": "Invalid credentials",
                "data": None,
                "error": {
                    "code": 401,
                    "type": "InvalidCredentials",
                    "details": "Invalid Password or E-mail"
                }
            }), 401
        except Exception as e:   
            return jsonify({
                "success": False,
                "message": "Something went wrong. Please try again later.",
                "data": None,
                "error": {
                    "code": 500,
                    "type": "InternalServerError",
                    "details": str(e)
                }
            }), 500