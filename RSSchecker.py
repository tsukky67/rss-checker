import discord
import feedparser
import psycopg2
import nest_asyncio
nest_asyncio.apply()

TOKEN = "OTI3OTkzMzIzNDM0Njk2NzI0.YdSTIQ.BN72FbC3_SaYMkiGVH0Jr5e-9pY"
client = discord.Client()

#bot起動完了時に実行される処理

CHANNEL_ID = 927990496813539361


def connect():
    con = psycopg2.connect("host=" + "ec2-34-226-134-154.compute-1.amazonaws.com" +
                           " port=" + "5432" +
                           " dbname=" + "dhk84rh4qge1r" +
                           " user=" + "fpftzugpxpxnol" +
                           " password=" + "9367ccbf29a56fc3fd472fc57bf54841f6feadb6aaac62bad4ff0557fd618f0d")

    return con

if __name__ == '__main__':
    con = connect()


async def check():
    url = 'https://feed43.com/6143843436874854.xml'  # rssのアドレス
    feed = feedparser.parse(url)
    title = feed.entries[0].title
    link = feed.entries[0].link

    await channel.send(title+' '+link)


@client.event
async def on_ready():
    print('ログイン成功')
    await check()


#メッセージ受信時に実行される処理



@client.event
async def on_message(message):
    if message.content.startswith('/setrss'):  # コマンド指定
        cmd_search = str(message.content)  # コマンドを文字列化
        name = cmd_search[6:]  # 文字列化したコマンドからチャンネル名を抽出
        
        def insert_execute(con, slq):
            with con.cursor() as cur:
                cur.execute(sql, (message.channnel.id, name))

            con.commit()
        if __name__ == '__main__':
            con = connect()
            sql = """insert into pages(id,name) values(%s,%s)"""
            insert_execute(con, sql)

    await message.channel.send("多分できてる")

client.run(TOKEN)
