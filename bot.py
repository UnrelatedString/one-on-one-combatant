class Bot:
    def __init__(self, client):
        self.client = client
        @client.event
        async def on_message(message):
            if message.author == client.user:
                return
            print(f'{message.author}: {message.content}')
            await self.handle_message(message)

    async def handle_message(self, message):
        pass