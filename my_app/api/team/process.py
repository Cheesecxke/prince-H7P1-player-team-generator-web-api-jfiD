## /////////////////////////////////////////////////////////////////////////////
## YOU CAN FREELY MODIFY THE CODE BELOW IN ORDER TO COMPLETE THE TASK
## /////////////////////////////////////////////////////////////////////////////

from django.http.response import JsonResponse
from rest_framework.request import Request
from rest_framework import status

#Retrieving our models(tables or database)
from my_app.models.player import Player

# This is where I believe we will get our data from(that is in the database)
from my_app.serializers.player import PlayerSerializer

# Personal Reasons :)
from collections import OrderedDict
from rest_framework.utils.serializer_helpers import ReturnList

position_list = ["defender", "midfielder", "forward"]
skills_list = ["defense", "attack", "speed", "strength", "stamina"]

def message(text):
    return {"message": text}

def Listthem():
    player = Player.objects.all()
    serializer = PlayerSerializer(player, many=True)

    output = []
    input = []

    if not(type(serializer.data) == ReturnList):
        input.append(dict(serializer.data))
    else:
        for i in serializer.data:
            input.append(dict(i))

    for i in range(0, len(input)):
        output.append({})
        output[i]["name"] = input[i]["name"]
        output[i]["age"] = input[i]["age"]
        output[i]["position"] = input[i]["position"]
        output[i]["playerSkills"] = []


    # for the skills
    for i in range(0, len(input)):
        if type(input[i]["playerSkills"]) == list:
            for a in input[i]["playerSkills"]:
                output[i]["playerSkills"].append(dict(a))
        else:
            output[i]["playerSkills"].append(dict(input[i]["playerSkills"]))

    return output

def count(text):
    counter = 0
    player = Player.objects.all()
    serializer = PlayerSerializer(player, many=True)

    # Output to add any skills and search through them
    output = []

    if (not (type(serializer.data) == ReturnList)):  # If it is a single item AKA: not a list
        output.append(dict(serializer.data))
    else:
        for i in serializer.data:
            output.append(dict(i))

    for i in output:
        if i["position"] == text:
            counter += 1
    return counter

def positionMax(thelist):
    if (thelist==[]):
        return []

    # get the max and min
    maximum = max(thelist)
    minimum = min(thelist)

    #Retrieve the positions
    position = []
    num = maximum + 1
    while num >= minimum:
        num -= 1
        for (a, b) in enumerate(thelist):
            if b == num:
                position.append(a)
    return position

def positionMax2(thelist, pos):
    if (thelist==[]):
        return []

    # get the max and min
    maximum = max(thelist)
    minimum = min(thelist)

    #Retrieve the positions
    position = []
    num = maximum + 1
    while num >= minimum:
        num -= 1
        for (a, b) in enumerate(thelist):
            if b == num:
                position.append(pos[a])
    return position

response = ""

def team_process_handler(request: Request):
    # We are checking the data if it is valid
    global response, position_list
    if (type(request.data) == dict):
        if not(request.data["position"] in position_list):
            response = message("Invalid value for position: " + request.data["position"])
            return JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR, safe=False)

        if not((request.data["mainSkill"] in skills_list)):
            response = message("Invalid value for skill: " + request.data["mainSkill"])
            return JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR, safe=False)

        if not((str(request.data["numberOfPlayers"]).isnumeric())):
            response = message("Invalid value for numberOfPlayers: " + request.data["numberOfPlayers"])
            return JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR, safe=False)
    else:
        for i in request.data:
            if not ((i["position"] in position_list)):
                response = message("Invalid value for position: " + i["position"])
                return JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR, safe=False)

            if not ((i["mainSkill"] in skills_list)):
                response = message("Invalid value for skill: " + i["mainSkill"])
                return JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR, safe=False)

            if not ((str(i["numberOfPlayers"]).isnumeric())):
                response = message("Invalid value for numberOfPlayers: " + i["numberOfPlayers"])
                return JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR, safe=False)

    # iterate through all the requirements in data
    # We first copy all the players and skills
    # We then sort from highest to lowest to another array, by coping from old array
    # Final list that will be printed out
    final_players = []
    data = []
    # This will prepare the list of players we will print out
    if (type(request.data) == list):
        data = request.data
    else:
        data.append(request.data)

    for a in data:
        # counting the number of defenders, midfielders, forwards
        defenders = count("defender")
        midfielders = count("midfielder")
        forwards = count("forward")

        # variables
        potential = []
        position = a["position"]
        skill = a["mainSkill"]
        no_of_players = a["numberOfPlayers"]

        if (no_of_players > defenders and position == "defender"):
            if (final_players == []):
                final_players.append(message("Insufficient number of players for position: defender"))
                if (a == data[len(data) - 1]):  # If it is the last item
                    if (len(final_players) == 1):
                        final_players = final_players[0]
                    response = final_players
                    return JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR, safe=False)

                else:
                    continue
            else:
                final_players.append(message("Insufficient number of players for position: defender"))
                if (a == data[len(data) - 1]):  # If it is the last item
                    if (len(final_players) == 1):
                        final_players = final_players[0]
                    response = final_players
                    return JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR, safe=False)
                else:
                    continue
        elif (no_of_players > midfielders and position == "midfielder"):
            if (final_players == []):
                final_players.append(message("Insufficient number of players for position: midfielder"))
                if (a == data[len(data) - 1]):  # If it is the last item
                    if (len(final_players) == 1):
                        final_players = final_players[0]
                    response = final_players
                    return JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR, safe=False)
                else:
                    continue
            else:
                final_players.append(message("Insufficient number of players for position: midfielder"))
                if (a == data[len(data) - 1]):  # If it is the last item
                    if (len(final_players) == 1):
                        final_players = final_players[0]
                    response = final_players
                    return JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR, safe=False)
                else:
                    continue
        elif (no_of_players > forwards and position == "forward"):
            if (final_players == []):
                final_players.append(message("Insufficient number of players for position: forward"))
                if (a == data[len(data) - 1]):  # If it is the last item
                    if (len(final_players) == 1):
                        final_players = final_players[0]
                    response = final_players
                    return JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR, safe=False)
                else:
                    continue
            else:
                final_players.append(message("Insufficient number of players for position: forward"))
                if (a == data[len(data) - 1]):  # If it is the last item
                    if (len(final_players) == 1):
                        final_players = final_players[0]
                    response = final_players
                    return JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR, safe=False)
                else:
                    continue

        players = Listthem()

        # Add players with required position and skill
        for b in players:
            for c in b["playerSkills"]:
                if (b["position"] == position and c["skill"] == skill and not (b in potential)):
                    potential.append(b)

        # we will now sort the potentials
        # firstly we get the required skills and put them in an array
        skill_array = []
        if (not (potential == [])):
            for i1 in potential:
                for i2 in i1["playerSkills"]:
                    if (i2["skill"] == skill):
                        skill_array.append(i2["value"])

        # we get the positions
        position_array = positionMax(skill_array)
        num1 = len(position_array)

        # if we do not have enough positions, we take from part that is not the potential
        skill_array = []
        skill_value = []
        if (len(position_array) < no_of_players):
            num2 = 0
            for b in players:
                if (not (b in potential) and b["position"] == position):
                    # search for highest skill for each
                    default = b["playerSkills"][0]["value"]
                    for c in b["playerSkills"]:
                        if (c["value"] > default):
                            default = c["value"]
                    skill_array.append(num2)
                    skill_value.append(default)
                num2 += 1

        position_array += positionMax2(skill_value, skill_array)

        if (num1 >= no_of_players):
            for i in position_array[0:no_of_players]:
                final_players.append(potential[i])
        else:
            for i in position_array[0:num1]:
                final_players.append(potential[i])
            for i in position_array[num1:no_of_players]:
                final_players.append(players[i])

    if (len(final_players) == 1):
        final_players = final_players[0]

    return JsonResponse(final_players, status=status.HTTP_500_INTERNAL_SERVER_ERROR, safe=False)
