from channels.consumer import AsyncConsumer
import json
from channels.db import database_sync_to_async
from .models import Group, Chat


class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("Websocket connected...", event)
        print('Channel Layer...', self.channel_layer) #get default channel layer from the project
        print('Channel Name...', self.channel_name) #get channel name

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        print('Group Name...', self.room_name)
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )

        await self.send({ # send to client 
            'type': 'websocket.accept',
        })
    
    async def websocket_receive(self, event):
        print("Message received form client...", event['text'])

        print(self.scope['user'])
        if self.scope['user'].is_authenticated:
            # if need to save data to database then do here
            data = json.loads(event['text']) # string to dict
            print('Data ...', data['message'])
            await self.save_message(self.room_name, data['message'])

            data['user'] = self.scope['user'].username # get the username 
            
            # send message to the group which is room_name
            await self.channel_layer.group_send(  
                self.room_name,
                {
                    'type': 'chat.message', # this-->chat.message event for this-->chat_message event handler
                    'message': json.dumps(data),
                }
            )
        else:
            await self.send({ # send to client 
                'type': 'websocket.send',
                'text': json.dumps({"message": "Login Required.", "user":"unknown"}) # python object to json string 
            })
    
    @database_sync_to_async
    def save_message(self, room_name, message):
        # This method runs in a synchronous context
        group = Group.objects.get(name=room_name)
        chat = Chat(
            content=message,
            group=group
        )
        chat.save() 

    async def chat_message(self, event):
        print('Event...', event)

        # then send message to the client
        await self.send({ 
            'type': 'websocket.send',
            'text': event['message']
        })

    
    async def websocket_disconnect(self, event):
        print('Websocket Disconnected...', event)

        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )