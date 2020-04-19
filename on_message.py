def register_message_handler(client):
    async def on_message(message):
        if message.author == client.user:
            return
        print(f'{message.author}: {message.content}')
    client.event(on_message)