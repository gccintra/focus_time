import pytest
from app.repository.data_record import DataRecord
from app.models.task import Task

TASK_FILE = "test_task.json"

@pytest.fixture
def data_record():
    return DataRecord(TASK_FILE)

def test_data_record_initialization_task(data_record):
    assert data_record.model_class == Task
    assert data_record._DataRecord__filename == "app/repository/database/" + TASK_FILE

def test_write_and_save(data_record):
    task = Task(
        identificator="task1",
        title="Test Task",
        color="blue",
        seconds_in_focus_per_day={"2025-01-24": 3600},
        task_to_do_list=[],
    )
    data_record.write(task)
    data_record.save()

    saved_data = data_record.get_models()
    assert len(saved_data) == 1
    assert saved_data[0].identificator == "task1"
    assert saved_data[0].title == "Test Task"
    assert saved_data[0].color == "blue"
