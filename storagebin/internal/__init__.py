from datetime import datetime

from storagebin import const
from storagebin.internal.blobstore import get_image_url, get, put
from storagebin.internal.blobstore import MAX_SIZE_IN_BYTES
from storagebin.internal.util import is_image
from storagebin.models import Binary, BinOwner

def DELETE(bin_owner, data_id):
    binary = _get_binary(data_id)
    
    if binary and _is_owner(bin_owner, binary):
        binary.delete()
        
        return const.PREFIX_DELETE + 'data_id=' + str(data_id), const.CONTENT_TYPE_HTML, const.HTTP_STATUS_200
    else:
        return _error_404_message(data_id), const.CONTENT_TYPE_HTML, const.HTTP_STATUS_404

def GET(data_id):
    binary = _get_binary(data_id)
    
    if binary:
        content_key = binary.content_key
        content_type = binary.content_type
        
        binary.last_access = datetime.utcnow()
        binary.save()
        
        if is_image(content_type):
            return get_image_url(content_key), content_type, const.HTTP_STATUS_302
        else:
            return get(content_key), content_type, const.HTTP_STATUS_200
    else:
        return _error_404_message(data_id), const.CONTENT_TYPE_HTML, const.HTTP_STATUS_404
    
def POST(bin_owner, data_id, uploaded_file):
    if uploaded_file.size > MAX_SIZE_IN_BYTES:
        return const.PREFIX_ERROR + uploaded_file.name + ' is too large', const.CONTENT_TYPE_HTML, const.HTTP_STATUS_400
    
    blob_key = None
    if data_id:
        binary = _get_binary(data_id)
        blob_key = binary.content_key
    
    blob_key = put(uploaded_file, blob_key)
    if blob_key is None:
        return const.PREFIX_POST + 'blob_key=' + blob_key, const.CONTENT_TYPE_HTML, const.HTTP_STATUS_502
    
    if data_id is None:
        binary = Binary(owner=bin_owner, content_key=blob_key,
               content_type=uploaded_file.content_type)
        binary.save()
        data_id = binary.id
    else:
        binary = _get_binary(data_id)
        binary.content_key = blob_key
        binary.save()
    
    return const.PREFIX_POST + 'data_id=' + str(data_id), const.CONTENT_TYPE_HTML, const.HTTP_STATUS_200

def _error_404_message(data_id):
    return const.PREFIX_ERROR + 'unable to find ' + str(data_id)

def get_owner(owner_key):
    query_set = BinOwner.objects.filter(key=owner_key)
    if query_set and (len(query_set) == 1):
        return query_set[0]
    else:
        return None

def _get_binary(data_id):
    from django.core.exceptions import ObjectDoesNotExist
    
    if data_id:
        binary = None
        try:
            binary = Binary.objects.get(id=data_id)
        except ObjectDoesNotExist:
            binary = None
        return binary
    else:
        return None

def _is_owner(bin_owner, binary):
    if binary and bin_owner and isinstance(binary, Binary) and isinstance(bin_owner, BinOwner):
        return (bin_owner.key == binary.owner.key)
    else:
        return False
