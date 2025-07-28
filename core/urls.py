from django.contrib import admin
from django.urls import path, include
from core.views import homepage_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('employer/', include('employer.urls')),
    path('', homepage_view, name='home'),
]
