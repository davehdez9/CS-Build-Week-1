from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from pusher import Pusher
from django.http import JsonResponse
from decouple import config
from django.contrib.auth.models import User
from adventure.models import Room
from .models import *
from rest_framework.decorators import api_view
import json

# instantiate pusher
pusher = Pusher(app_id=config('PUSHER_APP_ID'), key=config(
    'PUSHER_KEY'), secret=config('PUSHER_SECRET'), cluster=config('PUSHER_CLUSTER'))


@csrf_exempt
@api_view(["GET"])
def initialize(request):
    user = request.user
    player = user.player
    player_id = player.id
    uuid = player.uuid
    room = player.room()
    nextRooms = [{'n': room.n_to}, {'e': room.e_to},
                 {'s': room.s_to}, {'w': room.w_to}]
    players = room.playerNames(player_id)
    return JsonResponse({'uuid': uuid, 'name': player.user.username, 'title': room.title, 'x_coor': room.x_coor, 'y_coor': room.y_coor, 'description': room.description, 'nextRooms': nextRooms, 'players': players}, safe=True)


@csrf_exempt
@api_view(["GET"])
def getRoomCoors(request):
    allRooms = Room.objects.all()
    coors = [[room.x_coor, room.y_coor] for room in allRooms]
    return JsonResponse({'coors': coors}, safe=True)


@csrf_exempt
@api_view(["GET"])
def getMatrix(request):
    allRooms = Room.objects.all()
    coors = [[room.x_coor, room.y_coor] for room in allRooms]

    matrix = []
    for i in range(0, 50):
        matrix.append([])
        for j in range(0, 50):
            matrix[i].append(0)

    for x, y in coors:
        matrix[y][x] = 1

    return JsonResponse({'matrix': matrix}, safe=True)


@csrf_exempt
@api_view(["POST"])
def move(request):
    dirs = {"n": "north", "s": "south", "e": "east", "w": "west"}
    reverse_dirs = {"n": "south", "s": "north", "e": "west", "w": "east"}
    player = request.user.player
    player_id = player.id
    player_uuid = player.uuid
    data = json.loads(request.body)
    direction = data['direction']
    room = player.room()

    nextRoomID = None

    if direction == "n":
        nextRoomID = room.n_to
    elif direction == "s":
        nextRoomID = room.s_to
    elif direction == "e":
        nextRoomID = room.e_to
    elif direction == "w":
        nextRoomID = room.w_to
    if nextRoomID is not None and nextRoomID > 0:
        # Room we are moving to
        nextRoom = Room.objects.get(id=nextRoomID)

        # Rooms we can move to after we move to the Next Room
        nextNextRooms = [{'n': nextRoom.n_to}, {'e': nextRoom.e_to}, {
            's': nextRoom.s_to}, {'w': nextRoom.w_to}]

        player.currentRoom = nextRoomID
        player.save()
        players = nextRoom.playerNames(player_id)
        currentPlayerUUIDs = room.playerUUIDs(player_id)
        nextPlayerUUIDs = nextRoom.playerUUIDs(player_id)

        # Pusher Triggers
        for p_uuid in currentPlayerUUIDs:
            pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {
                           'message': f'{player.user.username} has walked {dirs[direction]}.'})
        for p_uuid in nextPlayerUUIDs:
            pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {
                           'message': f'{player.user.username} has entered from the {reverse_dirs[direction]}.'})

        return JsonResponse({'name': player.user.username, 'title': nextRoom.title, 'description': nextRoom.description, 'players': players, 'nextRooms': nextNextRooms, 'error_msg': ""}, safe=True)
    else:
        players = room.playerNames(player_id)
        return JsonResponse({'name': player.user.username, 'title': room.title, 'description': room.description, 'players': players, 'error_msg': "You cannot move that way."}, safe=True)


# @csrf_exempt
@api_view(["POST"])
def say(request):
    # IMPLEMENT
    print('Request', request)
    print('Request User', request.user)
    print('Player Id', request.user.player.id)

    data = json.loads(request.body)
    pusher.trigger('public-channel', 'broadcast',
                   {'message': data['message']})

    return JsonResponse({'error': "Not yet implemented"}, safe=True, status=500)
