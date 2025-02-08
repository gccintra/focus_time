from .data_record import DataRecord
from ..utils.logger import logger
from app.models.user import User
import json
import uuid
from ..models.exceptions import UserNotFoundError



class UserRecord(DataRecord):
    def __init__(self):
        super().__init__('user.json')
        

    def id_exists(self, users_full_list, new_id):
        return any(user.identificator == new_id for user in users_full_list)

    def generate_unique_id(self):
        users_full_list = self.get_models()
        new_id = f'user-{uuid.uuid4()}'
        while self.id_exists(users_full_list, new_id):
            new_id = f'user-{uuid.uuid4()}'
        return new_id
    

    def read(self):
        try:
            with open(self._filename, "r", encoding="utf-8") as fjson:
                file_data = json.load(fjson)
                self._models = [self.model_class(**data, hashed=True) for data in file_data] 
        except FileNotFoundError:
            logger.warning(f"Arquivo '{self._filename}' não encontrado! Iniciando com lista vazia.")
            self._models = []
        except json.JSONDecodeError as e:
            logger.error(f"Erro ao decodificar JSON do arquivo '{self._filename}': {e}\n Iniciando com lista vazia.")
            self._models = []
        except Exception as e:
            logger.error(f"Erro inesperado ao ler o arquivo '{self._filename}': {e} \n Iniciando com lista vazia.")
            self._models = []

    # Depois criar um get_user_by_any_data e usar getattr pro user.email por exemplo, da pra usar so uma funcao pra buscar o usuario por qualquer dado, só colocar o dado que eu quero como um parametro
    def get_user_by_email(self, email):
        users_list = self.get_models()
        for user in users_list:
            if user.email == email:
                logger.info(f'User com email "{email}" encontrada com sucesso!')
                return user
        logger.warning(f"User com e-mail '{email}' não foi encontrado.")
        raise UserNotFoundError(user_identificator=email)
    

    def get_user_by_id(self, user_id):
        users_list = self.get_models()
        for user in users_list:
            if user.identificator == user_id:
                logger.info(f'User com id "{user_id}" encontrada com sucesso!')
                return user
        logger.warning(f"User com id '{user_id}' não foi encontrado.")
        raise UserNotFoundError(user_identificator=user_id)
    
