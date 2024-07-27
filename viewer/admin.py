from django.contrib import admin
from .models import Album, Post, UserProfile, Blogpost, Slide

admin.site.register(Album)
admin.site.register(Post)
admin.site.register(Blogpost)
admin.site.register(Slide)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username',)

class SlideAdmin(admin.ModelAdmin):
    list_display = ('id', 'caption', 'image')
