from django.contrib import admin
from .models import Purchase, IssuedItem, Items, Faculty, Department

admin.site.register(Purchase)
admin.site.register(IssuedItem)
admin.site.register(Items)
admin.site.register(Faculty)
admin.site.register(Department)

