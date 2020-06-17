import os,random,time
import discord,asyncio
from dotenv import load_dotenv

from discord.ext import commands
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
style.use("fivethirtyeight")

load_dotenv()
TOKEN = os.getenv('NzIyMDExMzA3MzAxMjczNjIz.Xuc_8A.wMJSM7Fc4Ic92ARqWxqRAM-p_DY')
client = discord.Client()

def community_report(guild):
    online = 0
    idle = 0
    offline = 0

    for m in guild.members:
        if str(m.status) == "online":
            online += 1
        if str(m.status) == "offline":
            offline += 1
        else:
            idle += 1

    return online, idle, offline

async def user_metrics_background_task():
    await client.wait_until_ready()
    global sentdex_guild
    sentdex_guild = client.get_guild(702966818398273679)

    while not client.is_closed():
        try:
            online, idle, offline = community_report(sentdex_guild)
            with open("usermetrics.csv", "a") as f:
                f.write(f"{int(time.time())},{online},{idle},{offline}\n")

            plt.clf()
            df = pd.read_csv("usermetrics.csv", names=['time', 'online', 'idle', 'offline'])
            df['date'] = pd.to_datetime(df['time'], unit='s')
            df['total'] = df['online'] + df['offline'] + df['idle']
            df.drop("time", 1, inplace=True)
            df.set_index("date", inplace=True)
            a  = df['online'] + df['idle']
            a.plot()
            plt.legend()
            plt.savefig("online.png")

            await asyncio.sleep(5)
        except Exception as e:
            print(str(e))
            await asyncio.sleep(5)


@client.event
async def on_message(message):
    bad_words = ["mall herif","sokuk", "göt", "amk","sikik","salak","döl israfı","manyak","amık","amk salağı","amınakoyum","amına koyam","orosbu","orosbu evladı","orosbu çocu","piç"]

    for word in bad_words:
        if message.content.count(word) > 0:
            await message.channel.purge(limit=1)
            await message.channel.send("Kötü kelime algılandı ve silindi!")


    if message.author == client.user:
        return

    elif "sa" == message.content.lower():
        msg = 'Aleyküm Selam yeğenim {0.author.mention}'.format(message)
        await message.channel.send(msg)

    elif "rapor ver" == message.content.lower():
        sentdex_guild = client.get_guild(702966818398273679)
        online, idle, offline = community_report(sentdex_guild)
        await message.channel.send(f"```Çevrimiçi: {online}.\nDiğer/Meşgul: {idle}.\nÇevrimdışı: {offline}```")

        file = discord.File("online.png", filename="online.png")
        await message.channel.send("online.png", file=file)

    elif message.content.startswith('link'):
        await message.channel.send("https://discord.gg/wpdnNgg")

    elif "instagram" and "insta" == message.content.lower():
        await message.channel.send("https://www.instagram.com/bybas55/?hl=tr")

    elif "twitch" == message.content.lower():
        await message.channel.send("https://www.twitch.tv/bybastv")


    elif message.content.startswith("!turnuva"):
        await message.channel.send("```BEYLER BİLGİLER #turnuva-bilgi  TAKIM BULMA #takım-bulma  KAYIT İSE #turnuva-kayıt KANALLARINA BAKIN !!!!```")

    elif message.content.startswith("kurallar"):
        await message.channel.send("""
        ```
        1 - Reklam Yapmak Ban Sebebidir.
        2 - Spam, Flood, Trol, Başkası Hakkında Konuşmak Yasaktır.
        3 - Level Atlamak İçin Gereksiz Spam Atmak Yasaktır. Leveliniz Bile Sıfırlanabilir.
        4 - Her Hangi Bir Şey Satmak Yasaktır.
        5 - Ses Kanallarında İnsanları Rahatsız Etmek Yasaktır.
        6 - Özel Harf İçeren Nickler Yasaktır. (Rahat anlaşılması bakımından.)
        7 - Özelden Reklam Yapanları Bizlere Bildirirseniz Reklam Yapanları SS Alarak Bizleri Bilgilendirebilirsiniz.
        8 - Küfür argo v.b kelimeler kullanmak kesinlikle yasaktır.

        Kurallarımıza Uymayan Kullanıcılar Öncelikle Uyarılır, Uyarılara Aldırış Etmeyenler Sunucumuzdan Banlanır.

        Sunucumuzda Bulunan Herkesin Kuralları Okumuş ve Kabul Etmiş Olarak Saymaktayız.
        ```""")

    elif message.content.startswith("komutlar"):
        embed = discord.Embed(title="GamingArea BOT Hk.", description="Bazı yararlı bot komutları.")
        embed.add_field(name="sa", value="Kullanıcıya merhaba der.")
        embed.add_field(name="link", value="Kanal linkini verir.")
        embed.add_field(name="rapor ver", value="Online/Offline kişi sayısı.")
        embed.add_field(name="kurallar", value="Sunucu kuralları.")
        embed.add_field(name="!turnuva",value="Turnuva hakkında bilgi verir.")
        embed.add_field(name="members", value="Sunucuda bulunan toplam kişi sayısını verir.")
        embed.add_field(name="twitch", value="Twitch kanal linkini verir.")
        embed.add_field(name="instagram",value="İnstagram hesap linkini verir.")

        await message.channel.send(content=None, embed=embed)

    elif "members" == message.content.lower():
        sentdex_guild = client.get_guild(702966818398273679)
        await message.channel.send(f"```Sunucumuzda toplam {sentdex_guild.member_count} kullanıcı bulunmaktadır.```")


@client.event
async def on_ready():
    print('Giriş yapıldı.')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.loop.create_task(user_metrics_background_task())
client.run("NzIyMDExMzA3MzAxMjczNjIz.Xuc_8A.wMJSM7Fc4Ic92ARqWxqRAM-p_DY")
