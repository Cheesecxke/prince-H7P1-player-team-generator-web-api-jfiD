## /////////////////////////////////////////////////////////////////////////////
## YOU CAN FREELY MODIFY THE CODE BELOW IN ORDER TO COMPLETE THE TASK
## /////////////////////////////////////////////////////////////////////////////

from django.http.response import JsonResponse
from rest_framework.request import Request
from rest_framework import status

# For sending json data
from rest_framework.response import  Response

# For receiving method sent and the possible json data
from rest_framework.decorators import api_view

# This is where I believe we will get our data from(that is in the database)
from my_app.serializers.player import PlayerSerializer
from my_app.serializers.player_skill import PlayerSkillSerializer

#Retrieving our models(tables or database)
from my_app.models.player import Player
from my_app.models.player_skill import PlayerSkill

# Personal Reasons :)
from collections import OrderedDict
from rest_framework.utils.serializer_helpers import ReturnList

position_list = ["defender", "midfielder", "forward"]
skills_list = ["defense", "attack", "speed", "strength", "stamina"]

def message(text):
    return {"message": text}

def check(request):
    # We are checking the data if it is valid
    if not((request.data["position"] in position_list)):
        return message("Invalid value for position: " + request.data["position"])

    if not(request.data["age"].isnumeric()):
        return message("Invalid value for age: " + request.data["age"])

    if (type(request.data["playerSkills"]) == list):
        for i in request.data["playerSkills"]:
            if not((i["skill"] in skills_list)):
                return message("Invalid value for skill: " + i["skill"])
            if not(str(i["value"]).isnumeric()):
                return message("Invalid value for value: " + i["value"])
    else:
        if not ((request.data["playerSkills"]["skill"] in skills_list)):
            return message("Invalid value for skill: " + request.data["playerSkills"]["skill"])
        if not (str(request.data["playerSkills"]["value"]).isnumeric()):
            return message("Invalid value for value: " + request.data["playerSkills"]["value"])

def create_player_handler(request: Request):
    done = ""
    done = check(request)
    if not (done == ""):
        return Response(done)

    serializer = PlayerSerializer(Player)
    serializer.create(validated_data=request.data)


    return JsonResponse('', status=status.HTTP_500_INTERNAL_SERVER_ERROR, safe=False)
