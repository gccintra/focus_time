let timerInterval;
let elapsedTime = parseInt(task_data.today_total_seconds) || 0;
let isRunning = false;

document.addEventListener("DOMContentLoaded", function() {
    const startButton = document.querySelector(".btn-primary");
    const timerDisplay = document.getElementById("timerStr");
    const taskId = task_data.task_id; 

    startButton.addEventListener("click", function() {
        if (isRunning) {
            // Parar cronômetro e enviar dados para o backend
            clearInterval(timerInterval);
            isRunning = false;
            startButton.textContent = "Start";

            // Enviar minutos para o backend
            fetch(`/tasks/update_task_time/${taskId}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ elapsed_minutes: Math.floor(elapsedTime / 60) })
            })
            .then(response => response.json())
            .then(data => {
                console.log("Tempo atualizado no backend:", data);
            })
            .catch(error => console.error("Erro ao atualizar:", error));
        } else {
            isRunning = true;
            startButton.textContent = "Stop";
            updateTimerDisplay(timerDisplay, elapsedTime);
            timerInterval = setInterval(() => {
                elapsedTime += 60;
                updateTimerDisplay(timerDisplay, elapsedTime);
            }, 1000);
        }
    });

    function updateTimerDisplay(timerDisplay, seconds) {
        const hours = String(Math.floor(seconds / 3600)).padStart(2, '0');
        const minutes = String(Math.floor((seconds % 3600) / 60)).padStart(2, '0');
        const secs = String(seconds % 60).padStart(2, '0');
        timerDisplay.textContent = `${hours}:${minutes}:${secs}`;
    }
});
