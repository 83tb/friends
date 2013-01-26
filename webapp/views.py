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