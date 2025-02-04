# Doing (MVP):

- [ ] Validações de campo (Title)
- [ ] Getters e Setters, + Segurança
    - [ ] Validações ao tentar criar uma task com id igual (hard coded)
    - [ ] Adicionar cache em memória usando bibliotecas como functools.lru_cache.
- [ ] Layout de Today e Week na página principal
- [x] Padrão de dados retornados para o front-end (TASKS)
- [x] Tratamento de Erros e Apresentação de Mensagens (Front-End)
    - [x] To Do
    - [x] Tasks
- [x] Ordenação das tasks por maior porcentagem. (ta com bug)
- [ ] Autenticação com JWT
    - [ ] Register
    - [ ] Login
    - [ ] Logout
- [ ] Websocket -> Confirmar Presença (enviar notificação) de 60 em 60 minutos, caso a presença não seja confirmada o tempo de foco é pausado
- [ ] Bug nos dias (365)
    - [ ] Domingo (Não cria uma nova week)
    - [x] Segunda e Terça (o layout quebra, não elimina a primeira semana na esquerda)


- [ ] Dockerizar
- [ ] Testes Unitários (Failure and Success)




# To do:

- [ ] Delete e Edit Task
- [ ] Edit To Do
- [ ] Edit, Delete User


- [x] Deixar o toast mais bonito
- [x] last 365 days
- [ ] ToDo para cada task
    - [x] BackEnd: Create
    - [x] Validação do nome do status
    - [x] FrontEnd: Apresentação das tasks
    - [x] Delete
    - [x] Info: Created Time and Completed Time
    - [ ] To Do List Filtros (por data de criação/finalização)
    - [ ] Prioridade
- [x] BUG: Ao criar nova task, tem que criar o gráfico tambem. (Atualizar no arquivo js)
- [x] Abstrair mais o codigo (templates, js, partials, mais classes, rotas)
- [x] Refatorar pesado aqui (+segurança, melhorar a manipulação dos dados (dicionário x instâncias), melhorar os models.)
- [x] Melhorar DB Tabelas (Task, ToDo)
- [x] ToDo Blueprint
- [x] Classe exeption
- [x] logging
- [x] Tratamento de Erros (Back-End)
- [ ] configurar logging do flask: https://flask.palletsprojects.com/en/stable/logging/
- [x] Estudar e Melhorar os blueprints
- [x] REFATORAR TUDO, TENDO EM VISTA A REFATORACAO DE DATA_RECORD 
- [x] SEPARAR CONTROLLER E ROUTES (ta tudo junto hoje em dia)
- [x] Salvar o seconds_in_focus_per_day a todo segundo, e não somente quando o usuário clicar em stop. (para salvar o tempo msm se o usuário sair dar tela, fechar a tela, perder conexão com internet.)
- [x] Gráfico do git hub
- [x] Separar melhor as pastas dos arquivos 
- [ ] Factory + Injeção de Dependências

Pensar no cenário onde o timer foi iniciado antes da 00:00 e continuou até após 00:00

- [x] Salvar o tempo em segundos no banco...
- [ ] salvar em banco de dados inves de arquivo
- [ ] my perfomance
- [ ] edit e delete


Aprender:

- [ ] Docker
- [ ] Git


