from django.shortcuts import render


def index(request):
    return render(request, "test_chat/index.html")


def room(request, room_name):
    return render(request, "test_chat/room.html", {"room_name": room_name})