import json
import logging
import uuid
from ..models.task import Task
from ..models.user import User

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

class DataRecord:
    def __init__(self, filename):
        self.models_classes = {
            'user.json': User,
            'task.json': Task,
        }

        self.__filename = "app/database/" +  filename
        self.model_class = self.models_classes.get(filename)

        if not self.model_class:
            logging.error(f"Arquivo '{filename}' não possui classe associada!")
            raise ValueError(f"Arquivo '{filename}' não possui classe associada!")

        self._models = []
        self.read()

    def read(self):
        try:
            with open(self.__filename, "r", encoding="utf-8") as fjson:
                file_data = json.load(fjson)
                self._models = [self.model_class(**data) for data in file_data]
            logging.info(f"{len(self._models)} registros carregados de '{self.__filename}'.")
        except FileNotFoundError:
            logging.warning(f"Arquivo '{self.__filename}' não encontrado! Iniciando com lista vazia.")
            self._models = []
        except Exception as e:
            logging.error(f"Erro ao ler o arquivo '{self.__filename}': {e}")
            self._models = []

    def write(self, model):
        if not isinstance(model, self.model_class):
            logging.error(f"Tipo inválido: esperado '{self.model_class.__name__}', recebido '{type(model).__name__}'.")
            raise TypeError(f"Esperado instância de '{self.model_class.__name__}', mas recebido '{type(model).__name__}'.")

        self._models.append(model)
        self.save()
        logging.info(f"Novo registro adicionado e salvo: {model}.")

    def save(self):
        """Salva os modelos no arquivo JSON."""
        try:
            with open(self.__filename, "w", encoding="utf-8") as fjson:
                json.dump([model.to_dict() for model in self._models], fjson, indent=4, ensure_ascii=False)
            logging.info(f"{len(self._models)} registros salvos em '{self.__filename}'.")
        except Exception as e:
            logging.error(f"Erro ao salvar os dados: {e}")

    def get_models(self):
        """Retorna todos os modelos carregados."""
        self.read()
        return self._models

