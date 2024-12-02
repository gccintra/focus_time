import json
import uuid

class DataRecord:
    """Banco de dados JSON para os recursos Gerente e Empregados."""

    def __init__(self, filename):
        self.__filename = "app/database/" +  filename
        self.__models = []
        self.read()

    def read(self):
        try:
            with open(self.__filename, "r", encoding="utf-8") as fjson:
                self.__models = json.load(fjson)
        except FileNotFoundError:
            print(f"O arquivo {self.__filename} não existe!")
            self.__models = []

    def write(self, model):
        try:
            self.__models.append(vars(model))  # Converte o objeto em um dicionário.
            self.save()
        except Exception as e:
            print(f"Erro ao adicionar o modelo: {e}")

    def save(self):
        try:
            with open(self.__filename, "w", encoding="utf-8") as fjson:
                json.dump(self.__models, fjson, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao salvar os dados: {e}")

    def get_models(self):
        return self.__models

    def id_exists(self, tasks, new_id):
        return any(task.get('id', 0) == new_id for task in tasks)

    def generate_unique_id(self):
        new_id = str(uuid.uuid4())
        while self.id_exists(self.__models, new_id):
            new_id = str(uuid.uuid4())  # Tenta gerar outro se já existir
        return new_id