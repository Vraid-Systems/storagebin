from __future__ import with_statement
from google.appengine.api import files
from google.appengine.api.images import get_serving_url
from google.appengine.ext.blobstore import delete as blobstore_delete, BlobReader, MAX_BLOB_FETCH_SIZE

MAX_SIZE_IN_BYTES = MAX_BLOB_FETCH_SIZE - 1 #1015807 bytes ~ 0.969MB

def delete(blob_keys):
    if blob_keys:
        blobstore_delete(blob_keys)

def get_image_url(blob_key):
    return get_serving_url(blob_key)

def get(blob_key):
    return BlobReader(blob_key).read()

def put(uploaded_file, existing_blob_key):
    # clear existing data
    delete(existing_blob_key)
    
    # write new data
    file_name = files.blobstore.create(uploaded_file.content_type)
    with files.open(file_name, 'a') as f:
        f.write(uploaded_file.read())
    files.finalize(file_name)
    
    # return the blob_key associated with the new data
    blob_key = files.blobstore.get_blob_key(file_name)
    return blob_key
