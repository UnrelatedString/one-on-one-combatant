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
async def help(bot, message):
    '''Prints this list of commands.'''
    await message.channel.send(helptext)

for names in sorted(docs):
    helptext += f'**{", ".join(names)}:** {docs[names]}\n'