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


def select_execute(con, sql):
    with con.cursor() as cur:
        cur.execute(sql)
        rows = cur.fetchall()

        return rows


async def check():
    if __name__ == '__main__':
        con = connect()

        sql = 'select * from pages'

        res = select_execute(con, sql)
        for r in res:
            feed = feedparser.parse(r[0])
            title = feed.entries[0].title
            link = feed.entries[0].link

            def updatet_execute(con, slq):
                with con.cursor() as cur:
                    cur.execute(sql, (link, r[0]))

                con.commit()

            sql = """update pages set latest_link = %s WHERE url = %s"""

            updatet_execute(con, sql)

            sql = """select distinct from users where url = '""" + r[0] + """'"""

            res = select_execute(con, sql)

            channel = client.get_channel(int(res[0][0]))
            await channel.send(title+' '+link)


@client.event
async def on_ready():
    print('ログイン成功')
    await check()

@client.event
async def on_message(message):
    if message.content.startswith('/setrss'):  # コマンド指定
        cmd_serch = str(message.content)  # コマンドを文字列化
        url = cmd_serch[8:]
        try:
            feed = feedparser.parse(url)
            title = feed.entries[0].title
            link = feed.entries[0].link

        except IndexError:
            await message.channel.send("アクセスできなかったよ")

        else:
            if __name__ == '__main__':
                con = connect()

                def insert_execute(con, slq):
                  with con.cursor() as cur:
                    cur.execute(sql, (message.channel.id, url))
                  con.commit()
                sql = """insert into users(channel_id,url) values(%s,%s)"""

                insert_execute(con, sql)

                def insert_execute2(con, slq):
                    with con.cursor() as cur:
                        cur.execute(sql, (url, link))
                    con.commit()
                sql = """insert into pages(url,latest_link) values(%s,%s)"""

                insert_execute2(con, sql)

                await message.channel.send("多分できてるよ")
    # if message.content.startswith('/delrss'):
    if message.content.startswith('/checkrss'):
        await check()

client.run(TOKEN)