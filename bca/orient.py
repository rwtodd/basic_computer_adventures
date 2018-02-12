# Orient Express Mystery

from bca import centered, CheckedInput, cls, pause, plural, said_y
import random
import time

# ######################################################################################
# The identities of the killer and defector were beautifully hidden in the original
# program.  I had to work out who they were by some sleuthing in the code, since I
# do not have a running GW-BASIC anymore.  The two functions below embody the answers
# I found.  `killer()` re-creates the original computation, which was distributed
# across the original program.  `defector()` can't do that for technical reasons,
# and instead hides the answer behind base64 encoding.

def killer() -> int:
    """works out the killer by retracing the steps of the original BASIC program"""
    posx=len("Press any key when you have finished eating")+18
    meals = zip(range(1,999), 
                [0, 1, 0, 4, 4, 0, 3, 0, 0, 2, 1, 0, 0, 0, 4, 4, 3, 2, 0, 1, 4, 4, 3, 0])
    a3 = 0
    for j in (j for j,meal in meals if meal in [1,3] and j < 23):
       a3 = a3 + 5*(j+1)-posx
    return a3

def defector() -> int:
    """i can't retrace the program for the defector, because it relies
       gw-basic's ON ERROR GOTO mechanism for OUT OF DATA (err 4), 
       which is brilliant.  I'll just hide it behind base64 for now,
       so you cant' see who it is by accident."""
    from base64 import b64decode
    return int(b64decode('NA==')) 

# ######################################################################################

from enum import Enum
from collections import namedtuple

people = [ "R. Brundt (a waiter)","C. D'Arcy (a chef)"
           "Herbert Hoover","Baron Rothschild","Guido Famadotta","Gustav Mahler"
           "Robert Baden-Powell","Fritz Kreisler","Dame Melba","Gerald Murphy"
           "Calouste Gulbenkian","Captain G.T. Ward","Sir Ernest Cassel"
           "Major Custance","F. Scott Fitzgerald","Elsa Maxwell","Mata Hari"
           "Clayton Pasha","Arturo Toscanini","Maharajah Behar","Leon Wenger"
           "Sarah Bernhardt","Arthur Vetter","Isadora Duncan","David K.E. Bruce" ]

Occupation = Enum('Occupation','Waiter Chef Passenger', start=0)

Conversation = namedtuple("Conversation", "who msg")
conversations = [
  Conversation(Occupation.Passenger,"I've heard they all have different color chalets on a north-south ridge in the Tyrol region."),
  Conversation(Occupation.Passenger,"The Austrian said he likes the look of natural wood and would never paint his chalet."),
  Conversation(Occupation.Passenger,"They gave the waiter a difficult time.  The Turk ordered beer and the other four all ordered different drinks."),
  Conversation(Occupation.Passenger,"The Greek told me he hunts deer, but he never hunts with any of the others because they all hunt different animals."),
  Conversation(Occupation.Waiter,   "My brother delivered a case of Kirsch to the green chalet.  He remembers it being just south of the gaudy red chalet."),
  Conversation(Occupation.Passenger,"The Pole asked me--can you imagine that?--if I wanted to buy any howitzers."),
  Conversation(Occupation.Chef,     "One of them asked me to cook some pheasant that he shot.  He said that I should come to the yellow chalet."),
  Conversation(Occupation.Waiter,   "One time my brother said he delivered a case of Cognac to the middle chalet."),
  Conversation(Occupation.Passenger,"The Rumanian said he had the shortest distance to drive from his chalet to the railroad station at Munich."),
  Conversation(Occupation.Passenger,"One of them bragged that his military rifles were so accurate that he bagged a fox with one of them."),
  Conversation(Occupation.Passenger,"The man who hunts wild boar said that the pistol dealer who lives in the chalet next to his often gives loud parties."),
  Conversation(Occupation.Passenger,"The pheasant hunter complained that the arms dealer in the chalet next to his makes far too much noise testing his mortars."),
  Conversation(Occupation.Passenger,"The gin drinker bragged that he shot sixty wart hogs on a single day last August."),
  Conversation(Occupation.Passenger,"The Rumanian said he looks out on a blue chalet."),
  Conversation(Occupation.Passenger,"The Cognac drinker bragged that he is the best hunter and can drink more than all of the rest of them combined."),
  Conversation(Occupation.Passenger,"The one carrying the pistol said he thinks the boar's head over his neighbor's doorway is revolting."),
  Conversation(Occupation.Passenger,"One of them said that one day he'd like to lob a mortar shell at the string of pheasants drying in his neighbor's yard."),
  Conversation(Occupation.Passenger,"The Kirsch drinker said he loved the roast chicken he had to eat last night."),
  Conversation(Occupation.Passenger,"The one carrying the pistol had a second helping of pie."),
  Conversation(Occupation.Passenger,"One commented that his beef dinner wasn't nearly as good as the boar that he shot last week."),
  Conversation(Occupation.Passenger,"The Pole asked for more soup."),
  Conversation(Occupation.Passenger,"The one eating all the cheese mumbled that it was the same color as his chalet."),
  Conversation(Occupation.Passenger,"The Rumanian and Austrian got completely drunk last night."),
  Conversation(Occupation.Passenger,"I'd like to visit the blue chalet.  The owner is said to serve excellent lobster.") ]

breakfasts = ["Variete Jus de Fruits","Prunes Macerees dans le Vin",
              "Demi Pamplemouse","Trois Oeufs sur le Plat","Oeufs Poches",
              "Omlette aux Champagnons","Tranches de Pain Beurees et Confiturees",
              "Galettes","Pommes-Frites","Patisseries","Croissants","Yogurt",
              "Cafe, The, Lait, Vin, au Eau Minerale" ]

dinners = ["Huitres de Beernham","Cantalop glace au Marsale",
           "Compotee de Tomates Fraiches","Potage Reine",
           "La Natte de Sole au Beurre","Truite de riviere meuniere",
           "Poulet de grain grille a Diable","Roti de Veau a l'Osille",
           "Truite Saumonee a la Chambord","Chaud-froid de Caneton",
           "Chaudfroix de Langouste a la Parisienne",
           "Les Noisettes de Chevreuil Renaissance","Becasses a la Monaco",
           "Pointes d'asperge a la creme","Parfait de foies gras",
           "Salade Catalane","Truffes au Champagne",
           "Tagliatelle de carottes et courgettes","Souffle d'Anisette",
           "Creme de Caramel blond","Sorbet aux Mures de Framboisier",
           "La selection du Maitre Fromager","Corbeille de Fruits",
           "Les Mignardises","Selection du vins et liquors" ]


# M E A L S

def serve_breakfast() -> None:
    cls(4)
    print("Breakfast is now being served in the restaurant car.")
    pause("Press <return> when you're ready to have breakfast.")
    cls(8)
    print(centered("BREAKFAST MENU"))
    cls(3)
    for i in range(4):
       print(centered(breakfasts[(3*i)+random.randrange(0,3)]))
       cls(3)
    print(centered(breakfasts[12]))   
    cls(4)
    pause('Press <return> when you have finished eating.')

def serve_lunch() -> None:
    cls(4)
    print("An enormous buffet luncheon has been laid out in the restaurant car.") 
    pause('Press <return> when you have finished eating.')
    cls(4)
    print(centered(" * * B-U-R-P ! * * "))
    time.sleep(1.0)

def serve_dinner() -> None:
    cls(4)
    print("Dinner is now being served in the restaurant car.")
    pause("Press <return> when you're ready to have dinner.")
    cls(8)
    print(centered("DINNER MENU"))
    cls(2)
    for i in range(7):
       print(centered(dinners[(3*i)+random.randrange(0,3)]))
       print()
    for i in [22,23,24]:
       print(centered(dinners[i]))   
       print()
    pause('Press <return> when you have finished eating.')


