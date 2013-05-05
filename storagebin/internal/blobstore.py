from __future__ import with_statement
from google.appengine.api import files
from google.appengine.api.images import get_serving_url

MAX_SIZE_IN_BYTES = 31457280

def get_data_url(blob_key):
    return get_serving_url(blob_key)

def put_data(data_id, uploaded_file):
    file_name = files.blobstore.create(uploaded_file.content_type, data_id)
    
    with files.open(file_name, 'w') as f:
        f.write(uploaded_file.read())
    
    files.finalize(file_name)
    
    blob_key = files.blobstore.get_blob_key(file_name)
    
    return blob_key
