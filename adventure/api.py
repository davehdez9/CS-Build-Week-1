from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from pusher import Pusher
from django.http import JsonResponse
from decouple import config
from django.contrib.auth.models import User
from adventure.models import Room, Monster, Player
from .models import *
from rest_framework.decorators import api_view
import json
import operator

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
    monster = Monster.objects.get(id=room.monster.id)
    roomMonster = {
        'name': monster.name,
        'description': monster.description,
        'honeyGained': monster.honeyGained,
        'honeyLost': monster.honeyLost,
        'xpGained': monster.honeyGained,
        'xp': monster.xp
    }

    return JsonResponse({'uuid': uuid, 'xp': player.xp, 'honey': player.honey, 'name': player.user.username, 'title': room.title, 'roomId': room.id, 'monster': roomMonster, 'x_coor': room.x_coor, 'y_coor': room.y_coor, 'description': room.description, 'nextRooms': nextRooms, 'players': players}, safe=True)


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
    monster = Monster.objects.get(id=room.monster.id)
    roomMonster = {
        'name': monster.name,
        'description': monster.description,
        'honeyGained': monster.honeyGained,
        'honeyLost': monster.honeyLost,
        'xpGained': monster.honeyGained,
        'xp': monster.xp
    }

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
        nextMonster = Monster.objects.get(id=nextRoom.monster.id)
        nextRoomMonster = {
            'name': monster.name,
            'description': monster.description,
            'honeyGained': monster.honeyGained,
            'honeyLost': monster.honeyLost,
            'xpGained': monster.honeyGained,
            'xp': monster.xp
        }

        # Rooms we can move to after we move to the Next Room
        nextNextRooms = [{'n': nextRoom.n_to}, {'e': nextRoom.e_to}, {
            's': nextRoom.s_to}, {'w': nextRoom.w_to}]

        player.currentRoom = nextRoomID
        player.save()
        players = nextRoom.playerNames(player_id)
        currentPlayerUUIDs = room.playerUUIDs(player_id)
        nextPlayerUUIDs = nextRoom.playerUUIDs(player_id)

        # Pusher Triggers
        # for p_uuid in currentPlayerUUIDs:
        #     pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {
        #                    'message': f'{player.user.username} has walked {dirs[direction]}.'})
        # for p_uuid in nextPlayerUUIDs:
        #     pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {
        #                    'message': f'{player.user.username} has entered from the {reverse_dirs[direction]}.'})

        return JsonResponse({'name': player.user.username, 'title': nextRoom.title, 'description': nextRoom.description, 'roomId': nextRoom.id, 'monster': nextRoomMonster, 'x_coor': nextRoom.x_coor, 'y_coor': nextRoom.y_coor, 'players': players, 'nextRooms': nextNextRooms, 'error_msg': ""}, safe=True)
    else:
        players = room.playerNames(player_id)
        return JsonResponse({'name': player.user.username, 'title': room.title, 'roomId': room.id, 'description': room.description, 'monster': roomMonster, 'x_coor': room.x_coor, 'y_coor': room.y_coor, 'players': players, 'error_msg': "You cannot move that way."}, safe=True)


@csrf_exempt
@api_view(["POST"])
def say(request):
    # IMPLEMENT
    # print('Request', request)
    # print('Request User', request.user)
    # print('Player Id', request.user.player.id)
    # print('Room ID', request.user.player.room().id)
    user = request.user.username
    roomId = request.user.player.room().id

    data = json.loads(request.body)
    pusher.trigger(f'room-{roomId}', 'broadcast',
                   {'user': user, 'message': data['message']})

    return JsonResponse({'user': user, 'message': data['message']}, safe=True, status=200)


@csrf_exempt
@api_view(["POST"])
def battleResults(request):
    user = request.user.username
    player = request.user.player
    player_id = player.id

    player_uuid = player.uuid

    data = json.loads(request.body)

    # honey Gained will just be a positive or negative number
    # Front End will just send the "lost" value in the body
    # Will subtract accordingly here
    honeyGained = data['honeyGained']
    xpGained = data['xpGained']

    player.honey += honeyGained
    player.xp += xpGained
    player.save()

    return JsonResponse({'xp': player.xp, 'honey': player.honey, 'message': f"{user} now has {player.honey} honey and {player.xp} XP"})


@csrf_exempt
@api_view(["GET"])
def leaderboard(request):
    allPlayers = Player.objects.all().order_by('-xp')
    players = [{'username': player.user.username, 'honey': player.honey, 'xp': player.xp}
               for player in allPlayers][:10]

    return JsonResponse({'topPlayers': players})
