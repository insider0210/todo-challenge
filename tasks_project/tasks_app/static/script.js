const elementDivTasksTable = document.getElementById('div-tasks-table');

const getDataFromUrl = async (url) => {
    let response = await fetch(url);
    let dataJson = await response.json();
    return dataJson;
}

const sendDataToUrl = async (url, data, httpVerb) => {
    let response = await fetch(url, {
        method: httpVerb,
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          },
        body: JSON.stringify(data)
    });
    let dataJson = response.json();
    return dataJson;
}


function loadColumnTask (trColumn,contentColumn) {
    let columnTd = document.createElement('td');
    columnTd.classList.add('tasks-register');
    columnTd.innerHTML = contentColumn;
    trColumn.appendChild(columnTd);
}

async function deleteTask(element) {
    let tableTbody = document.getElementById('tasks-table');
    let idRegisterToDelete = element.target.parentElement.id;
    let registerToDelete  = document.getElementById(idRegisterToDelete);
    tableTbody.removeChild(registerToDelete);
    body = {
        id : idRegisterToDelete
    };
    const response = await sendDataToUrl('tareas/',body,'DELETE');
    if(response['taskDeleteStatus'] == 'SUCCESS') {
        console.log(`Se elimino la tarea de id "${idRegisterToDelete}" correctamente`);
    } else {
        console.war(`No se pudo eliminar la tarea de id "${idRegisterToDelete}"`);
    }
}

async function completeTask(element) {
    let idRegisterToDelete = element.target.parentElement.id;
    body = {
        id : idRegisterToDelete
    };
    const response = await sendDataToUrl('tareas/',body,'PUT');
    if(response['taskUpdateStatus'] == 'SUCCESS') {
        console.log(`Se completo la tarea de id "${idRegisterToDelete}" correctamente`);
    } else {
        console.war(`No se pudo completar la tarea de id "${idRegisterToDelete}"`);
    }
}

function loadTasksOnTable(response) {
    let tasks_list = response['tasksFinded']
    const tableTbody = document.getElementById('tasks-table');
    
    tasks_list.forEach(element => {
        let fieldsTask = element['fields'];

        let trTable = document.createElement('tr');
        trTable.setAttribute('id',element['pk'])

        let deleteColumn = document.createElement('td');
        deleteColumn.classList.add('action-on-task');
        deleteColumn.innerHTML = '❌';
        deleteColumn.addEventListener('click', deleteTask);
        trTable.appendChild(deleteColumn);

        loadColumnTask(trTable,`${element['pk']}°`);
        loadColumnTask(trTable,`${fieldsTask['completed'] ? 'COMPLETADA' : 'SIN COMPLETAR'}`);
        loadColumnTask(trTable,`${fieldsTask['publish_date']}`);
        loadColumnTask(trTable,`${fieldsTask['content']}`);

        let completeColumn = document.createElement('td');
        completeColumn.classList.add('action-on-task')
        completeColumn.innerHTML = '✔️';
        completeColumn.addEventListener('click', completeTask);
        trTable.appendChild(completeColumn);
        
        tableTbody.appendChild(trTable)
    });

}

async function getTasksWithFilters() {
    const elementTaskDateInput = document.getElementById('task-date');
    const elementTaskContentInput = document.getElementById('task-content');
    
    let taskDate = elementTaskDateInput.value
    let taskContent = elementTaskContentInput.value

    if((taskContent || taskDate) === '' ) {
        console.log('Se traen todas las tareas');
    } else {
        console.log('Obtengo las tareas con los filtros seleccionados');
    }

    let urlToSend = `tareas/?content=${taskContent}&publish_date=${taskDate}`
    var response = await getDataFromUrl(urlToSend);
    
    console.log(response);
    clearSelection();
    if(response['searchTasksStatus'] == 'SUCCESS') {
        loadTasksOnTable(response);
    } else {
        log.war('Ocurrio un error al traer los datos de las tareas');
    }
    elementDivTasksTable.classList.remove('d-none');
}

async function createTask() {
    let elementTaskContentInput = document.getElementById('input-task-content');
    let elementTaskDateInput = document.getElementById('input-task-creation-date');

    body = {
        publish_date : elementTaskDateInput.value,
        content : elementTaskContentInput.value 
    };

    const response = await sendDataToUrl('tareas/',body,'POST');
    console.log(response);

    elementTaskDateInput.value = '';
    elementTaskContentInput.value = '';

    console.log(response['createTaskStatus']);
    if(response['createTaskStatus'] == 'FAIL') {
        console.war("No se creo la tarea correctamente");
    }

    else if(response['createTaskStatus'] == 'SUCCESS') {
        console.log("Se creo la tarea correctamente");
    }

}

function clearSelection() {
    console.log('Se limpia la tabla de contenido de las tareas');
    let newTbody = document.createElement('tbody');
    newTbody.setAttribute('id','tasks-table');
    document.getElementById('tasks-table').parentNode.replaceChild(newTbody,document.getElementById('tasks-table'));
    elementDivTasksTable.classList.add('d-none');
}