import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from .models import ChatRoom, ChatRoomMessage
from boards.models import Topic
from accounts.models import CustomUser

class ChatRoomConsumer(AsyncWebsocketConsumer):
    
    ##### ChatRoom #####
    @database_sync_to_async
    def check_room_name_in_topic(self, roomname):
        result = Topic.objects.filter(topic=roomname).exists()
        return result
    
    @database_sync_to_async
    def get_chatroom(self, topic):
        room_name = ChatRoom.objects.get(room_name=topic).room_name
        return room_name
    
    @database_sync_to_async
    def add_user_in_chatroom(self, room_name, user):
        """
        return the number of users in a current chat room.
        """
        chat_room = ChatRoom.objects.get(room_name=room_name)
        chat_room.users.add(user)
        numbers_of_users = chat_room.users.all().count()
        return numbers_of_users
    
    @database_sync_to_async
    def remove_user_from_chatroom(self, room_name, user):
        """
        return the number of users in a current chat room, when user is out of the chat room.
        """
        chat_room = ChatRoom.objects.get(room_name=room_name)
        chat_room.users.remove(user)
        numbers_of_users = chat_room.users.all().count()
        return numbers_of_users
    
    ##### ChatRoomMessage #####
    @database_sync_to_async
    def save_user_message(self, room_name, username, message):
        writer = CustomUser.objects.get(username=username)
        chat_room = ChatRoom.objects.get(room_name=room_name)
        message = ChatRoomMessage.objects.create(
            room_name=chat_room,
            message=message,
            writer=writer
        )
        message.save()
    
    
    
    async def connect(self):
        self.room_name = await self.get_chatroom(
            self.scope['url_route']['kwargs']['topic']
        )
        self.username = self.scope['user'].username
        self.room_group_name = f'chat_{self.room_name}'
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )
        await self.accept()
        
        # Check if the room name is in board topic query, otherwise force to disconnect.
        self.result = await self.check_room_name_in_topic(self.room_name)
        if not self.result:
            await self.close()
        
        # add user into chatroom
        self.numbers_of_users = await self.add_user_in_chatroom(
            self.room_name, self.scope['user']
        )
        # send a message when new user joined this chat room.
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_joined',
                'joined_user': self.username,
                'numbers_of_users': self.numbers_of_users,
            }
        )
    
    async def chat_joined(self, event):
        joined_user = event['joined_user']
        numbers_of_users = event['numbers_of_users']
    
        await self.send(text_data=json.dumps({
            'action': 'user_joined',
            'joined_user': joined_user,
            'numbers_of_users': numbers_of_users,
        }))
        
    async def disconnect(self, close_code):
        # remove user from the chat room
        self.numbers_of_users = await self.remove_user_from_chatroom(
            self.room_name, self.scope['user']
        )
        # Update the number of users and send it to the chatroom
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_exits',
                'numbers_of_users': self.numbers_of_users,
            }
        )
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )
        
    async def user_exits(self, event):
        numbers_of_users = event['numbers_of_users']
        
        await self.send(text_data=json.dumps({
            'action': 'user_exits',
            'numbers_of_users': numbers_of_users,
        }))
        
    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']
        user_avatar = text_data_json['user_avatar']
        await self.save_user_message(
            self.room_name,
            username,
            message
        )
        
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_massage',
                'message': message,
                'username': username,
                'user_avatar': user_avatar,
            }
        )
        
    # Receive message from room group
    async def chat_massage(self, event):
        message = event['message']
        username = event['username']
        user_avatar = event['user_avatar']
        
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'action': 'user_message',
            'message': message,
            'username': username,
            'userAvatar': user_avatar,
        }))
    
    pass