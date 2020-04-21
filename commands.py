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

@cmd('h', '?')
async def help(bot, args, message):
    '''Prints this list of commands.'''
    await message.channel.send(helptext)

@cmd('duel', 'play', 'battle')
async def challenge(bot, args, message):
    '''Requests a game from mentioned user.'''
    ch = message.channel
    timeout = 30
    if not message.mentions:
        await ch.send('You must mention a user to challenge them.')
        return
    opponent = message.mentions[0]
    ret = await bot.gm.challenge(message.author, opponent)
    if ret:
        await ch.send(ret)
        return
    await ch.send(f'{message.author.display_name} has challenged {opponent.display_name} to a duel!\nThey have {timeout} seconds to accept with `{bot.prefix}accept @{message.author.display_name}`')
    await asyncio.sleep(timeout)
    if await bot.gm.expire(message.author):
        await ch.send('Challenge timed out.')

@cmd('a')
async def accept(bot, args, message):
    '''Accepts requested game.'''
    ch = message.channel
    if not message.mentions:
        await ch.send("You can't accept nobody's challenge!")
        return
    opponent = message.mentions[0]
    ret = await bot.gm.accept(opponent, message.author)
    if ret:
        await ch.send(ret)
        return
    await ch.send('Accepted!')
    await bot.gm.start_game(ch, bot.client.wait_for, message.author, opponent)

@cmd('exit','e','k')
async def kill(bot, args, message):
    '''DELETE THIS LATER but hell if it isn't easier than quitting the process'''
    await bot.client.close()

@cmd('!')
async def fight_self(bot, args, message):
    '''Start a game against yourself for easy testing purposes'''
    await bot.gm.start_game(message.channel, bot.client.wait_for, message.author, message.author)

for names in sorted(docs): #handle >2000 at some point maybe? eh
    helptext += f'> **{", ".join(names)}:** {docs[names]}\n'
