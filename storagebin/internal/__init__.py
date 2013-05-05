from django.core.exceptions import ObjectDoesNotExist

from storagebin import const
from storagebin.internal.blobstore import get_image_url, get, put
from storagebin.internal.blobstore import MAX_SIZE_IN_BYTES
from storagebin.internal.util import is_image
from storagebin.models import Binary, BinOwner

ERROR = "ERROR: "

def DELETE(bin_owner, data_id):
    binary = _get_binary(data_id)
    if binary and _is_owner(bin_owner, binary):
        binary.delete()
        
        return {const.RESP_KEY_CONTENT: 'DELETE: data_id=' + str(data_id),
                const.RESP_KEY_MIME: 'text/html',
                const.RESP_KEY_STATUS: 200}
    else:
        return {const.RESP_KEY_CONTENT: ERROR + 'unable to find ' + str(data_id),
                const.RESP_KEY_MIME: 'text/html',
                const.RESP_KEY_STATUS: 404}

def GET(data_id):
    binary = _get_binary(data_id)
    
    if binary:
        content_key = binary.content_key
        content_type = binary.content_type
        if is_image(content_type):
            return {const.RESP_KEY_CONTENT: get_image_url(content_key),
                    const.RESP_KEY_MIME: content_type,
                    const.RESP_KEY_STATUS: 302}
        else:
            return {const.RESP_KEY_CONTENT: get(content_key),
                    const.RESP_KEY_MIME: content_type,
                    const.RESP_KEY_STATUS: 200}
    else:
        return {const.RESP_KEY_CONTENT: ERROR + 'unable to find ' + str(data_id),
                const.RESP_KEY_MIME: 'text/html',
                const.RESP_KEY_STATUS: 404}
    
def POST(bin_owner, data_id, uploaded_file):
    if uploaded_file.size > MAX_SIZE_IN_BYTES:
        return {const.RESP_KEY_CONTENT: ERROR + uploaded_file.name + ' is too large',
                const.RESP_KEY_MIME: 'text/html',
                const.RESP_KEY_STATUS: 400}
    
    blob_key = None
    if data_id:
        binary = _get_binary(data_id)
        blob_key = binary.content_key
    
    blob_key = put(uploaded_file, blob_key)
    if blob_key is None:
        return {const.RESP_KEY_CONTENT: 'POST: blob_key=' + blob_key,
                const.RESP_KEY_MIME: 'text/html',
                const.RESP_KEY_STATUS: 502}
    
    if data_id is None:
        binary = Binary(owner=bin_owner, content_key=blob_key,
               content_type=uploaded_file.content_type)
        binary.save()
        data_id = binary.id
    else:
        binary = _get_binary(data_id)
        binary.content_key = blob_key
        binary.save()
    
    return {const.RESP_KEY_CONTENT: 'POST: data_id=' + str(data_id),
            const.RESP_KEY_MIME: 'text/html',
            const.RESP_KEY_STATUS: 200}

def get_owner(owner_key):
    query_set = BinOwner.objects.filter(key=owner_key)
    if query_set and (len(query_set) == 1):
        return query_set[0]
    else:
        return None

def _get_binary(data_id):
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
