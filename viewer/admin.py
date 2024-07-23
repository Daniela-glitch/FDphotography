# viewer/admin.py
from django.contrib import admin
from .models import Album, Post, UserProfile
from .models import Blogpost

admin.site.register(Album)
admin.site.register(Post)
admin.site.register(Blogpost)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)  # Adjust based on actual fields
    search_fields = ('user__username',)

