## /////////////////////////////////////////////////////////////////////////////
## YOU CAN FREELY MODIFY THE CODE BELOW IN ORDER TO COMPLETE THE TASK
## /////////////////////////////////////////////////////////////////////////////

from django.http.response import JsonResponse
from rest_framework.request import Request
from rest_framework import status
from typing import Any

#Retrieving our models(tables or database)
from my_app.models.player import Player

Bearer = "Bearer SkFabTZibXE1aE14ckpQUUxHc2dnQ2RzdlFRTTM2NFE2cGI4d3RQNjZmdEFITmdBQkE="

def delete_player_handler(request: Request, id: Any):

    # Get the data of the Player with the specific id
    if (Bearer == request.META.get('HTTP_AUTHORIZATION', '')):
        player = Player.objects.get(id=id)
        player.delete()

    return JsonResponse('', status=status.HTTP_500_INTERNAL_SERVER_ERROR, safe=False)
