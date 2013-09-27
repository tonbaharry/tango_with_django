from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse

def index(request):
	# Request the context of the request.
	context = RequestContext(request)
	
	# Construct a dictionary to pass to the template engine as its context.
	context_dict = {'boldmessage': "I am from the context"}
	
	# Return a rendered response to send to the client.
	# Note that the first parameter is the path to te template we wish to use.
	return render_to_response('rango/index.html', context_dict, context)

def about(request):
	context = RequestContext(request)
	
	return render_to_response('rango/about.html', None, context)
