from commands import cmds, docs, helptext #this is messy

class Bot:
    prefix = "c!"

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
        if message.content.startswith(self.prefix):
            text = message.content[len(self.prefix):] or '[blank]'
            cmd = text.split()[0]
            if cmd.lower() in cmds:
                await cmds[cmd.lower()](self, text[len(cmd)+1:], message)
            else:
                await message.channel.send(f"`{cmd}` is not a valid command. Use `{self.prefix}help`")

