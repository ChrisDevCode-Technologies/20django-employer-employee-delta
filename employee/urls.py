from . import views
from django.urls import path

app_name = 'employee'
urlpatterns = [
    path('', views.index_view, name='dashboard'),
]
