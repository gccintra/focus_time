function inicializateChartContent(){
    const tasks = document.querySelectorAll('.custom-card');

    tasks.forEach((task, index) => { // Passando o índice do forEach aqui
        const taskId = task.getAttribute('data-id');
        const ctx = document.getElementById(`myPieChart-${taskId}`).getContext('2d');
    
        fetch(`/tasks/get_data_for_chart_my_tasks_menu/${taskId}`)
            .then(response => response.json())
            .then(data => {
                if (data.createChart) {
                    const labels = data.tasks.map(task => task.title);
                    const taskMinutes = data.tasks.map(task => task.minutes);
                    const colors = data.tasks.map(task => task.color);

                    const totalMinutes = taskMinutes.reduce((a, b) => a + b, 0); // Calcula o total de minutos
                    const percentage = ((taskMinutes[index] / totalMinutes) * 100).toFixed(1); // Porcentagem da tarefa específica
                    console.log(taskMinutes)
                    console.log(labels)
                    console.log(percentage)
                    new Chart(ctx, {
                        type: 'doughnut',
                        data: {
                            labels: labels,
                            datasets: [{
                                data: taskMinutes,
                                backgroundColor: colors,
                                borderColor: 'transparent',
                                hoverBackgroundColor: colors
                            }]
                        },
                        options: {
                            cutout: '70%', // Tamanho do buraco no centro
                            plugins: {
                                legend: {
                                    display: false // Remove a legenda
                                },
                                tooltip: {
                                    enabled: false // Desabilita os tooltips
                                }
                            }
                        },
                        plugins: [{
                            id: 'centerText',
                            beforeDraw: function(chart) {
                                const ctx = chart.ctx;
                                const { width } = chart;
                                const { height } = chart;
                                const centerX = width / 2;
                                const centerY = height / 2;
                        
                                // Calcula o raio interno e externo
                                const innerRadius = chart._metasets[0].data[0].innerRadius; // Valor padrão caso seja undefined
                                const outerRadius = chart._metasets[0].data[0].outerRadius;
                        
                                console.log("Raio interno:", innerRadius, "Raio externo:", outerRadius);
                        
                                // Fundo preto no centro
                                ctx.save();
                                ctx.beginPath();
                                ctx.arc(centerX, centerY, innerRadius, 0, Math.PI * 2);
                                ctx.fillStyle = '#212121';
                                ctx.fill();
                                ctx.restore();
                        
                                // Texto no centro
                                ctx.font = 'bold 20px Arial';
                                ctx.fillStyle = 'white';
                                ctx.textAlign = 'center';
                                ctx.textBaseline = 'middle';
                                ctx.fillText(`${percentage}%`, centerX, centerY);
                            }
                        }]                        
                    });
                } else {
                    document.getElementById(`myPieChart-${taskId}`).style.display = 'none'; // Esconde o canvas se não houver dados
                    console.log("Nenhum dado disponível para o gráfico.");
                }
            })
            .catch(error => console.error("Erro ao carregar dados:", error));
    });
   
};


document.addEventListener('DOMContentLoaded', function() {
    inicializateChartContent();
});

function reinitializateChartContentAfterDOMUpdate(){
    inicializateChartContent();
}