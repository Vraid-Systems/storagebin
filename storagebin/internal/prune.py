from datetime import datetime, timedelta

from storagebin import const, getHttpResponse
from storagebin.models import Binary

def cron(request): #called by cron.yaml through django
    no_old_data_resp = getHttpResponse(content='no old data found',
                                       content_type=const.CONTENT_TYPE_TEXT)
    
    db_Binary_objs = _older_than_90_days()
    if db_Binary_objs is None:
        return no_old_data_resp
    
    delete_count = _delete_old_Binary_objs(db_Binary_objs)
    if delete_count is None:
        return no_old_data_resp
    
    return getHttpResponse(content=delete_count + " records deleted",
                           content_type=const.CONTENT_TYPE_TEXT)

def _older_than_90_days():
    earlier_by_90_days = datetime.utcnow() - timedelta(days = 90)
    return Binary.objects.filter(last_access__lte=earlier_by_90_days)

def _delete_old_Binary_objs(db_Binary_objs):
    if db_Binary_objs is None:
        return None
    
    delete_count = len(db_Binary_objs)
    for db_Binary_obj in db_Binary_objs:
        db_Binary_obj.delete()
    
    return delete_count
