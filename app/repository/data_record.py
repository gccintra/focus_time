import json
import logging
from ..models.task import Task
from ..models.todo import ToDo
from ..models.user import User
from ..utils.logger import logger

class DataRecord:
    def __init__(self, filename):
        self.models_classes = {
            'user.json': User,
            'task.json': Task,
            'todo.json': ToDo,
            'test_task.json': Task   
        }

        self.__filename = "app/repository/database/" +  filename
        self.model_class = self.models_classes.get(filename)

        if not self.model_class:
            logger.error(f"Arquivo '{filename}' não possui classe associada!")
            raise ValueError(f"Arquivo '{filename}' não possui classe associada!")

        self._models = []
        self.read()

    def read(self):
        try:
            with open(self.__filename, "r", encoding="utf-8") as fjson:
                file_data = json.load(fjson)
                self._models = [self.model_class(**data) for data in file_data]
        except FileNotFoundError:
            logger.warning(f"Arquivo '{self.__filename}' não encontrado! Iniciando com lista vazia.")
            self._models = []
        except json.JSONDecodeError as e:
            logger.error(f"Erro ao decodificar JSON do arquivo '{self.__filename}': {e}\n Iniciando com lista vazia.")
            self._models = []
        except Exception as e:
            logger.error(f"Erro inesperado ao ler o arquivo '{self.__filename}': {e} \n Iniciando com lista vazia.")
            self._models = []

    def write(self, model):
        try:
            if not isinstance(model, self.model_class):
                raise TypeError(f"Esperado instância de '{self.model_class.__name__}', mas recebido '{type(model).__name__}'.")

            self._models.append(model)
            self.save()
            logger.info(f"Novo registro adicionado e salvo: {model}.")
        except TypeError as e:
            logger.error(e)
            raise
        except Exception as e:
            logger.error(f"Erro ao adicionar novo registro ao banco de dados: {e}")
            raise

    def save(self):
        try:
            with open(self.__filename, "w", encoding="utf-8") as fjson:
                json.dump([model.to_dict() for model in self._models], fjson, indent=4, ensure_ascii=False)
            logger.info(f"{len(self._models)} registros salvos em '{self.__filename}'.")
        except Exception as e:
            logger.error(f"Erro ao salvar os dados no banco de dados: {e}")
            raise

    def get_models(self):
        self.read()
        return self._models
 

