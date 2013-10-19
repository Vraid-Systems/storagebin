from datetime import datetime, timedelta

from django.test import TestCase

from taskifier.internal import pushQueue
from taskifier.models import Task, TaskOwner

class QueueTestSuite(TestCase):
    def setUp(self):
        self.taskowner = TaskOwner(email='example@example.com', key='example')
        self.taskowner.save()
    
    def test_ready_and_delete_tasks(self):
        task_1 = Task(owner=self.taskowner,
                    source="@handle_a",
                    dest="@handle_b",
                    content="some message",
                    ready_time=datetime.utcnow() + timedelta(minutes = 10))
        task_1.save()
        
        task_2 = Task(owner=self.taskowner,
                    source="a@domain.com",
                    dest="b@domain.com",
                    content="some message",
                    ready_time=datetime.utcnow())
        task_2.save()
        
        ready_tasks = pushQueue._get_ready_tasks()
        self.assertEqual(len(ready_tasks), 1)
        self.assertEqual(ready_tasks[0].source, "a@domain.com")
        
        pushQueue._delete_processed_tasks(ready_tasks)
        ready_tasks_after = pushQueue._get_ready_tasks()
        self.assertEqual(len(ready_tasks_after), 0)
    
    def test_queue_task_creation(self):
        task_1 = Task(owner=self.taskowner,
                    source="@handle_a",
                    dest="@handle_b",
                    content="some message",
                    ready_time=datetime.now())
        task_1.save()
        
        ready_tasks = pushQueue._get_ready_tasks()
        
        queue_Task = pushQueue._create_task_from_db(ready_tasks[0])
        self.assertTrue(queue_Task)
