from django.http import HttpRequest
from django.test import TestCase

import json

from taskifier import const
from taskifier import taskrouter
from taskifier.models import TaskOwner

class FullRunTestSuite(TestCase):
    def setUp(self):
        self.taskowner = TaskOwner(email='example@example.com', key='example')
        self.taskowner.save()
    
    def test_POST(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST = {const.KEY_ID: "",
                        const.KEY_SOURCE: "a@domain.com",
                        const.KEY_DEST: "b@domain.com",
                        const.KEY_CONTENT: "text content",
                        const.KEY_READY_TIME: "2013-09-13T04:22:58.578Z"}
        response = taskrouter(request=request,
                              owner_key=self.taskowner.key,
                              task_id=None)
        
        response_body = response.content
        self.assertTrue(response_body)
        
        json_body = json.loads(response_body)
        self.assertTrue(json_body)
        
        self.assertEqual(json_body[const.KEY_SOURCE], request.POST[const.KEY_SOURCE])
        self.assertEqual(json_body[const.KEY_DEST], request.POST[const.KEY_DEST])
        self.assertEqual(json_body[const.KEY_CONTENT], request.POST[const.KEY_CONTENT])
        self.assertEqual(json_body[const.KEY_READY_TIME], request.POST[const.KEY_READY_TIME])
    
    def test_POST_then_GET(self):
        request_POST = HttpRequest()
        request_POST.method = 'POST'
        request_POST.POST = {const.KEY_ID: "",
                             const.KEY_SOURCE: "a@domain.com",
                             const.KEY_DEST: "b@domain.com",
                             const.KEY_CONTENT: "text content",
                             const.KEY_READY_TIME: "2000-09-13T04:22:58.100Z"}
        response_POST = taskrouter(request=request_POST,
                                   owner_key=self.taskowner.key,
                                   task_id=None)
        json_POST = json.loads(response_POST.content)
        task_id = json_POST[const.KEY_ID]
        
        request_GET = HttpRequest()
        request_GET.method = 'GET'
        response_GET = taskrouter(request=request_GET,
                                  owner_key=self.taskowner.key,
                                  task_id=task_id)
        json_GET = json.loads(response_GET.content)
        
        self.assertEqual(json_GET[const.KEY_ID], task_id)
        self.assertEqual(json_GET[const.KEY_SOURCE], request_POST.POST[const.KEY_SOURCE])
        self.assertEqual(json_GET[const.KEY_DEST], request_POST.POST[const.KEY_DEST])
        self.assertEqual(json_GET[const.KEY_CONTENT], request_POST.POST[const.KEY_CONTENT])
        self.assertEqual(json_GET[const.KEY_READY_TIME], request_POST.POST[const.KEY_READY_TIME])
    
    def test_POST_then_DELETE(self):
        request_POST = HttpRequest()
        request_POST.method = 'POST'
        request_POST.POST = {const.KEY_ID: "",
                             const.KEY_SOURCE: "a@domain.com",
                             const.KEY_DEST: "b@domain.com",
                             const.KEY_CONTENT: "text content",
                             const.KEY_READY_TIME: "2013-09-13T04:22:58.578Z"}
        response_POST = taskrouter(request=request_POST,
                                   owner_key=self.taskowner.key,
                                   task_id=None)
        json_POST = json.loads(response_POST.content)
        task_id = json_POST[const.KEY_ID]
        
        request_DELETE = HttpRequest()
        request_DELETE.method = 'DELETE'
        response_DELETE = taskrouter(request=request_DELETE,
                                     owner_key=self.taskowner.key,
                                     task_id=task_id)
        json_DELETE = json.loads(response_DELETE.content)
        self.assertEqual(json_DELETE[const.KEY_ID], task_id)
