document.getElementById('createTaskToDoButton').addEventListener('click', function() {
    const taskId = task_data.task_id; 
    var taskToDoName = document.getElementById('taskToDoName').value;

    if (taskToDoName.trim() !== "") {


      fetch(`/tasks/${taskId}/new_task_to_do`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ name: taskToDoName })
      })
      .then(response => response.json())
      .then(data => {
         var toDoHTML = `
            <div class="col-md-12">

                <div 
                    class="d-flex justify-content-between align-items-center to-do-card"
                    data-id="${data.to_do_identificator }">
        
                    <div class="d-flex align-items-center" id="toDoTextCheck">
                        <input class="form-check-input me-3 mt-0 rounded-checkbox" type="checkbox" id="checkboxNoLabel" value="" aria-label="...">
                        <span id="taskTitle" class="mb-0">${data.to_do_title}</span>
                    </div>
                    
                    <i class="bi bi-trash fs-4" id="deleteToDo"></i>
                </div>

            </div>
         `;
        document.querySelector('#toDoGrid').innerHTML += toDoHTML;
        $('#newTaskToDo').modal('hide'); 
      });
    } else {
      alert("Please provide a to do task name.");
    }
  });