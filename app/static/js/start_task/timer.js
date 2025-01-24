let timerInterval;
let saveInterval;
let elapsedTime = parseInt(task_data.today_total_seconds) || 0;
let isRunning = false;
let startTime


document.addEventListener("DOMContentLoaded", function() {
    const startButton = document.querySelector("#timerButton");
    const timerDisplay = document.getElementById("timerDisplay");
    const taskId = task_data.task_id; 

    startButton.addEventListener("click", function() {
        if (isRunning) {
            stopTimer()
        } else {
            startTimer()
        }
    });

    function startTimer(){
        startTime = Date.now() - elapsedTime * 1000;
        isRunning = true;
        startButton.textContent = "Stop";


        timerInterval = setInterval(() => {
            elapsedTime = Math.floor((Date.now() - startTime) / 1000);
            updateTimerDisplay(timerDisplay, elapsedTime);
        }, 1000);

        saveInterval = setInterval(() => {
            saveElapsedTime();
        }, 60000)

    }

    function stopTimer(){
        clearInterval(timerInterval);
        clearInterval(saveInterval);
        isRunning = false;
        startButton.textContent = "Start";

        saveElapsedTime()
    }

    function saveElapsedTime(){
        fetch(`/tasks/update_task_time/${taskId}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ elapsed_seconds: elapsedTime })
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
        })
        .catch(error => console.error("Erro ao atualizar:", error));
    }

    function updateTimerDisplay(timerDisplay, seconds) {
        const hours = String(Math.floor(seconds / 3600)).padStart(2, '0');
        const minutes = String(Math.floor((seconds % 3600) / 60)).padStart(2, '0');
        const secs = String(seconds % 60).padStart(2, '0');
        timerDisplay.textContent = `${hours}:${minutes}:${secs}`;
    }

    window.addEventListener("beforeunload", function () {
        if (isRunning) {
            clearInterval(timerInterval);
            clearInterval(saveInterval);
            isRunning = false;
            startButton.textContent = "Start";
            
            // envia um request assíncrono e não bloqueante para um servidor web. O request não espera por uma resposta.
            const url = `/tasks/update_task_time/${taskId}`;
            const data = JSON.stringify({ elapsed_seconds: elapsedTime });
            const blob = new Blob([data], { type: "application/json" });
    
            navigator.sendBeacon(url, blob);
        }
    });
});

