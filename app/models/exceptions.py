class TaskError(Exception):
    """Erro geral relacionado a tarefas."""
    def __init__(self, message="Erro relacionado à tarefa."):
        super().__init__(message)


class TaskNotFoundError(TaskError):
    """Erro para quando uma tarefa não é encontrada."""
    def __init__(self, task_id=None, message="Tarefa não encontrada."):
        if task_id:
            message = f"Tarefa com ID '{task_id}' não foi encontrada."
        super().__init__(message)

class TaskValidationError(TaskError):
    """Erro para validação de dados."""
    def __init__(self, field=None, message=None):
        if field and not message:
            message = f"O campo '{field}' é inválido ou está vazio."
        elif field and message:
            message = f"O campo '{field}' apresenta erro: {message}"
        else:
             message = f"Erro de validação de dados."
        super().__init__(message)

class DatabaseError(Exception):
    """Erro geral relacionado ao banco de dados."""
    def __init__(self, message="Erro ao acessar o banco de dados."):
        super().__init__(message)





class ToDoError(Exception):
    """Erro geral relacionado ao ToDo."""
    def __init__(self, message="Erro relacionado ao To-Do."):
        super().__init__(message)


class TodoNotFoundError(ToDoError):
    """Erro para quando um to-do não é encontrada."""
    def __init__(self, todo_id=None, message="To-do não encontrado."):
        if todo_id:
            message = f"To-do com ID '{todo_id}' não foi encontrado."
        super().__init__(message)


class ToDoValidationError(ToDoError):
    """Erro para validação de dados."""
    def __init__(self, field=None, message=None):
        if field and not message:
            message = f"O campo '{field}' é inválido ou está vazio."
        elif field and message:
            message = f"O campo '{field}' apresenta erro: {message}"
        else:
             message = f"Erro de validação de dados."
        super().__init__(message)





class UserError(Exception):
    """Erro geral relacionado ao ToDo."""
    def __init__(self, message="Erro relacionado ao User."):
        super().__init__(message)


class UserNotFoundError(UserError):
    """Erro para quando um user não é encontrada."""
    def __init__(self, user_identificator=None, message="User não encontrado."):
        if user_identificator:
            message = f"User com identificação '{user_identificator}' não foi encontrado."
        super().__init__(message)


class InvalidPasswordError(UserError):
    """Erro para quando a senha é incorreta para autenticação."""
    def __init__(self, message="Invalid Password!"):
        super().__init__(message)

