import discord

from bot import Bot

def run_bot():
    client = discord.Client()
    bot = Bot(client)
    with open('token.txt') as tokf:
        tok = tokf.read()
        print(tok)
        client.run(tok)

if __name__ == '__main__':
    run_bot()