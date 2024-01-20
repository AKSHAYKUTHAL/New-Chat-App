import json
from channels.consumer import AsyncConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import Thread,ChatMessage,ThreadManager
# from chat.models import Thread, ChatMessage
from asgiref.sync import sync_to_async


User = get_user_model()


class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):

        await self.send({
            'type': 'websocket.accept'
        })

        user = self.scope['user']
        threads = await self.get_user_threads(user)

        for thread in threads:
            chat_room = f'chatroom_{thread.unique_id}'
            await self.channel_layer.group_add(
                chat_room,
                self.channel_name
            )

    async def websocket_receive(self, event):
        # print('receive', event)
        received_data = json.loads(event['text'])
        msg = received_data.get('message')
        sent_by_id = received_data.get('sent_by')
        send_to_id = received_data.get('send_to')
        thread_id = received_data.get('thread_id')
        unique_id = received_data.get('unique_id')

        if not msg:
            print('Error:: empty message')
            return False
        
        if not unique_id:
            print('Error: unique_id is missing')
            return
        
        chat_room = f'chatroom_{unique_id}'
        self.chat_room = chat_room


        sent_by_user = await self.get_user_object(sent_by_id)
        send_to_user = await self.get_user_object(send_to_id)
        thread_obj = await self.get_thread(thread_id)
        if not sent_by_user:
            print('Error:: sent by user is incorrect')
        if not send_to_user:
            print('Error:: send to user is incorrect')
        if not thread_obj:
            print('Error:: Thread id is incorrect')

        await self.create_chat_message(thread_obj, sent_by_user, msg)

        
        self_user = self.scope['user']
        response = {
            'message': msg,
            'sent_by': self_user.id,
            'thread_id': thread_id,
            'unique_id': unique_id,
        }

        # await self.channel_layer.group_add(
        #     chat_room,
        #     self.channel_name
        # )


        await self.channel_layer.group_send(
            self.chat_room,
            {
                'type': 'chat_message',
                'text': json.dumps(response)
            }
        )



    async def websocket_disconnect(self, event):
        print('disconnect', event)


    async def chat_message(self, event):
        # print('chat_message', event)
        await self.send({
            'type': 'websocket.send',
            'text': event['text']
        })



    @database_sync_to_async
    def get_user_object(self, user_id):
        return User.objects.filter(id=user_id).first()

    @database_sync_to_async
    def get_thread(self, thread_id):
        return Thread.objects.filter(id=thread_id).first()

    @database_sync_to_async
    def create_chat_message(self, thread, user, msg):
        ChatMessage.objects.create(thread=thread, user=user, message=msg)

    @database_sync_to_async
    def get_user_threads(self, user):
        return list(Thread.objects.by_user(user=user))
    
    
