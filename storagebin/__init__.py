from django.http import HttpResponse, HttpResponseRedirect
from storagebin import const
from storagebin.api import DELETE, GET, POST, get_owner
from storagebin.models import BinOwner

def binrouter(request, owner_key = None, data_id = None):
    """route data request to correct handler and return HttpResponse
    
    Args:
        request: the HttpRequest object
        owner_key: string finger print of the user
        data_id: a numeric identifier for the Binary object
    
    Returns:
        HttpResponse or HttpResponseRedirect
    """
    # no app data is exchanged for OPTIONS
    if request.method == 'OPTIONS':
        return getHttpResponse()
    
    # no permissions are enforced for GET
    if request.method == 'GET':
        return getHttpResponse(GET(data_id))
    
    # hydrate bin_owner for all other request.method types
    bin_owner = None
    if owner_key:
        bin_owner = get_owner(owner_key)
    if bin_owner is None or not isinstance(bin_owner, BinOwner):
        return getHttpResponse(const.PREFIX_ERROR + 'invalid owner_key', const.CONTENT_TYPE_HTML, const.HTTP_STATUS_403)
    
    # only owners can delete their data objects
    if request.method == 'DELETE':
        return getHttpResponse(DELETE(bin_owner, data_id))
    
    # only authed users can store data on this system
    if request.method == 'POST':
        if request.FILES and len(request.FILES) == 1:
            return getHttpResponse(bin_owner, data_id, request.FILES['file'])
    
    # default NOOP response
    return getHttpResponse()

def addCORSHeaders(http_response):
    if http_response and isinstance(http_response, HttpResponse):
        http_response['Access-Control-Allow-Origin'] = '*'
        http_response['Access-Control-Max-Age'] = '120'
        http_response['Access-Control-Allow-Credentials'] = 'true'
        http_response['Access-Control-Allow-Methods'] = 'OPTIONS, GET, POST, DELETE'
        http_response['Access-Control-Allow-Headers'] = 'origin, content-type, accept, x-requested-with'
    return http_response

def getHttpResponse(content='', content_type=const.CONTENT_TYPE_HTML, status=const.HTTP_STATUS_200):
    if status == const.HTTP_STATUS_302:
        http_response = HttpResponseRedirect(content)
    else:
        http_response = HttpResponse(content, content, content_type=content_type, status=status)
    return addCORSHeaders(http_response)
