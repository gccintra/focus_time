document.addEventListener('DOMContentLoaded', function() {
    const ctx = document.getElementById('myPieChart').getContext('2d');
    
    fetch(`/tasks/get_data_for_chart`)
        .then(response => response.json())
        .then(data => {
            if (data.createChart){
                const labels = data.tasks.map(task => task.title);
                const taskMinutes = data.tasks.map(task => task.minutes);
                const colors = data.tasks.map(task => task.color);

                new Chart(ctx, {
                    type: 'doughnut',
                    data: {
                        labels: labels,
                        datasets: [{
                            data: taskMinutes,
                            backgroundColor: colors,
                            borderColor: 'none'
                        }]
                    },
                    options: {
                        //responsive: true,
                        plugins: {
                            title: {
                                align: 'start',
                                display: true,
                                text: 'Today Resume',
                                color: '#ffffff', // Cor do título
                                font: {
                                    size: 32 // Tamanho do texto do título
                                }
                            },
                            legend: {
                                position: window.innerWidth <= 768 ? 'bottom' : 'right', 
                                labels: {
                                    color: '#ffffff',
                                    padding: 30,  
                                    usePointStyle: true,
                                    useBorderRadius: true,  // Faz os ícones redondos
                                    pointStyle: 'circle',  // Define o estilo dos ícones como círculos
                                    font: {
                                        size: 14
                                    }
                                }
                            }
                        }
                    }
                });
            }else {
                document.getElementById('myPieChart').style.display = 'none'; // Esconde o canvas se não houver dados
                console.log("Nenhum dado disponível para o gráfico.");
            }
        }).catch(error => console.error("Erro ao carregar dados:", error));
});