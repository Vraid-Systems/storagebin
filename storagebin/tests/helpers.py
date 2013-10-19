from datetime import datetime

from django.test import TestCase

from taskifier import const
from taskifier.models import Task, TaskOwner
from taskifier.internal.TaskPayloadHelper import TaskPayloadHelper
from taskifier.internal.WorkerHelper import WorkerHelper

TEST_DATE = "2013-09-13T04:22:58.578Z" #ISO-8601 (UTC)
TEST_DATE_EXPECT = datetime(2013, 9, 13, 4, 22, 58, 578000)

TEST_EMAIL_CASES = ["user@domain.com", "@user@domain.com", "@cool_dude_ty", "user@domain.sub.com", "user@domain.com@.com"]
TEST_EMAIL_EXPECTS = [True, False, False, True, False]

TEST_TWITTER_CASES = ["user@domain.com", "@cool_dude_ty", "@cool-dude-ty", "@monkey.freud", "@___"]
TEST_TWITTER_EXPECTS = [False, True, False, False, True]

TEST_PAYLOAD = {const.KEY_SOURCE: "a@domain.com",
                const.KEY_DEST: "b@domain.com",
                const.KEY_CONTENT: "this is some text",
                const.KEY_READY_TIME: TEST_DATE}

class TaskPayloadHelperTestSuite(TestCase):
    def setUp(self):
        self.taskPayloadHelper = TaskPayloadHelper(TEST_PAYLOAD)
        
        self.owner = TaskOwner(email='example@example.com', key='example')
        self.owner.save()
    
    def test_get_ready_datetime(self):
        self.assertEqual(self.taskPayloadHelper.get_ready_datetime(),
                         TEST_DATE_EXPECT)
    
    def test_is_duplicate(self):
        self.assertFalse(self.taskPayloadHelper.is_duplicate())
        
        task = Task(owner=self.owner,
                    source=TEST_PAYLOAD[const.KEY_SOURCE],
                    dest=TEST_PAYLOAD[const.KEY_DEST],
                    content=TEST_PAYLOAD[const.KEY_CONTENT],
                    ready_time=TEST_DATE_EXPECT)
        task.save()
        
        self.assertTrue(self.taskPayloadHelper.is_duplicate())
    
    def test_is_valid(self):
        self.assertTrue(self.taskPayloadHelper.is_valid())

class WorkerHelperTestSuite(TestCase):
    def setUp(self):
        self.workerHelper = WorkerHelper()
    
    def _array_test_helper(self, function, cases, expects):
        i = 0
        for case in cases:
            self.assertEqual(function(case), expects[i])
            i += 1
    
    def test_email_simple_validate(self):
        """a most basic email format check"""
        self._array_test_helper(self.workerHelper.isEmail, TEST_EMAIL_CASES, TEST_EMAIL_EXPECTS)

    def test_twitter_handle(self):
        """various Twitter handles are correctly identified"""
        self._array_test_helper(self.workerHelper.isTwitterHandle, TEST_TWITTER_CASES, TEST_TWITTER_EXPECTS)
