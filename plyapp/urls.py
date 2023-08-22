from django.urls import path , include
from . import views

urlpatterns = [
    path('', views.process_query, name='generate_text'),
    path('addandshow/', views.add_show, name='addandshow'),
    path('delete/<int:id>/', views.delete_option, name='deleteoption'),
    path('<int:id>/', views.updateoption, name='updateoption'),
    path('feedback/', views.feedback, name='feedback'),
    path('accounts/', include('django.contrib.auth.urls'))
    ]
