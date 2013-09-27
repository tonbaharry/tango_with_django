from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page

def encode_url(str):
	return str.replace(' ', '_').lower()

def decode_url(str):
	return str.replace('_', ' ').capitalize()

def index(request):
	# Request the context of the request.
	context = RequestContext(request)
	
	# Query the database for a list of ALL categories currently stored.
	# Order by the number of likes and show the top five anyway.
	category_list = Category.objects.order_by('-likes')[:5]
	context_dict = {'categories': category_list}
	
	# Loop through each category returned, creating a URL attribute.
	# The attribute stores an encoded URL (spaces replaced by underscores).
	for category in category_list:
		category.url = encode_url(category.name)
	
	# Work out the top 5 pages (in terms of views) across all categories.
	page_list = Page.objects.order_by('-views')[:5]
	context_dict['pages'] = page_list
	
	# Render the response and send it back!
	return render_to_response('rango/index.html', context_dict, context)

def about(request):
	context = RequestContext(request)
	
	return render_to_response('rango/about.html', None, context)

def category(request, category_name_url):
	# Request our context
	context = RequestContext(request)
	
	# Change underscores in the category name to spaces.
	# URL's don't handle spaces well, so we encode them as underscores. 
	category_name = decode_url(category_name_url)
	
	# Build up the dictionary we will use as out template context dictionary.
	context_dict = {'category_name': category_name}
	
	try:
		# Find the category with the given name.
		# Raises an exception if the category doesn't exist.
		# We also do a case insensitive match.
		category_model = Category.objects.get(name__iexact=category_name)
		
		# Retrieve all the associated pages.
		# Note that filter returns >= 1 model instance.
		pages = Page.objects.filter(category=category_model)
		
		# Adds our results list to the template context under name pages.
		context_dict['pages'] = pages
	except Category.DoesNotExist:
		# We get here if the category does not exist.
		# Will trigger the template to display the 'no category' message.
		pass
	
	# Go render the response and return it to the client.
	return render_to_response('rango/category.html', context_dict, context)

