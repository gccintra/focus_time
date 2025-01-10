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
        // var taskHTML = `
        //   <div class="col-md-4">
        //     <div class="custom-card" style="border-color : ${data.color}" data-id="${data.id}">
        //       <h3>${data.name}</h3>
        //       <p>Today: ${data.today_total_time}</p>
        //       <p>Week: ${data.week_total_time}</p>
        //     </div>
        //   </div>
        // `;
        // document.querySelector('#taskGrid').innerHTML += taskHTML;
        $('#newTaskToDo').modal('hide'); 
      });
    } else {
      alert("Please provide a to do task name.");
    }
  });