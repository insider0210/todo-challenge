import json, logging
from django.db import models
from django.core import serializers
from django.db.models import Q
from datetime import datetime

logger = logging.getLogger(__name__)


class Task(models.Model):
    """
        publish_date (date) : Fecha de creacion de la tarea
        content (str)       : Contenido de la tarea
        completed (boolean) : Estado de la tarea, si fue completada o no
        deleted (boolean)   : Estado de eliminacion de la tarea dentro de la bbdd (baja logica)
    """
    publish_date = models.DateField('date published')
    content = models.CharField(max_length=50)
    completed = models.BooleanField()
    deleted = models.BooleanField()


    def get_all_tasks_with_filters(filters_dic : dict) -> list:
        """
            Filtra las tareas que cumpla con los parametro del diccionario
            El diccionario esta pensado para que tenga el siguiente formato:\n
            {
                publish_date: '1999-12-02', 
                content: 'Cita a las 12'
            }
        """
        all_models = Task.objects.filter(~Q(deleted__contains="1"))
        lambda_tasks_functions = [
            (lambda querySetObject : querySetObject.filter(content__contains=filters_dic['content'])) if filters_dic['content'] != '' else None,
            (lambda querySetObject : querySetObject.filter(publish_date=filters_dic['publish_date'])) if filters_dic['publish_date'] != '' else None
        ]

        for filter in lambda_tasks_functions: all_models = filter(all_models) if filter is not None else all_models
        all_models = serializers.serialize('json', all_models, fields=('pk','publish_date','content','completed'))
        all_models = json.loads(all_models)
        return all_models
    

    def create_new_task(json_task : dict) -> int or None:
        """
            Creacion de una nueva tarea en base al diccionario con el siguiente formato:\n
            {
                publish_date: '1999-12-02', 
                content: 'Cita a las 12'
            }
        """
        try:
            date_from_task = datetime.strptime(json_task['publish_date'], '%Y-%m-%d').date()
            content_from_task = json_task['content']
            new_task = Task(publish_date=date_from_task,content=content_from_task,completed=False,deleted=False)
            new_task.save()
        except(OSError) as e:
            logger.error(f'Ocurrio el siguiente error al crear la tarea: {e}')
            return None
        else:
            return new_task.id


    def delete_task(task_id : int):
        """
            Se elimina la tarea en base al id.\n
            En este caso se hace coincidir con la PK de la tabla PERO podria ser indexado con otra key el eliminado
        """
        task_to_delete = Task.objects.get(id=task_id)
        task_to_delete.delete()


    def complete_task(task_id : int):
        """
            Marca la tarea como completada
        """
        task_to_modify = Task.objects.get(id=task_id)
        task_to_modify.completed = True
        task_to_modify.save()
