from django.test import TestCase
from tasks_app.models import Task


class TasksTestCase(TestCase):

    def test_tasks_can_be_stored(self):
        new_task_id = Task.create_new_task({
            "publish_date": '1999-12-02', 
            "content": 'Cita a las 12'
        })
        self.assertTrue(Task.objects.get(id=new_task_id) is not None)


    def test_tasks_can_be_completed(self):
        new_task_id = Task.create_new_task({
            "publish_date": '1999-12-02', 
            "content": 'Cita a las 12'
        })
        self.assertFalse(Task.objects.get(id=new_task_id).completed)
        Task.complete_task(new_task_id)
        self.assertTrue(Task.objects.get(id=new_task_id).completed)


    def test_tasks_can_be_deleted(self):
        new_task_id = Task.create_new_task({
            "publish_date": '1999-12-02', 
            "content": 'Cita a las 12'
        })
        self.assertTrue(Task.objects.get(id=new_task_id) is not None)

        Task.delete_task(new_task_id)

        with self.assertRaises(Task.DoesNotExist) as context: Task.objects.get(id=new_task_id)
        self.assertTrue('does not exist' in str(context.exception))


    def test_tasks_can_be_filtered(self):
        Task.create_new_task({
            "publish_date": '1999-12-02', 
            "content": 'Cita a las 12'
        })
        Task.create_new_task({
            "publish_date": '1998-11-15', 
            "content": 'Cita a las 14'
        })
        Task.create_new_task({
            "publish_date": '2021-04-03', 
            "content": 'Cita a las 15'
        })

        # Check only content filter
        all_tasks = Task.get_all_tasks_with_filters({
            "publish_date": '',
            "content": 'Cita a las 12'
        })
        self.assertTrue('Cita a las 12' in [task['fields']['content'] for task in all_tasks])

        # Check only date filter
        all_tasks = Task.get_all_tasks_with_filters({
            "publish_date": '1998-11-15',
            "content": ''
        })
        self.assertTrue('1998-11-15' in [task['fields']['publish_date'] for task in all_tasks])

        # Check both filters
        all_tasks = Task.get_all_tasks_with_filters({
            "publish_date": '1999-12-02',
            "content": 'Cita a las 12'
        })
        self.assertTrue(
            'Cita a las 12' in [task['fields']['content'] for task in all_tasks] and 
            '1999-12-02' in [task['fields']['publish_date'] for task in all_tasks]
        )
