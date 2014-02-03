from datetime import datetime, timedelta

from storagebin import const, getHttpResponse
from storagebin.internal.blobstore import delete as delete_wrapper
from storagebin.models import Binary

def cron(request): #called by cron.yaml through django
    no_old_data_resp = getHttpResponse(content='no old data found',
                                       content_type=const.CONTENT_TYPE_TEXT)
    
    db_Binary_objs = _older_than_90_days()
    if db_Binary_objs is None:
        return no_old_data_resp
    
    # ALWAYS run blob deletion before killing datastore lookup objects
    _delete_old_Blobs(db_Binary_objs)
    delete_count = _delete_old_Binary_objs(db_Binary_objs)
    if delete_count is None:
        return no_old_data_resp
    
    return getHttpResponse(content=str(delete_count) + " records deleted",
                           content_type=const.CONTENT_TYPE_TEXT)

def _older_than_90_days():
    earlier_by_90_days = datetime.utcnow() - timedelta(days = 90)
    return Binary.objects.exclude(last_access__isnull=True).filter(last_access__lte=earlier_by_90_days)

def _delete_old_Binary_objs(db_Binary_objs):
    if db_Binary_objs is None:
        return None
    
    delete_count = len(db_Binary_objs)
    db_Binary_objs.delete()
    
    return delete_count

def _delete_old_Blobs(db_Binary_objs):
    if db_Binary_objs is None:
        return
    
    blob_keys = list()
    for db_Binary_obj in db_Binary_objs:
        if db_Binary_obj.content_key:
            blob_keys.append(db_Binary_obj.content_key)
    delete_wrapper(blob_keys)
