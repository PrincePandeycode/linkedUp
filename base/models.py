from pyexpat import model
from django.db import models

# Create your models here.
#81. so what is happening is whenever user joins , we create a column in roomMember recording his
# name,roomname and uid.
# 82. on handleUserUserjoin (when a new user joins) event,query db for room member name by id . so that everyone can see their name
# 83. whe user leaves , delete that instance of roomMember
#  this model will be filled dynamically here
class RoomMember(models.Model):
    name = models.CharField(max_length=200)
    uid = models.CharField(max_length=200)
    room_name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

# 84.now makemigrations and migrtae --> creating superuser password -- prince11 username --princechat

# 85. now we will register this model into admin panel --> go to admin.py


class Post(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)