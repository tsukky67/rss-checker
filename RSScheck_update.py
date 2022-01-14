import os
import asyncio
import discord
import feedparser
import psycopg2
import nest_asyncio
import urllib.parse
nest_asyncio.apply()

TOKEN = os.environ['DISCORD_BOT_TOKEN']
client = discord.Client()


def connect():
    urllib.parse.uses_netloc.append("postgres")
    url = urllib.parse.urlparse(os.environ["DATABASE_URL"])
    con = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
                           
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

client.run(TOKEN)
