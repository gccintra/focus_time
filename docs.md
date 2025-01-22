Doing:
- [ ] ToDo para cada task
    - [x] BackEnd: Create

        Obs.:
        Os IDs dos To-Dos são únicos apenas dentro de cada Task. Isso significa que podem existir To-Dos com IDs iguais em Tasks diferentes. Para identificar um To-Do de forma precisa, sempre utilizamos a combinação Task/To-Do. Essa abordagem funciona porque a lista de To-Dos é uma composição da Task, garantindo o contexto necessário para localizar qualquer To-Do.

        Usar a combinação Task/To-Do para identificar os To-Dos oferece benefícios como:

        - Unicidade e Clareza: Evita conflitos de ID entre diferentes Tasks, mantendo a integridade dos dados.
        - Contextualização: Facilita a busca por To-Dos dentro de uma Task específica, garantindo precisão.
        - Escalabilidade: Permite o crescimento sem risco de colisões de ID, mesmo com várias Tasks e To-Dos.
        
    - [ ] Validação do nome do status
    - [x] FrontEnd: Apresentação das tasks
    - [x] Delete
    - [x] Info: Created Time and Completed Time
    - [ ] To Do List Filtros (por data de criação/finalização)
- [x] BUG: Ao criar nova task, tem que criar o gráfico tambem. (Atualizar no arquivo js)
- [ ] Abstrair mais o codigo (templates, js, partials, mais classes, rotas)
- [ ] Refatorar pesado aqui (+segurança, melhorar a manipulação dos dados (dicionário x instâncias), melhorar os models.)

To do:
- [ ] Getters e Setters, + Segurança
- [x] REFATORAR TUDO, TENDO EM VISTA A REFATORACAO DE DATA_RECORD 
- [ ] SEPARAR CONTROLLER E ROUTES (ta tudo junto hoje em dia)
- [ ] Salvar o seconds_in_focus_per_day a todo segundo, e não somente quando o usuário clicar em stop. (para salvar o tempo msm se o usuário sair dar tela, fechar a tela, perder conexão com internet.)
- [ ] Tratamento de Erros e apresentação para o usuário
- [ ] Validações de campo
- [ ] Gráfico do git hub
- [ ] Testes unitários  
- [ ] Separar melhor as pastas dos arquivos (por funcionalidade talvez)

Pensar no cenário onde o timer foi iniciado antes da 00:00 e continuou até após 00:00

- [x] Salvar o tempo em segundos no banco...
- [ ] salvar em banco de dados inves de arquivo
- [ ] my perfomance
- [ ] edit e delete




Aprender:

- [ ] Docker
- [ ] Git


