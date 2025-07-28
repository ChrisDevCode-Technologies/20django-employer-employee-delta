from django.contrib import admin
from django.urls import path, include
from .views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),  # if applicable
    path('employee/', include('employee.urls')),  # if applicable
    # show the base.html template
    path('', home_view, name='home'),  # main app urls
]
