# import pytest
# from app.repository.task_record import TaskRecord
# from app.models.task import Task
# from app.models.todo import ToDo
# from app.models.exceptions import TaskNotFoundError

# TASK_FILE = "test_task.json"

# @pytest.fixture
# def task_record():
#     return TaskRecord(TASK_FILE)

# def test_generate_unique_id(task_record):
#     unique_id = task_record.generate_unique_id()
#     assert isinstance(unique_id, str)
#     assert len(unique_id) > 0

# def test_get_task_by_id_success(task_record):
#     task = task_record.get_task_by_id("task1")
#     assert isinstance(task, Task)
#     assert task.identificator == "task1"

# def test_get_task_by_id_failure(task_record):
#     with pytest.raises(TaskNotFoundError):
#         task_record.get_task_by_id("invalid_id")

# def test_create_to_do(task_record):
#     to_do = ToDo(to_do_title="New To-Do")
#     task_record.create_to_do("task1", to_do)

#     task = task_record.get_task_by_id("task1")
#     assert len(task.task_to_do_list) == 1
#     assert task.task_to_do_list[0].to_do_title == "New To-Do"


# def test_update_to_do_status(task_record):
#     task = task_record.get_task_by_id("task1")
#     updated_to_do = ToDo(
#         to_do_title="New To-Do",
#         to_do_identificator=task.task_to_do_list[0].to_do_identificator,
#         to_do_completed_time="2025-01-25T12:00:00",
#         to_do_status="completed"
#     )
#     result = task_record.update_to_do_status(task, updated_to_do)
#     assert result is True
#     assert task.task_to_do_list[0].to_do_status == "completed"

# def test_save_task_to_do_list_in_db(task_record):
#     task = task_record.get_task_by_id("task1")
#     initial_to_do_list_length = len(task.task_to_do_list)
#     to_do = ToDo(to_do_title="Another To-Do")
#     task.task_to_do_list.append(to_do)

#     task_record.save_task_to_do_list_in_db(task)
#     assert len(task.task_to_do_list) == initial_to_do_list_length + 1
