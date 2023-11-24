from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from account.models import AccountModel
from chat.models import ChatModel,ChatListModel


class ChatRoomConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        data = {"message":"Hello World"}
        receiver_id = self.scope['receiver_id']
        sender_id = self.scope['user'].id
        self.receiver = await database_sync_to_async(AccountModel.objects.get)(pk=receiver_id)
        self.sender = await database_sync_to_async(AccountModel.objects.get)(pk=sender_id)
        self.chat_limit = [
            f"chat_{self.sender}_{self.sender.id}_to_{self.receiver}_{self.receiver.id}",
            f"chat_{self.receiver}_{self.receiver.id}_to_{self.sender}_{self.sender.id}"
        ]
        self.room_group_name = f"chat_{self.sender}_{self.sender.id}_to_{self.receiver}_{self.receiver.id}"
        self.receiver_rgn = f"chat_{self.receiver}_{self.receiver.id}_to_{self.sender}_{self.sender.id}"
        if self.room_group_name in self.chat_limit:
            await self.channel_layer.group_add(
               self.room_group_name,
               self.channel_name
            )
            await self.accept()
            print("connection established")
            
        await self.send_json(data)
    async def receive_json(self,content):
        receiver = await database_sync_to_async(AccountModel.objects.get)(pk=content['receiver_id'])
        sender = await database_sync_to_async(AccountModel.objects.get)(pk=content['sender_id'])
        message = content['message']
        obj = await database_sync_to_async(ChatModel.objects.create)(sender=sender,receiver=receiver, message=message)
        await self.channel_layer.group_send(
            self.receiver_rgn,
            {
                'type':'chat_message',
                'receiver_id':content['receiver_id'],
                'sender_id':content['sender_id'],
                'message':content['message'],
                'hour':f"{obj.time}",
            }
        )
        r_username = await sync_to_async(lambda:receiver.username)()
        s_username = await sync_to_async(lambda:sender.username)()
        time = await sync_to_async(lambda:obj.time)()
        
        receiver_chatlist = f"chatlist_{content['receiver_id']}"
        sender_chatlist = f"chatlist_{content['sender_id']}"
        chatlist_obj = await database_sync_to_async(ChatListModel.objects.get)(sender=sender,receiver=receiver)
        chatlist_id = await sync_to_async(lambda:chatlist_obj.id)()
        print("chat list id",chatlist_id)
        await self.channel_layer.group_send(
            receiver_chatlist,
            {
                'type':'chatlist',
                'chatlist_id':chatlist_id,
                'username':s_username,
                'time':f'{time}',
                'message': message,
            }
        )
        await self.channel_layer.group_send(
            sender_chatlist,
            {
                'type':'chatlist',
               'chatlist_id':chatlist_id,
                'username':r_username,
                'time':f'{time}',
                'message':message 
            }
        )
    async def chat_message(self,event):
        data = {
            'message':event['message'],
            'receiver_id':event['receiver_id'],
            'sender_id':event['sender_id'],
            'hour':event['hour']
        }
        await self.send_json(data)
    async def disconnect(self,close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
class ChatListConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room_group_name = f"chatlist_{self.scope['user'].id}"
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
    async def chatlist(self,event):
        data = {
            'username':event['username'],
            'chatlist_id':event['chatlist_id'],
            'time':event['time'][:5],
            'message':event['message']
        }
        await self.send_json(data)
        
    async def disconnect(self,close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
       