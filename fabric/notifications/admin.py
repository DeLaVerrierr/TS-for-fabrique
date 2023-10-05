from django.contrib import admin

from .models import Client,Message,StatisticsNewletter, Newsletter

admin.site.register(Client)
admin.site.register(Message)
admin.site.register(StatisticsNewletter)
admin.site.register(Newsletter)
