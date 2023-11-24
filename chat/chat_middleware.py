from asgiref.sync import sync_to_async

class ChatRoomMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response
    def process_request(self,request):
        request.test = "This test for receiver"
        return None
    def __call__(self,request):
        response = self.get_response(request)
        return response 
    
class AsyncChatRoomMiddleware:
    def __init__(self,inner):
        self.inner = inner
    async def __call__(self,scope,receive,send):
        @sync_to_async
        def get_receiver_id(session):
            receiver_id = session.get('receiver_id')
            return receiver_id
        
        scope['receiver_id'] = await get_receiver_id(scope['session'])
        return await self.inner(scope,receive,send)
    