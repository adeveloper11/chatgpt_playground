from django.contrib import admin
from .models import ChatLog, QueryOption, Feedbackdata, Login

# Register the ChatLog model with the admin site
admin.site.register(ChatLog)
admin.site.register(QueryOption)
admin.site.register(Feedbackdata)
admin.site.register(Login)
