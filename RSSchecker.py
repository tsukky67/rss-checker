import asyncio
import discord
import feedparser
import psycopg2
import nest_asyncio
nest_asyncio.apply()

TOKEN = "OTI3OTkzMzIzNDM0Njk2NzI0.YdSTIQ.BN72FbC3_SaYMkiGVH0Jr5e-9pY"
client = discord.Client()

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
    if message.content.startswith('/checkrss'):
        await check()
    if message.content.startswith('/delrss'):
        await message.channel.send("どのデータを削除しますか？数字を入力してください")
        con = connect()
        sql = """select * from  users WHERE channel_id = '""" + message.channel.id + "'"
        userlist = select_execute(con, sql) 
        for i in range(len(userlist)):
            await message.channel.send(i +":"+ userlist[i])
        mchannel = m.channel
        def delcheck(m):
            # メッセージが `おはよう` かつ メッセージを送信したチャンネルが
            # コマンドを打ったチャンネルという条件
            return 0 <= m.content <= len(userlist) and m.channel == mchannel

        try:
            msg = await client.wait_for('message', delcheck=delcheck, timeout=60)

        except asyncio.TimeoutError:
            await message.channel.send(f'時間切れです')

        else:
            def delete_execute(con, slq):
                with con.cursor() as cur:
                    cur.execute(sql)

                con.commit()

            if __name__ == '__main__':
                con = connect()

                sql = """delete
                            from users
                        where channnel_id = '"""+ userlist[message.channel.content]+"'"

                # データ削除
                delete_execute(con, sql)


client.run(TOKEN)