import discord
import nest_asyncio
nest_asyncio.apply()

TOKEN = "OTI3OTkzMzIzNDM0Njk2NzI0.YdSTIQ.BN72FbC3_SaYMkiGVH0Jr5e-9pY"
client = discord.Client()

#bot起動完了時に実行される処理
CHANNEL_ID = 927990496813539361


async def greet():
    channel = client.get_channel(CHANNEL_ID)
    await channel.send('ログインしました')


@client.event
async def on_ready():
    await greet()

#メッセージ受信時に実行される処理


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    #受信したメッセージが"hey"だったとき"hello"を返す
    if message.content.startswith('hey'):
        await message.channel.send('hello')

client.run(TOKEN)
