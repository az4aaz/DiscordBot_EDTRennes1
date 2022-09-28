import os
from dotenv import load_dotenv
import discord
from pprint import pprint
from discord.ext import commands
from scrappingEDT import EDTapi

# Import de la key du bot discord
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Initialisation du scrapper pour l'EDT
API=EDTapi()

# Autorisation du bot. Peuvent être modifiée (intents.{autorisation} = True)
intents = discord.Intents.default()
intents.message_content = True;

""" class Bot() {
    def __init__(self) :
        super
} """

# Initialise le bot avec sont préfixe de commande
bot = commands.Bot(command_prefix='/',intents=intents)

def getUserGroup(user) :
    groupe = None
    pprint(user.roles)
    if "A1" in [x.name for x in user.roles] :
        groupe = "2A1"
    elif "A2" in [x.name for x in user.roles] :
        groupe = "2A2"
    return groupe


# Evenement lors de la connexion du bot a Discord
@bot.event
async def on_ready():
    print(f'{bot.user.name} est connecté !') # Le print se fait dans la console côté serveur
    API.update_info();



# Définition de la commande de base permettant de retourner l'emploi du temps        
@bot.command(name='edt', help="Donne l'emploi du temps de la classe passée en paramètre pour un jour donné", pass_context=True)
async def start(ctx, date="Aujourd'hui", classe=None):
    if classe == None :
        groupe = getUserGroup(ctx.message.author) 
    else :
        groupe = classe
    if groupe == None :
        await ctx.channel.send("Tu n'as pas de rôle de classe. Tu peux préciser un groupe dans la commande (à la suite de /edt)")
    else :  
        API.update_info();
        edt = API.getEDT(groupe, date)

        await ctx.channel.send("**Emploi du temps {0}, Journée : {1}**".format(groupe,date))
        #pprint(edt)

        message = ">>> "
        for x in edt : 
            message += "**" + x[-1] + "**"
            if (len(x[-3])>5) :
                message += " - *" + x[-3] + "*"
            message += "\n"
            message += "**" + "="*(len(x[-1])-5) + "**\n"
            message += x[0] + " - " + x[1] +" | " + x[2]
            if (len(x[-2])>5) :
                message += "\n*" + x[-2] + "*"
            message += "\n\n"
            
        await ctx.channel.send(message)

bot.run(TOKEN)