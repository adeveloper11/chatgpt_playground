from django.contrib import admin
from .models import ChatLog, QueryOption, Feedbackdata

# Register the ChatLog model with the admin site
admin.site.register(ChatLog)
admin.site.register(QueryOption)
admin.site.register(Feedbackdata)