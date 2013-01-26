from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import requests

def index(request, template='index.html'):
    services = [
        'Facebook',
        'Twitter',
        'LinkedIn',


    ]
    if request.user.is_authenticated():
        user_profile = request.user.get_profile()

        profiles = user_profile.profiles
    response = render_to_response(
            template, locals(), context_instance=RequestContext(request)
        )
    return response

@login_required()
def query(request, template='query.html'):
    try:
        q = request.GET['q']
        user_profile = request.user.get_profile()
        r = requests.get('https://api.singly.com/friends/all?limit=10&q='+q+'&access_token='+user_profile.access_token)
        r = r.json()
        response = render_to_response(
            template, locals(), context_instance=RequestContext(request)
        )
        return response
    except KeyError:
        return render(request,'search.html')

def json_response(func):
    """
    A decorator thats takes a view response and turns it
    into json. If a callback is added through GET or POST
    the response is JSONP.
    """
    def decorator(request, *args, **kwargs):
        objects = func(request, *args, **kwargs)
        if isinstance(objects, HttpResponse):
            return objects
        try:
            data = simplejson.dumps(objects)
            if 'callback' in request.REQUEST:
                # a jsonp response!
                data = '%s(%s);' % (request.REQUEST['callback'], data)
                return HttpResponse(data, "text/javascript")
        except:
            data = simplejson.dumps(str(objects))
        return HttpResponse(data, "application/json")
    return decorator


@json_response
def manifest(request):
    return {
        "name": "Friends",
        "description": "Search your friends throughout your social networks. We do not store or cache your data.",
        "launch_path": "/",
        "icons": {
            "128": "glyphicons-halflings.png"
        },
        "developer": {
            "name": "83tb",
            "url": "http://twitter.com/83tb"
        },
        "default_locale": "en"
    }