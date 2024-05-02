from django.contrib import admin

# Register your models here.
# 86. registering RoomMember here
from .models import RoomMember
from .models import Post

admin.site.register(RoomMember)
admin.site.register(Post)
 #87. Now we will create a endpoint, whenever a user joins a stream (local stream ), i mean 
#  when we join , then we will send a requets to backend asynchronously , theat will go and creta a user for us in database
# goto -->view.py