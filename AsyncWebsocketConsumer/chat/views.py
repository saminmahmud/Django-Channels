from django.shortcuts import render
from .models import Group, Chat

def home(request):
    return render(request, 'home.html')


def chat(request, room_name):
    group = Group.objects.filter(name=room_name).first()
    chats=[]
    if group:
        chats = Chat.objects.filter(group=group)
    else:
        group = Group(name = room_name)
        group.save()

    return render(request, 'room.html', {'room_name': room_name, 'chats':chats})
