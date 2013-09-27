from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm, PageForm

def encode_url(str):
	return str.replace(' ', '_')

def decode_url(str):
	return str.replace('_', ' ')

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
	context_dict = {'category_name': category_name, 'category_name_url': category_name_url}
	
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

def add_category(request):
    # Get the context from the request.
    context = RequestContext(request)

    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            return index(request)
        else:
            # No form passed - ignore and keep going.
            pass
    else:
        # If the request was not a POST, display the form to enter details.
        form = CategoryForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render_to_response('rango/add_category.html', {'form': form}, context)


def add_page(request, category_name_url):
    context = RequestContext(request)

    category_name = decode_url(category_name_url)
    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            # This time we cannot commit straight away.
            # Not all fields are automatically populated!
            page = form.save(commit=False)

            # Retrieve the associated Category object so we can add it.
            cat = Category.objects.get(name=category_name)
            page.category = cat

            # Also, create a default value for the number of views.
            page.views = 0

            # With this, we can then save our new model instance.
            page.save()

            # Now that the page is saved, display the category instead.
            return category(request, category_name)
        else:
            print form.errors
    else:
        form = PageForm()

    return render_to_response( 'rango/add_page.html',
            {'category_name_url': category_name_url,
             'category_name': category_name, 'form': form},
             context)