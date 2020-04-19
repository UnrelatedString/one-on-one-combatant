import asyncio

cmds = {}
docs = {}
helptext = ''

def cmd(*aliases):
    def ind(f):
        names = (f.__name__, *aliases)
        for name in names:
            cmds[name] = f
        docs[names] = f.__doc__
        return f
    return ind

@cmd('h')
async def help(bot, args, message):
    '''Prints this list of commands.'''
    await message.channel.send(helptext)

@cmd('duel', 'play', 'battle')
async def challenge(bot, args, message):
    ch = message.channel
    timeout = 60
    if not message.mentions:
        await ch.send('You must mention a user to challenge them.')
        return
    opponent = message.mentions[0]
    await ch.send(f'{message.author.display_name} has challenged {opponent.display_name} to a duel!\nThey have {timeout} seconds to accept.')
    await asyncio.sleep(timeout)
    await ch.send('Challenge timed out.')

for names in sorted(docs):
    helptext += f'> **{", ".join(names)}:** {docs[names]}\n'