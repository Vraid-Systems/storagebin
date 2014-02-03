from datetime import datetime, timedelta

from django.test import TestCase

from storagebin.internal import prune
from storagebin.models import Binary, BinOwner

class PruneTestSuite(TestCase):
    def setUp(self):
        self.binowner = BinOwner(email='example@example.com', key='example')
        self.binowner.save()
    
    def test_old_and_delete_bin(self):
        earlier_by_89_days = datetime.utcnow() - timedelta(days = 89)
        binary_1 = Binary(owner=self.binowner,
                          content_key="",
                          content_type="text/plain/1",
                          last_access=earlier_by_89_days)
        binary_1.save()
        
        binary_1_5 = Binary(owner=self.binowner,
                          content_key="",
                          content_type="text/plain/1.5")
        binary_1_5.save()
        
        earlier_by_91_days = datetime.utcnow() - timedelta(days = 91)
        binary_2 = Binary(owner=self.binowner,
                          content_key="",
                          content_type="text/plain/2",
                          last_access=earlier_by_91_days)
        binary_2.save()
        
        self.assertEqual(Binary.objects.count(), 3)
        
        old_data = prune._older_than_90_days()
        self.assertEqual(len(old_data), 1)
        self.assertEqual(old_data[0].content_type, "text/plain/2")
        
        prune._delete_old_Binary_objs(old_data)
        old_data_after = prune._older_than_90_days()
        self.assertEqual(len(old_data_after), 0)
