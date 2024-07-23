from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Service)
admin.site.register(Category)
admin.site.register(CategoryDetail)
admin.site.register(PriceOption)