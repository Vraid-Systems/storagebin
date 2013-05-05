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
    
    content_type = uploaded_file.content_type
    if is_image(content_type):
        blob_key = put_data(data_id, content_type)
        if blob_key is None:
            return {const.RESP_KEY_CONTENT: 'POST: ' + data_id,
                    const.RESP_KEY_MIME: 'text/html',
                    const.RESP_KEY_STATUS: 502}
        
        if data_id is None:
            binary = Binary(owner=bin_owner, content_key=blob_key,
                   content_type=content_type)
            binary.save()
        else:
            binary = Binary.objects.get(data_id=data_id)
            binary.content_key = blob_key
            binary.save()
        
        return {const.RESP_KEY_CONTENT: 'POST: ' + data_id,
                const.RESP_KEY_MIME: 'text/html',
                const.RESP_KEY_STATUS: 200}
    else:
        return {const.RESP_KEY_CONTENT: ERROR + 'unsupported Content-Type ' + content_type,
                const.RESP_KEY_MIME: 'text/html',
                const.RESP_KEY_STATUS: 400}

def get_owner(owner_key):
    return BinOwner.objects.filter(key=owner_key)

def _is_owner(bin_owner, binary):
    if bin_owner and binary:
        return (bin_owner.key == binary.owner.key)
    else:
        return False
