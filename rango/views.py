from django.shortcuts import render, render_to_response
from django.template import RequestContext

# Create your views here.
from django.http import HttpResponse

def index(request):
    context = RequestContext(request)
    context_dict = {'boldmessage': "I am the bold message"}
    return render_to_response('rango/index.html', context_dict, context)

def about(request):
    return HttpResponse("This is about page! <a href='/rango'>Go back</a>")

def contact(request):
    context = RequestContext(request)
    context_dict = {'title': "Contact me"}
    return render_to_response("rango/contact.html", context_dict, context)