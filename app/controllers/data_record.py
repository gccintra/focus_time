import json
import uuid
from ..models.task import Task
from ..models.user import User

class DataRecord:
    # MUDAR AQUI E REFATORAR TUDO
    # Guardar na models as classes já instânciadas
    # Vou ter que criar varios tipos de data record e ter que mudar todo o código para mexer diretamente com a instância e não com o dict
    def __init__(self, filename):
        self.models_classes = {
            'user.json': User,
            'task.json': Task,
        }

        self.__filename = "app/database/" +  filename
        self.model_class = self.models_classes.get(filename)

        if not self.model_class:
            raise ValueError(f"Arquivo '{filename}' não possui classe associada!")

        self._models = []
        self.read()

    def read(self):
        try:
            with open(self.__filename, "r", encoding="utf-8") as fjson:
                file_data = json.load(fjson)
                self._models = [self.model_class(**data) for data in file_data]
        except FileNotFoundError:
            print(f"Arquivo '{self.__filename}' não encontrado! Iniciando com lista vazia.")
            self._models = []
        except Exception as e:
            print(f"Erro ao ler o arquivo '{self.__filename}': {e}")
            self._models = []

    def write(self, model):
        """Adiciona um novo modelo e salva no arquivo."""
        if not isinstance(model, self.model_class):
            raise TypeError(f"Esperado instância de '{self.model_class.__name__}', mas recebido '{type(model).__name__}'.")

        self._models.append(model)
        self.save()


    # Nesse caso é obrigatório ter o to_dict em todas as classes. (Criar uma model pai para abstrair isso, fazendo o método ser obrigatório)
    def save(self):
        """Salva os modelos no arquivo JSON."""
        try:
            with open(self.__filename, "w", encoding="utf-8") as fjson:
                json.dump([model.to_dict() for model in self._models], fjson, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao salvar os dados: {e}")

    def get_models(self):
        """Retorna todos os modelos carregados."""
        self.read()
        return self._models

