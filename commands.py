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
    '''Requests a game from mentioned user.'''
    ch = message.channel
    timeout = 60
    if not message.mentions:
        await ch.send('You must mention a user to challenge them.')
        return
    opponent = message.mentions[0]
    await ch.send(f'{message.author.display_name} has challenged {opponent.display_name} to a duel!\nThey have {timeout} seconds to accept with `{bot.prefix}accept @{message.author.display_name}`')
    await asyncio.sleep(timeout)
    await ch.send('Challenge timed out.')

@cmd('a')
async def accept(bot, args, message):
    '''Accepts requested game.'''
    ch = message.channel
    if not message.mentions:
        await ch.send("You can't accept nobody's challenge!")
        return
    opponent = message.mentions[0]
    await ch.send('sike')

for names in sorted(docs): #handle >2000 at some point maybe? eh
    helptext += f'> **{", ".join(names)}:** {docs[names]}\n'
