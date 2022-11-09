from django.urls import path
from todo import views

urlpatterns = [
    path(r'^register/$', views.register, name='register'),
]

