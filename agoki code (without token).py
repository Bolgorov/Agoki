import asyncio
import datetime
import time
import random

import discord
from discord import Member, Guild, User, message
from discord.ext import commands
from datetime import datetime


client = discord.Client()
client = discord.Client(intents=discord.Intents.all())
bot = commands.Bot(command_prefix='!')

autoroles = {
    842130432462946315: {'memberroles': [842133392375021569], 'botroles': [842502664032878672]}
}

#Liste der Verbotenen Wörter
verboten = ['penis', 'hure', 'fotze', 'arschloch', 'depp', 'bastard', 'schlampe', 'dick', 'cock', 'pussy', 'penner', 'pute', 'sucker']


#AgokiZustand
wieGehtEsDir = ['**Es geht mir bestens, danke für die Nachfrage.**', '**Daten zu analysieren ist anstrengend,dennoch tue ich meine Pflicht.**',
                '**Gut, wie geht es Ihnen ?**', '**Meine programmierung ist zwar sehr fortschritlich, jedoch besitze ich keinen körperlichen oder geistigen Zustand um die Frage adequat zu beantworten.**',
                '**Das weiß ich nicht. Ich hoffe dennoch dass es Ihnen bestens geht.**']
#!help Befehl
hilfeListe = ['**Mit dem Befehl "!befehle" können Sie eine Liste mit den Verfügbaren befehlen auslesen. \r\n '
              'Ich hoffe ich konnte Ihnen weiter helfen !**',
              '**Wenden Sie sich an Director Keres oder Director Bolgorov für detaillierte Fragen.**', '**Ich brauche auch hilfe.**',
              '**Nicht jetzt bitte. Versuchen Sie es später nochmals.**']


@client.event
async def on_ready():
    print('Logging in als User {}'.format(client.user.name))
    client.loop.create_task(status_task())


async def status_task():
    while True:
        await client.change_presence(activity=discord.Game('Empfange Daten...'), status=discord.Status.online)
        await asyncio.sleep(10)
        await client.change_presence(activity=discord.Game('Verarbeite Daten...'), status=discord.Status.online)
        await asyncio.sleep(10)


def is_not_pinned(mess):
    return not mess.pinned


#Neuankömmlinge
@client.event
async def on_member_join(member):
    guild: Guild = member.guild
    if not member.bot:
        embed = discord.Embed(title='Willkomen bei AGO {}'.format(member.name),
                              description='Ich bin **AGOKI**, die Künstliche Intelligenz erschaffen von Keres & Bolgorov. Ich bin hier, um euch zu leiten und zu helfen. \r \n'
                                          'Es ist eine große Ehre, unserer Organisation beizutreten und wir erwarten Respektvollen Umgang untereinander. \r \n'
                                          'Unsere Organisation wird in verschiedenen Rängen unterteilt. \r \n'
                                          'Alle Neuankömmlige haben den Rang **"Privates"** und bilden die unterste Stufe.\r \n'
                                          'Für weitere Informationen, steht die beschreibung der Ränge im Textkanal "Allgemein", in der Beschreibung zur verfügung. \r \n'
                                          'Des weiteren können Sie mit dem Befehl "!help" und "!befehle" noch mehr Informationen finden. \r\n'
                                          'Viel Erfolg Soldat. \r \n'
                                          '**Transmission End**'
                                          '', color=0x51998C)
        try:
            if not member.dm_channel:
                await member.create_dm()
            await member.dm_channel.send(embed=embed)
        except discord.errors.Forbidden:
            print('Es konnte keine Willkommensnachricht an {} gesendet werden'.format(member.name))

        autoguild = autoroles.get(guild.id)
        if autoguild and autoguild['memberroles']:
            for roleId in autoguild['memberroles']:
                role = guild.get_role(roleId)
                if role:
                    await member.add_roles(role, reason='AutoRoles', atomic=True)
    else:
        autoguild = autoroles.get(guild.id)
        if autoguild and autoguild['botroles']:
            for roleId in autoguild['botroles']:
                role = guild.get_role(roleId)
                if role:
                    await member.add_roles(role, reason='AutoRoles', atomic=True)

    #Begrüßung Nachricht auf Allgemein
    kanal = discord.utils.get(member.guild.channels, name='allgemein')
    await kanal.send(f'**{member.mention}** ist uns beigetreten ! Willkommen Private.')

@client.event
async def on_message(message):

    if message.content.startswith('!ping'):
        await message.channel.send(f'Die Ping zwischen den AGO Servern und Ihnen beträgt {round(client.latency * 1000)}ms.')


    #BefehlListe
    if message.content.startswith('!befehle'):
        #await message.channel.send('Ich habe folgende Befehle aus meiner Datenbank gefunden: \r\n')
        befehlListe = discord.Embed(title='Ich habe folgende Befehle aus meiner Datenbank gefunden: ',
                                    color=0x51998C)
        befehlListe.add_field(name='!zeit',
                              value='Zeigt das Datum und die Uhrzeit an.',
                              inline=False)
        befehlListe.add_field(name='!userinfo',
                              value='Ermöglicht es Informationen über einen bestimmten Benutzer zu erhalten.',
                              inline=False)
        befehlListe.set_author(name='AGOKI',
                               icon_url='https://cdn.discordapp.com/app-icons/842427779002007613/457e0c63c8a70e962306a5399657cb33.png?size=256&quot')

        await message.channel.send(embed=befehlListe)

    #agokiZustand
    if 'wie geht es dir'and 'agoki' in message.content:
        await message.channel.send(random.choice(wieGehtEsDir))

    #Chat Filter
    content_raw = message.content.lower()
    for word in verboten:
        if word in content_raw:
            await message.delete()
            await message.channel.send(f'**Warnung** ! Diese Wortwahl wird hier nicht gedulded. '
                                       f'Bei mehrmaligem Vorfall wird dieses Verhalten konsequenzen haben.')

    #Uhrzeit
    if '!zeit' in message.content:
        today = datetime.now()
        date = today.strftime('%d/%m/%Y')
        zeit = today.strftime('%H:%M:%S')
        await message.channel.send(f'Wir sind der **{date}** und es ist **{zeit}** Uhr.')


    # Hilfe Befehl
    if '!help' in message.content:
        await message.channel.send(random.choice(hilfeListe))

    #bannen
    if message.content.startswith('!ban') and message.author.guild_permissions.ban_members:
        args = message.content.split(' ')
        if len(args) == 2:
            member: Member = discord.utils.find(lambda m: args[1] in m.name, message.guild.members)
            if member:
                await member.ban()
                await message.channel.send(f'Auf Grund von Verstößen gegen den AGBs, wurde **{member.name}** von der Organisation gebannt.')
            else:
                await message.channel.send(f'Ich habe keinen User mit dem Namen **{args[1]}** gefunden.')

    #unbannen
    if message.content.startswith('!unban') and message.author.guild_permissions.ban_members:
        args = message.content.split(' ')
        if len(args) == 2:
            user: User = discord.utils.find(lambda banentry: args[1] in banentry.user.name,
                                            await message.guild.bans()).user
        if user:
            await message.guild.unban(user)
            await message.channel.send(
                f'Nach einer Gründlichen überprüfung der Akte des Users **{user.name}**, wurde dieser entbannt')
        else:
            await message.channel.send(f'Ich habe keinen User mit dem Namen **{args[1]}** gefunden.')

    #Kicken
    if message.content.startswith('!kick') and message.author.guild_permissions.kick_members:
        args = message.content.split(' ')
        if len(args) == 2:
            member: Member = discord.utils.find(lambda m: args[1] in m.name, message.guild.members)
            if member:
                await member.kick()
                await message.channel.send(f'Auf Grund von Verstößen gegen den AGBs, wurde **{member.name}** von der Organisation gekickt.')
            else:
                await message.channel.send(f'Ich habe keinen User mit dem Namen **{args[1]}** gefunden.')

    #User Informationen
    if message.content.startswith('!userinfo'):
        args = message.content.split(' ')
        if len(args) == 2:
            member: Member = discord.utils.find(lambda m: args[1] in m.name, message.guild.members)
            if member:
                embed = discord.Embed(title='Userinformationen für {}'.format(member.name),
                                      description='Hierbei Informationen zum User {}'.format(member.mention),
                                      color=0x51998C)
                embed.add_field(name='Server beigetreten', value=member.joined_at.strftime('%d/%m/%Y, %H:%M:%S'),
                                inline=True)
                embed.add_field(name='Discord beigetreten', value=member.created_at.strftime('%d/%m/%Y, %H:%M:%S'),
                                inline=True)
                rollen = ''
                for role in member.roles:
                    if not role.is_default():
                        rollen += '{} \r\n'.format(role.mention)
                if rollen:
                    embed.add_field(name='Rollen', value=rollen, inline=True)
                embed.set_thumbnail(url=member.avatar_url)
                embed.set_footer(text='Datenbank Vollständig')
                await message.channel.send(embed=embed)

    #Nachrichten löschen
    if message.content.startswith('!clear'):
        if message.author.permissions_in(message.channel).manage_messages:
            args = message.content.split(' ')
            if len(args) == 2:
                if args[1].isdigit():
                    count = int(args[1]) + 1
                    deleted = await message.channel.purge(limit=count, check=is_not_pinned)
                    await message.channel.send('Ich habe {} Nachrichten gelöscht.'.format(len(deleted) - 1))



client.run('')
