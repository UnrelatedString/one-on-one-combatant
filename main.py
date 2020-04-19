import discord

from on_message import register_message_handler

def run_bot():
    client = discord.Client()
    register_message_handler(client)
    with open('token.txt') as tokf:
        tok = tokf.read()
        print(tok)
        client.run(tok)

if __name__ == '__main__':
    run_bot()