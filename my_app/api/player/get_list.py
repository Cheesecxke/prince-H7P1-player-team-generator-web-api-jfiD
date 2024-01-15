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


def get_player_list_handler(request: Request):

    player = Player.objects.all()
    if (len(list(player))==0):
        response = ''
    elif (len(list(player))==1):
        serializer = PlayerSerializer(Player)
        response = serializer.data
    else:
        serializer = PlayerSerializer(Player, many=True)  # many = true is to say allow multiple data
        response = serializer.data

    return JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR, safe=False)
