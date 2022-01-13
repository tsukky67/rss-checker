import os
import asyncio
import discord
import feedparser
import psycopg2
import nest_asyncio
nest_asyncio.apply()

TOKEN = os.environ['DISCORD_BOT_TOKEN']
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


def delete_execute(con, slq):
                with con.cursor() as cur:
                    cur.execute(slq)

                con.commit()


async def check():
    if __name__ == '__main__':
        con = connect()

        sql = 'select distinct url,latest_link from pages'

        res = select_execute(con, sql)

        for r in res:
            feed = feedparser.parse(r[0])
            title = feed.entries[0].title
            link = feed.entries[0].link

            def updatet_execute(con, slq):
                with con.cursor() as cur:
                    cur.execute(sql, (link, r[0]))

                con.commit()

            sql = """select * from pages where url = '""" + r[0] + """'"""
            
            page = select_execute(con, sql)
        
            if  page[0][1] != link:

                sql = """update pages set latest_link = %s WHERE url = %s"""

                updatet_execute(con, sql)

                sql = """select distinct channel_id,url from users where url = '""" + r[0] + """'"""

                res1 = select_execute(con, sql)

                if res1 == []:
                    if __name__ == '__main__':
                        sql = """delete
                                from pages
                                    where url = '""" + r[0] + "'"
                    delete_execute(con, sql)

                else:
                    channel = client.get_channel(int(res1[0][0]))
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
            await message.channel.send("正しいRSSリンクを入力してください")

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

                await message.channel.send("登録が完了しました")

    if message.content.startswith('/checkrss'):
        con = connect()
        sql = """select distinct channel_id,url from users where channel_id = '""" + str(message.channel.id) + """'"""
        res = select_execute(con, sql)
        for r in res:
            feed = feedparser.parse(r[1])
            title = feed.entries[0].title
            link = feed.entries[0].link

            await message.channel.send(title+' '+link)

    if message.content.startswith('/delrss'):
        await message.channel.send("どのデータを削除しますか？数字を入力してください")
        con = connect()
        sql = """select * from  users WHERE channel_id = '""" + str(message.channel.id) + "'"
        userlist = select_execute(con, sql)
        for i in range(len(userlist)):
            await message.channel.send(str(i) + ":" + str(userlist[i][1]))
        mchannel = message.channel

        def check(m):
            # メッセージが `おはよう` かつ メッセージを送信したチャンネルが
            # コマンドを打ったチャンネルという条件
            return 0 <= int(m.content) <= len(userlist) and m.channel == mchannel

        try:
            msg = await client.wait_for('message', check=check, timeout=60)
        except asyncio.TimeoutError:
            await message.channel.send(f'時間切れです')

        else:
            if __name__ == '__main__':
                con = connect()
                sql = """delete
                            from users
                              where url = '""" + userlist[int(msg.content)][1]+"'"
                # データ削除
                delete_execute(con, sql)
            await message.channel.send("削除が終了しました")
client.run(TOKEN)
