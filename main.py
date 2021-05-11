import discord
import os
import datetime
import reply
import cricket
from keep_alive import keep_alive

client = discord.Client()

cric_on = False
match = 0

@client.event
async def on_message(message):
    global cric_on, match
    if message.author == client.user:
        return
    if message.content.lower().startswith('hp cricket') or cric_on:
        if message.content.lower().startswith('hp cricket') and cric_on:
            await message.channel.send('Already game is going on\nPlease wait untill the game is over.')
        elif message.content.lower().startswith('hp cricket'):
            match = cricket.cric(message)
            if match.check():
                cric_on = True
                await message.channel.send(match.ready())
            else:
                await message.channel.send('Same player cant play in two teams\nAlso bot name cant be mentioned!')
        if message.content.lower()=='send':
            for player in match.players:    
                user = await client.fetch_user(player.id)
                await user.send('hello man!')
                print('opssss')
    elif message.author.id == 689759222564651039 and message.content.lower().startswith('request'):
        msg = message.content.split(' ', 1)[1]
        try:
            user = await client.fetch_user(int(msg))
            await user.send_friend_request()
            await message.channel.send('Done.')
        except:
            await message.channel.send('Unable to send request')
    elif message.content.lower().startswith('hp') or str(message.channel).startswith('Direct'):
        msg = message.content.lower()
        msg = [wr for wr in msg.split(' ') if wr!='']
        if msg[0]=='hp':
            msg.pop(0)
        msg = ' '.join(msg)
        t = message.created_at + datetime.timedelta(hours=5, minutes=30)
        print(message.channel)
        await message.channel.send(reply.reply(msg, message, t))

keep_alive()
client.run(os.environ['TOKEN'])