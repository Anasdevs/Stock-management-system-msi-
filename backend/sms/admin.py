from django.contrib import admin
from .models import Purchase, IssuedItem

admin.site.register(Purchase)
admin.site.register(IssuedItem)

