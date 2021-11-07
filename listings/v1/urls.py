from django.urls import path

# plugin library

# project library
from . import views

urlpatterns = [
    path('units/', views.Units.as_view(), name='units'),
]
app_name = 'listings'
