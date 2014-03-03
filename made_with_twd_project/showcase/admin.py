__author__ = 'leif'

from django.contrib import admin
from showcase.models import Category, Team, Demo, Rating

admin.site.register(Category)
admin.site.register(Team)
admin.site.register(Demo)
admin.site.register(Rating)
