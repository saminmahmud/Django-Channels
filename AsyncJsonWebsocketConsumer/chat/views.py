from django.shortcuts import render, HttpResponse
from .models import Group, Chat
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

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


# if user hit this views then message send from here.
def SendOutsideConsumer(request):
    room_name = "batman"
    content = {
        'message': 'Message Send from outside of the consumer.',
        'user': 'unknown'
    }
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        room_name, # group name
        {
            'type': 'chat.message',
            'message': content
        }
    )
    return HttpResponse("Message Sent from view to consumer.")