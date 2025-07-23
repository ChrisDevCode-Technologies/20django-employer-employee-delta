from django.contrib import admin
from .models import UserProfile  # ✅ import the model properly

admin.site.register(UserProfile)  # ✅ register the correct model
