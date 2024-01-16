## /////////////////////////////////////////////////////////////////////////////
## YOU CAN FREELY MODIFY THE CODE BELOW IN ORDER TO COMPLETE THE TASK
## /////////////////////////////////////////////////////////////////////////////

from django.http.response import JsonResponse
from rest_framework.request import Request
from rest_framework import status

# This is where I believe we will get our data from(that is in the database)
from my_app.serializers.player import PlayerSerializer

#Retrieving our models(tables or database)
from my_app.models.player import Player

position_list = ["defender", "midfielder", "forward"]
skills_list = ["defense", "attack", "speed", "strength", "stamina"]

position_list = ["defender", "midfielder", "forward"]
skills_list = ["defense", "attack", "speed", "strength", "stamina"]


def message(text):
    return {"message": text}


def check(request):
    # We are checking the data if it is valid
    if request["name"] == "":
        return message("Invalid value for name: Empty")

    if request["position"] == "":
        return message("Invalid value for position: Empty")

    if not (request["position"] in position_list):
        return message("Invalid value for position: " + request["position"])

    if request["playerSkills"] in ["", {}, []]:
        return message("Invalid value for playerSkills: Empty")

    if type(request["playerSkills"]) == list:
        for i in request["playerSkills"]:
            if i["skill"] == "":
                return message("Invalid value for skill: Empty")
            if i["value"] == "":
                return message("Invalid value for value: Empty")
            if not (i["skill"] in skills_list):
                return message("Invalid value for skill: " + i["skill"])
            if not (str(i["value"]).isnumeric()):
                return message("Invalid value for value: " + str(i["value"]))
            if not (0 <= i["value"] <= 100):
                return message("Invalid value for value: " + str(i["value"]))
    else:
        if request["playerSkills"]["skill"] == "":
            return message("Invalid value for skill: Empty")
        if request["playerSkills"]["value"] == "":
            return message("Invalid value for value: Empty")
        if not (request["playerSkills"]["skill"] in skills_list):
            return message("Invalid value for skill: " + request["playerSkills"]["skill"])
        if not (str(request["playerSkills"]["value"]).isnumeric()):
            return message("Invalid value for value: " + str(request["playerSkills"]["value"]))
        if not (0 <= request["playerSkills"]["value"] <= 100):
            return message("Invalid value for value: " + str(request["playerSkills"]["value"]))

    return ""


def valid(validated_data):
    if validated_data.get("name", None) is None:  # no name
        return message("Invalid value for name: None")
    if validated_data.get("position", None) is None:  # no position
        return message("Invalid value for position: None")
    if validated_data.get("playerSkills", None) is None:  # no skills
        return message("Invalid value for playerSkills: None")

    if validated_data.get("playerSkills") in ["", {}, []]:
        return message("Invalid value for playerSkills: Empty")

    var = validated_data.get("playerSkills")
    playerSkills = []
    if (type(var) == dict):
        playerSkills.append(var)
    else:
        for i in var:
            playerSkills.append(i)

    for playerSkill in playerSkills:
        if playerSkill.get("skill", None) is None:  # no skill
            return message("Invalid value for skill: None")
        if playerSkill.get("value", None) is None:  # no value
            return message("Invalid value for value: None")

    return ""
def create_player_handler(request: Request):
    # Check is data valid
    validity = ""
    validity = valid(request.data)
    if not (validity == ""):
        return JsonResponse(validity, status=status.HTTP_500_INTERNAL_SERVER_ERROR, safe=False)

    # Checks if there is empty strings or wrong information
    done = ""
    done = check(request.data)
    if not (done == ""):
        return JsonResponse(done, status=status.HTTP_500_INTERNAL_SERVER_ERROR, safe=False)

    serializer = PlayerSerializer(Player)
    serializer.create(validated_data=request.data)

    return JsonResponse('', status=status.HTTP_500_INTERNAL_SERVER_ERROR, safe=False)
