import const
from django.http import HttpResponse, HttpResponseRedirect
from storagebin.api import DELETE, GET, POST, get_owner
from storagebin.models import BinOwner

ERROR = "ERROR: "

def binrouter(request, owner_key = None, data_id = None):
    """route data request to the correct handler and return HTTP response
    
    Args:
        request: the HttpRequest object
        owner_key: string finger print of the user
        data_id: a numeric identifier for Binary object
    
    Returns:
        HttpResponse or HttpResponseRedirect
    """
    response = {const.RESP_KEY_CONTENT: 'NOOP',
                const.RESP_KEY_MIME: 'text/html',
                const.RESP_KEY_STATUS: 200}
    
    bin_owner = None
    if owner_key:
        bin_owner = get_owner(owner_key)
    
    if request.method == 'OPTIONS':
        response[const.RESP_KEY_CONTENT] = ''
    elif request.method == 'GET':
        response = GET(data_id)
    elif bin_owner and isinstance(bin_owner, BinOwner):
        if request.method == 'DELETE':
            response = DELETE(bin_owner, data_id)
        elif request.method == 'POST':
            if request.FILES and len(request.FILES) == 1:
                response = POST(bin_owner=bin_owner,
                                data_id=data_id,
                                uploaded_file=request.FILES['file'])
    else:
        response[const.RESP_KEY_CONTENT] = ERROR + 'invalid owner_key'
        response[const.RESP_KEY_STATUS] = 403

    if response[const.RESP_KEY_STATUS] == 302:
        r_content = response[const.RESP_KEY_CONTENT]
        return HttpResponseRedirect(r_content)
    else:
        aHttpResponse = HttpResponse(content=response[const.RESP_KEY_CONTENT],
                            mimetype=response[const.RESP_KEY_MIME],
                            status=response[const.RESP_KEY_STATUS])
        return addCORSHeaders(aHttpResponse)

def addCORSHeaders(theHttpResponse):
    if theHttpResponse and isinstance(theHttpResponse, HttpResponse):
        theHttpResponse['Access-Control-Allow-Origin'] = '*'
        theHttpResponse['Access-Control-Max-Age'] = '120'
        theHttpResponse['Access-Control-Allow-Credentials'] = 'true'
        theHttpResponse['Access-Control-Allow-Methods'] = 'HEAD, GET, OPTIONS, POST, DELETE'
        theHttpResponse['Access-Control-Allow-Headers'] = 'origin, content-type, accept, x-requested-with'
    return theHttpResponse
