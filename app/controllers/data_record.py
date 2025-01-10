import json
import uuid

class DataRecord:
    def __init__(self, filename):
        self.__filename = "app/database/" +  filename
        self._models = []
        self.read()

    def read(self):
        try:
            with open(self.__filename, "r", encoding="utf-8") as fjson:
                self._models = json.load(fjson)
        except FileNotFoundError:
            print(f"O arquivo {self.__filename} não existe!")
            self._models = []

    def write(self, model):
        try:
            self._models.append(vars(model))  # Converte o objeto em um dicionário.
            self.save()
        except Exception as e:
            print(f"Erro ao adicionar o modelo: {e}")

    def save(self):
        try:
            with open(self.__filename, "w", encoding="utf-8") as fjson:
                json.dump(self._models, fjson, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao salvar os dados: {e}")

    def get_models(self):
        self.read()
        return self._models

