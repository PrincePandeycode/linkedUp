from django.shortcuts import render
# 38. from documentation of agora tokn builer. import these packages
from agora_token_builder import RtcTokenBuilder
# 42. importing the module required for json response
from django.http import JsonResponse
# 45. importing random
import random
#48. importing time
import time
# 91
import json
# 95.
from .models import RoomMember
# 99.
from django.views.decorators.csrf import csrf_exempt

from datetime import datetime

from .models import Post

# Create your views here.
def homepage(request):
    return render(request,'base/home.html')

def lobby(request):
    return render(request,'base/lobby.html')

def room(request):
    current_time = datetime.now()
    return render(request,'base/room.html', {'current_time': current_time})

# 39. now the function that generate the token automaticlly using token builder
def getToken(request):

    # ------------------------------------------------------------------------
    

    # 43. now we will set up all the required variables like appId, appCertificate, channelName, uid, role, privilegeExpiredTs
    appId = '2c67e9a895d04a318044724f6a4bc0d0'  # from agora console ,app is my videochat
    appCertificate = 'b710f3987c7947639f83f2fa5bfc94dd' #from agora
    channelName = request.GET.get('channel') #we will get it from user, for now the url of this view
    # 44. uid has to be a number between  1 and 230 , so we will import random to generate this
    uid = random.randint(1,230)
    # 46 . Now we will set the expiration time for token in seconds. its your choice (used by process 49 )
    expirationTimeInSeconds = 3600*24 #3600 seconds means 1 hour and 24 times meand 24 hrs or 1 day
    
    #47. getting current time stmap , then we will use the expirationtime that is 1 day to figure out excatly when it is going to expire
    currentTimeStamp = time.time() #used by process 49

    #49. now again to the rtctokenbuilder parameter, when it is going to expire
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds

    # 50. now setting the role for the parameter, if it is 1 --> host, 2--> guest , at this point it doesnt matter cause we are relly not dealing with authentication now
    role = 1 # for time being setting role to 1 for everybody
# ----------------------------------------------------------------------------------------

    # 51.now we will create url to test this endpoint or view. got to urls.py

    # 40. this line is also from token-builder documentation.
    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)
    # 41. we will return a json response. basiccally it is an object which returns things like the generated token, userid,etc things generated by ths function
    # basically this is an api call that we are going to make asynchronously using ajax
    return JsonResponse({'token':token, 'uid':uid}, safe=False) # 42. we are returning two things here token and uid as py dictionary like a json object also safe=False: By default, Django's JsonResponse class requires the data to be JSON-serializable, meaning it should be a list or a dictionary. Setting safe=False allows you to return other data types (such as dictionaries) directly without wrapping them in a list.


# 88 . creating user in db
# 100. using csrf_exempt as we are telling we dont need csrf protection for this view for now
@csrf_exempt #Now we need to create a url for this -->urls.py
def createMember(request):
    #89 first of all we get the data from frontend, so we are going to send a post request to backend
    # 90. As it is going to be json data from frontend, we have to parse it, importing json
    data = json.loads(request.body) # 91.This line of code parses the JSON data sent by the client (contained in request.body) and stores it in the variable data as a Python dictionary. Once parsed, you can access the data sent by the client as key-value pairs in the data dictionary.
    # 92. json.loads converts json to python dictionary. request.body has json data from frontend
    # 93. now we have the data we can crete a roomMember in db or search for a room memeber if it exists
    # 94. importing RoomMember frommodels
    # 95. now we will create the memeber if it is not there 

    member, created = RoomMember.objects.get_or_create(
        name = data['name'],
        uid = data['UID'],
        room_name = data['room_name']
    )
#    96.the code snippet is attempting to retrieve a RoomMember object from the database based on the provided name, UID, and room name.
#   If the object exists, it retrieves it. If the object does not exist, it creates a new RoomMember object with the provided attributes. 
#   The member variable will contain the retrieved or newly created RoomMember object, and the created variable will contain a boolean value
#    indicating whether the object was newly created (True) or already existed (False).
    return JsonResponse({'name':data['name']},safe=False)
# 97. As we know we are sending this data from frontendusing POST request. so django needs the csrf token for working . for now we can expempt the csrf token thing
# 98. by importing csrf exempt and using as decorator above the view

# 110. view to display my name to all and others name to me
    # we get all values of room memeber from database using their uid and room_name
def getMember(request):
    #111. getting these two values 
    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')


#112. searching database basd on these two values
    member = RoomMember.objects.get(uid = uid, room_name = room_name)
    name = member.name


# 113. returnning an json file containing the name of user now we will create a url for this-->urls.py
    return JsonResponse({'name':member.name}, safe = False)

# 121. deleteing s member when he leaves the stream
@csrf_exempt #Now we need to create a url for this -->urls.py
def deleteMember(request):
    data = json.loads(request.body) #getting this data from from frontend ans parsing it
    member = RoomMember.objects.get(  # quering the database to get the user using these  3 attributes
        name = data['name'],
        uid = data['UID'],
        room_name = data['room_name'],
        )
    member.delete() #deleting the member
    return JsonResponse('Member was deleted',safe=False)


@csrf_exempt
def save_post(request):
    if request.method == 'POST':
        content = request.POST.get('content', None)
        if content:
            # Save the post to the database
            post = Post.objects.create(content=content)
            return JsonResponse({'success': True, 'message': 'Post saved successfully.'})
        else:
            return JsonResponse({'success': False, 'message': 'Content is required.'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method.'})

