document.getElementById('createTask').addEventListener('click', function() {
    var taskName = document.getElementById('taskName').value;
    var taskColor = document.getElementById('taskColor').value;

    if (taskName.trim() !== "") {
      fetch("/tasks/new_task", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ name: taskName, color: taskColor })
      })
      .then(response => response.json())
      .then(data => {
        var taskHTML = `
          <div class="col-md-4">
            <div class="custom-card" style="border-color : ${data.color}" data-id="${data.id}">
              <h3>${data.name}</h3>
              <p>Today: ${data.today_total_time}</p>
              <p>Week: ${data.week_total_time}</p>
            </div>
          </div>
        `;
        document.querySelector('#taskGrid').innerHTML += taskHTML;
        $('#newTask').modal('hide'); 
      });
    } else {
      alert("Please provide a task name.");
    }
  });