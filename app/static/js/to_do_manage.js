const taskId = task_data.task_id; 

document.getElementById('createTaskToDoButton').addEventListener('click', function() {
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
          <div class="col-md-12 to-do-item">

                <div 
                    class="d-flex justify-content-between align-items-center to-do-card"
                    data-id="${data.to_do_identificator}">
        
                    <div class="to-do-text-check d-flex align-items-center">
                        <input class="form-check-input to-do-check-box me-3 mt-0 rounded-checkbox" type="checkbox" value="" aria-label="...">
                        <span class="to-do-title mb-0">${data.to_do_title}</span>
                    </div>
                    
                    <i class="bi bi-trash fs-4" id="deleteToDo"></i>
                </div>

            </div>
        `;
      document.querySelector('#toDoGridInProgress').innerHTML += toDoHTML;
      $('#newTaskToDo').modal('hide'); 
    });
  } else {
    alert("Please provide a to do task name.");
  }
});


document.querySelectorAll('.to-do-grid').forEach(grid => {
  grid.addEventListener('click', function (event) {
    const checkbox = event.target.closest('.to-do-check-box');
    if (checkbox) {
      const toDoCard = checkbox.closest('.to-do-card');
      const toDoItem = checkbox.closest('.to-do-item');
      if (toDoCard) {
        const toDoId = toDoCard.getAttribute('data-id');
        const isChecked = checkbox.checked;

        // Envia a requisição para o backend
        fetch(`/tasks/${taskId}/change_to_do_state`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ status: isChecked ? "completed" : "in progress", id: toDoId }),
        })
          .then(response => response.json())
          .then(data => {
            if (data.success) {
              
              const currentGrid = isChecked
                ? document.querySelector('#toDoGridInProgress')
                : document.querySelector('#toDoGridCompleted');
              const newGrid = isChecked
                ? document.querySelector('#toDoGridCompleted')
                : document.querySelector('#toDoGridInProgress');

              currentGrid.removeChild(toDoItem);
            
              const toDoTitle = toDoItem.querySelector('.to-do-title');
              if (toDoTitle) {
                toDoTitle.innerHTML = isChecked
                  ? `<del>${toDoTitle.textContent}</del>`
                  : toDoTitle.textContent.replace(/<del>|<\/del>/g, "");
              }

              newGrid.appendChild(toDoItem);

              checkbox.checked = isChecked;
            } else {
              alert("Erro ao atualizar o status do To-Do.");
              checkbox.checked = !isChecked; 
            }
          })
          .catch((error) => {
            console.error("Erro:", error);
            checkbox.checked = !isChecked;
          });
      }
    }
  });
});
