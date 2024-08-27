from .models import Group, Chat
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("Websocket Connectied...")
        print("Channel Layer...", self.channel_layer)
        print("Channel Name...", self.channel_name)
        
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        print('Group Name...', self.room_name)
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )
        await self.accept() # to accept the connection

        # await self.close() # to force close/reject the connection. use self.close(code=4123) to add custom websocket error code  
    
    async def receive(self, text_data=None, bytes_data=None):
        print("Message Recieved...", text_data)
        
        print(self.scope['user'])
        if self.scope['user'].is_authenticated:
            data = json.loads(text_data)
            # if need to save data to database then do here
            await self.save_message(self.room_name, data['message'])
            
            data['user'] = self.scope['user'].username # get the username 

            await self.channel_layer.group_send(
                self.room_name,
                {
                    'type': 'chat.message',
                    'message': data
                }
            )
        else:
            await self.send(text_data=json.dumps({
                "message": "Login Required.",
                "user": "unknown"
            }))

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
        print('Event...', event['message'])

        # then send message to the client
        await self.send(text_data=json.dumps(event['message']))

    
    
    async def disconnect(self, close_code):
        print("Disconnect...", close_code)
        
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )





