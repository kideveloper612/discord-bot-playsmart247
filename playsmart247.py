import requests
from bs4 import BeautifulSoup
import os
import discord
import dotenv


dotenv.load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


def get_request(param):
    headers = {
        'User-Agent': 'Mozila/5.0',
    }

    res = requests.request("GET", base_url, headers=headers, params=param)
    return res


def parse(content):
    return BeautifulSoup(content, 'html5lib')


def write(lines):
    lines.reverse()
    with open(file='result.txt', encoding='utf-8', mode='w') as file:
        for item in lines:
            file.write("%s\n" % item)


def main(pins):
    param = {
        'spins': pins
    }
    numbers = []
    response = get_request(param)
    soup = parse(response.text)
    options = soup.find_all('script')
    for option in options:
        script_txt = str(option.text)
        if '#new-datatable' in script_txt:
            results = script_txt.split('data:')[1].split('ordering:')[0].split(',')
            for result in results:
                content = result.replace('["', '').replace('"]', '').replace(']', '')
                content_soup = BeautifulSoup(content)
                number_soup = content_soup.find(attrs={'class': 'num'})
                if number_soup is not None:
                    number = number_soup.text.strip()
                    numbers.append(number)
    write(lines=numbers)


if __name__ == '__main__':
    base_url = 'https://playsmart247.com/auto-roulette'
    client = discord.Client()

    @client.event
    async def on_ready():
        print(f'{client.user.name} has connected to Discord!')

    @client.event
    async def on_member_join(member):
        await member.create_dm()
        await member.dm_channel.send(
            f'Hi {member.name}, welcome to my Discord server!'
        )

    @client.event
    async def on_message(message):

        print('{} requested to scrape'.format(message.author))
        if message.author == client.user:
            return

        if '.help' in message.content:
             await message.channel.send("""
                 Pour m'utiliser, c'est tres simple : 
                - Si vous rechercher 250 entrer:
                .send 250 spin
                
                - Si vous rechercher 25000 spin enter: 
                .send 2500 spin""")

        if '.send 250 spin' in message.content:
            main(pins=250)
            await message.channel.send(" Un moment je scan pour vous la table bleu ")
            await message.channel.send(file=discord.File('result.txt'))
        elif '.send 2500 spin' in message.content:
            main(pins=2500)
            await message.channel.send(" Un moment je scan pour vous la table bleu ")
            await message.channel.send(file=discord.File('result.txt'))

        elif message.content == 'raise-exception':
            raise discord.DiscordException

    client.run(TOKEN)
