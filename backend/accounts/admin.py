from django.contrib import admin
from .models import UserProfile, DailyReview

admin.site.register(UserProfile)
admin.site.register(DailyReview)