from storagebin.internal import DELETE as int_DELETE
from storagebin.internal import GET as int_GET
from storagebin.internal import POST as int_POST
from storagebin.internal import get_owner as int_get_owner

def DELETE(bin_owner, data_id):
    """Delete a binary object from the datastore
    
    Args:
        bin_owner: the owner Model
        data_id: a numeric identifier for Binary object
    
    Returns:
        A dictionary for creating a HTTP response. Example:
        {RESP_KEY_CONTENT: 'DELETE: [data_id]',
         RESP_KEY_MIME: 'text/html',
         RESP_KEY_STATUS: 200}
    """
    return int_DELETE(bin_owner, data_id)

def GET(data_id):
    """Get a binary object from the datastore
    
    Args:
        data_id: a numeric identifier for Binary object
    
    Returns:
        A dictionary for creating a HTTP response. Example:
        {RESP_KEY_CONTENT: [content URI],
         RESP_KEY_MIME: 'text/html',
         RESP_KEY_STATUS: 302}
    """
    return int_GET(data_id)

def POST(bin_owner, data_id, uploaded_file):
    """Add/update a binary object to/in the datastore
    
    Args:
        bin_owner: the owner Model
        data_id: a numeric identifier for Binary object
        uploaded_file: an instance of django.http.UploadedFile
    
    Returns:
        A dictionary for creating a HTTP response. Example:
        {RESP_KEY_CONTENT: 'OK',
         RESP_KEY_MIME: 'text/html',
         RESP_KEY_STATUS: 200}
    """
    return int_POST(bin_owner, data_id, uploaded_file)

def get_owner(owner_key):
    """Retrieve the BinOwner object via the owner_key
    
    Args:
        owner_key: string finger print of the user
    
    Returns:
        BinOwner
    """
    return int_get_owner(owner_key)
