from commands import cmds, docs, helptext #this is messy

class Bot:
    def __init__(self, client):
        self.client = client
        @client.event
        async def on_message(message):
            if message.author == client.user:
                return
            await self.handle_message(message)

    async def handle_message(self, message):
        print(f'{message.author}: {message.content}')
        # make better system later
        prefix = "c!"
        if message.content.startswith(prefix):
            text = message.content[len(prefix):] or '[blank]'
            cmd = text.split()[0]
            if cmd.lower() in cmds:
                await cmds[cmd](self, message)
            else:
                await message.channel.send(f"{cmd} is not a valid command. Use {prefix}help")

