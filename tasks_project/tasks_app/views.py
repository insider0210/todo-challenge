import logging, ast
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from tasks_app.models import Task


logger = logging.getLogger(__name__)


"""
    En cada respuesta HTTP se tiene los siguientes casos:
        En caso de ocurra un error se devuelve un status FAIL + un mensaje muy elemental del error
        En caso de que la creacion fue correcta, SUCCESS
"""


def index(request) -> HttpResponse:
    """
        HTTP GET para renderizar el template de home
    """
    logger.info('Se accedio al index de "tasks_app"')
    return render(request, 'index.html')


def tasks_actions(request):
    """
        Handler para verbos HTTP al recurso definido como "tareas/" en urls.py
    """
    if request.method == "GET":
        return get_tasks(request)
    elif request.method == "POST":
        return create_task(request)
    elif request.method == "PUT":
        return complete_task(request)
    elif request.method == "DELETE":
        return delete_task(request)
    else:
        return method_not_allowed_error()


def get_tasks(request) -> JsonResponse or HttpResponse:
    """
        HTTP GET para filtrar las tareas en base a los parametros recibidos
    """
    query_param = request.GET.dict()
    logger.info(f'Se solicito filtrar las tareas. Se leyeron los filtros : {query_param}')
    all_tasks = Task.get_all_tasks_with_filters(query_param)

    return JsonResponse({
        "searchTasksStatus" : "SUCCESS",
        "tasksFinded" : all_tasks
    })


def create_task(request) -> JsonResponse or HttpResponse:
    """
        HTTP POST para crear nuevas tareas
        Se debe recibir un JSON con el siguiente formato para crearla correctamente
        {
            "publish_date" : "25-04-1999",
            "content" : "Hacer la cama a las 20hs"
        }
    """
    json_task = ast.literal_eval(request.body.decode('utf-8')) 
    logger.info(f'Recibi estos datos para la creacion de una nueva tarea: {json_task}')

    new_task_id = Task.create_new_task(json_task)
    if new_task_id is None:
        logger.info('No se creo la tarea. Hubo un error en el servidor')
        return JsonResponse({
            "createTaskStatus" : "FAIL",
            "Reason" : "Verify the error on the server"
        })

    logger.info(f'Se creo la tarea de id "{new_task_id}" exitosamente')
    return JsonResponse({
        "createTaskStatus" : "SUCCESS"
    })


def delete_task(request) -> JsonResponse or HttpResponse:
    """
        HTTP DELETE para eliminar tareas de la bbdd
        Se debe recibir un JSON con el siguiente formato para eliminarla correctamente
        {
            "id" : "1"
        }
    """
    json_task = ast.literal_eval(request.body.decode('utf-8')) 
    logger.info(f'Recibi esta informacion para eliminar la tarea: {json_task}')

    task_id_to_delete = json_task['id']
    if not task_id_to_delete:
        return JsonResponse({
            "taskDeleteStatus" : "FAIL",
            "Reason" : "Missing arguments to delete task"
        })

    Task.delete_task(int(task_id_to_delete))
    logger.info('Se elimino la tarea de forma correcta')
    return JsonResponse({
        "taskDeleteStatus" : "SUCCESS"
    })


def complete_task(request) -> JsonResponse or HttpResponse:
    """
        HTTP PUT para actualizar los datos de las tareas
        Se debe recibir un JSON con las siguientes keys
        {
            "id" : "1"
        }
    """
    json_task = ast.literal_eval(request.body.decode('utf-8')) 
    logger.info(f'Recibi esta informacion para completar una tarea: {json_task}')

    task_id_to_complete = json_task['id']
    logger.info(f'Me llego la tarea de id "{task_id_to_complete}" para completar')

    if not task_id_to_complete:
        return JsonResponse({
            "taskUpdateStatus" : "FAIL",
            "Reason" : "Missing arguments to complete task"
        })
    
    Task.complete_task(int(task_id_to_complete))
    logger.info('Se completo la tarea de forma correcta')
    return JsonResponse({
        "taskUpdateStatus" : "SUCCESS"
    })


def method_not_allowed_error() -> None:
    """
        Error generico para verbo HTTP no aceptado
    """
    logger.error('¡Se trato de enviar un verbo HTTP no valido!')
    return HttpResponse('<h1>Method not allowed!</h1>')
