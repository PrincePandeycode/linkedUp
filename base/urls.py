from django.urls import path
from . import views

urlpatterns = [
    path('',views.homepage,name = "home"),
    path('lobby', views.lobby,name="lobby"),
    path('room', views.room),

    #52. here is the url for the view 
    path('get_token', views.getToken), #http://localhost:8000/get_token?channel=mynewsite --> locally its working. we see a uid and a token generated on web screen. 
    #53. now we will check if it is generated automatically correct . So we go to streams.js and make changes there
    # 101. for stronig our data into backend(database)
    path('create_member',views.createMember),
    # 102. Now the frontend, we need to send the data from frontend to this view
    # we will create a function in frontend(streams.js) that will send data to backend view
    # go to streams.js

    # 114. url to get other members name from backkend(database) --> now we will create a function to get others name in streams.js
    path('get_member',views.getMember),

    #122. path to deletMember view, will be used to send data from frontend
    path('delete_member',views.deleteMember),

    path('save_post/', views.save_post, name='save_post'),

    



]
