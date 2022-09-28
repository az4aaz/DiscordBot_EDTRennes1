from collections import OrderedDict
from icalendar import Calendar
import dateparser
from datetime import timedelta
import urllib.request
from pprint import pprint

class EDTapi():

    url = 'https://planning.univ-rennes1.fr/jsp/custom/modules/plannings/PnR6Bln8.shu'
    cours = {} # Dictionnaire qui stocke les tous les cours
    cours_trie = {} # Dictionnaire qui stocke les tous les cours mais trié

    def __init__(self):
        urllib.request.urlretrieve(self.url, 'ADECal.ics')

    # Merci stackOverflow :cry:
    # Permet d'applatir une liste de liste
    def flatten(self, liste):
        rt = []
        for i in liste:
            if isinstance(i, list):
                rt.extend(self.flatten(i))
            else:
                rt.append(i)
        return rt

        
        
    #Fonction qui met a jour les informations du bot
    def update_info(self) :

        urllib.request.urlretrieve(self.url, 'ADECal.ics') # Telechargement fichier iCal
        self.cours = {}
        self.cours_trie = {}
        #Importation du fichier iCal et création de la variable cours qui contients tous les evenements du fichier formatté
        g = open('ADECal.ics', 'rb')
        gcal = Calendar.from_ical(g.read())
        for component in gcal.walk():
            if component.name == "VEVENT":
                dt_start = str(component.get('dtstart').dt+timedelta(hours=2)) #DTSART : heure du début de l'évenement
                dt_end = str(component.get('dtend').dt+timedelta(hours=2))     #DTEND : heure de fin de l'évenement
                descr = str(component.get('description'))  #DESCRIPTION : déscription de l'évenement
                summa = str(component.get('summary'))      #SUMMARY : résumé de l'évenement
                loca = str(component.get('location'))      #LOCATION : endroit où se passe le cours

                if (dt_start[:-15] not in self.cours.keys()) :
                    self.cours[dt_start[:-15]] = []

                chaine_donnee = self.flatten(
                        [
                            (dt_start)[-14:-9], 
                            (dt_end)[-14:-9], # [-14:-9] récupère l'heure de début/fin
                            loca, 
                            [descr.split("\n")[x] 
                                for x in range(len(descr.split("\n"))) 
                                if descr.split("\n")[x]!=""
                            ][:-1],
                            summa
                        ]
                    )
                self.cours[dt_start[:-15]].append(chaine_donnee)

        for jour in self.cours.items() :
            self.cours_trie[jour[0]] = sorted(jour[1], key=lambda x: x[0])

        #pprint(self.cours_trie["2022-09-29"])
        g.close()

    def getEDT(self, classe , dateX):
        date = str(dateparser.parse(dateX, settings={'DATE_ORDER': 'DMY'}).date())
        #pprint(self.cours_trie[date])
        edtE = [x for x in self.cours_trie[date] if classe == x[3][:-2] or x[3] == "2A I" or "Amphi" in x[2] or "DS" in x[2]]
        return edtE

test = EDTapi()


# TODO  : recuperer les profs dans DESCR et le reste (a voir) dans summary
# TODO : ajouter id roles (auto classe)