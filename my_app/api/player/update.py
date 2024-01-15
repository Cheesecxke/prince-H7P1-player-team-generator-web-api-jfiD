## /////////////////////////////////////////////////////////////////////////////
## YOU CAN FREELY MODIFY THE CODE BELOW IN ORDER TO COMPLETE THE TASK
## /////////////////////////////////////////////////////////////////////////////

from django.http.response import JsonResponse
from rest_framework.request import Request
from rest_framework import status
from typing import Any

#Retrieving our models(tables or database)
from my_app.models.player import Player

# This is where I believe we will get our data from(that is in the database)
from my_app.serializers.player import PlayerSerializer

position_list = ["defender", "midfielder", "forward"]
skills_list = ["defense", "attack", "speed", "strength", "stamina"]

def message(text):
    return {"message": text}

def check(data):
    # We are checking the data if it is valid
    if not((data["position"] in position_list)):
        return message("Invalid value for position: " + data["position"])

    if not(data["age"].isnumeric()):
        return message("Invalid value for age: " + data["age"])

    if (type(data["playerSkills"]) == list):
        for i in data["playerSkills"]:
            if not((i["skill"] in skills_list)):
                return message("Invalid value for skill: " + i["skill"])
            if not(str(i["value"]).isnumeric()):
                return message("Invalid value for value: " + i["value"])
    else:
        if not ((data["playerSkills"]["skill"] in skills_list)):
            return message("Invalid value for skill: " + data["playerSkills"]["skill"])
        if not (str(data["playerSkills"]["value"]).isnumeric()):
            return message("Invalid value for value: " + data["playerSkills"]["value"])

def update_player_handler(request: Request, id: Any):
    # check the input
    done = ""
    if not(request.data == {}):
        done = check(request.data)
        if not (done == ""):
            return done

        player = Player.objects.get(id=id)
        serializer = PlayerSerializer(instance=player)
        serializer.update(player, request.data)

    return JsonResponse('', status=status.HTTP_500_INTERNAL_SERVER_ERROR, safe=False)
