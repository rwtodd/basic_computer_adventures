# Orient Express Mystery

from bca import centered, CheckedInput, cls, pause, plural, said_y
import random
import time
from enum import Enum
from collections import namedtuple

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

# ######################################################################################
# MEALS

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
# ######################################################################################

# ######################################################################################
# Game State
class GameState:
    def __init__(self):
        self.segment  = None        # which segment of the trip are we on? 
        self.derailed = False       # have we derailed yet?
        self.bandits  = False       # have bandits attacked?
        self.hazard_delay = 0       # days delayed by hazards

# ######################################################################################


# ######################################################################################
# Hazards

def snow(gs: GameState) -> None:
    x = random.random()
    if x > 0.65: return   # 65% chance of snow
    cls(4)
    print("It is snowing heavily ", end='') 
    if x > 0.01:
        print("but the tracks have been cleared and the train")
        print("will not be delayed.")
    else:       
        print("and the train is forced to slow down.")
        print()
        print("Oh no!  The train is coming to a stop.  Let's hope this is")
        print("not a repeat of the trip of January 29, 1929 when the Orient")
        print("Express was stuck in snowdrifts for five days.")
        print()
        time.sleep(1.0)
        print("But it looks like it is!")
        time.sleep(1.0)
        print()
        gs.hazard_delay += 2 
        print("You are stranded for two days until a snowplow clears the track.")
        print(f"The train is now exactly {gs.hazard_delay} days behind schedule.")

def bandits(gs: GameState) -> None:
    if gs.bandits or (random.random() > 0.04): return    # 4% chance of bandits
    gs.bandits = True
    cls(4)
    print(centered(" * * CLANG! * *"))    
    time.sleep(1.0)
    cls(4)
    print("You are rudely awakened from a deep sleep by a loud noise")
    print("as the train jerks to a halt.")
    time.sleep(1.0) 
    print()
    print("You are shocked to see a bandit waving a gun in your face.")
    print("He demands you give him your wallet, jewelry, and watch.")
    time.sleep(1.0) 
    print()
    print("The bandits are off the train in a few moments with")
    print("their loot.  They disappear into the forest.  No one")
    print("was injured, and the train resumes its journey.")

def derail(gs: GameState) -> None:
    if gs.derailed or (random.random() > 0.02): return  # 2% chance of derailment
    gs.derailed = True
    gs.hazard_delay += 1
    cls(4)
    print(centered(" * * SCREEECH! * *"))
    time.sleep(1.0)
    cls(2)
    print("You hear a loud screeching noise as the train comes to a")
    print("crashing stop.  The engine, tender, and first coach are")
    print("leaning at a crazy angle.  People are screaming." )
    time.sleep(1.0)
    print()
    print("While not as bad as the derailment at Vitry-le-Francois in")
    print("November 1911, there is no question that the front of the")
    print("train has left the track." )
    time.sleep(1.0)
    print()
    print("You are stranded for exactly one day while the track is")
    print("repaired and a new locomotive obtained." )
    print()
    print(f"The train is now exactly {gs.hazard_delay} days behind schedule.")

# ######################################################################################


# ######################################################################################
# Trip Data (segments, conversations, etc.)

TimeFrame = Enum("TimeFrame", "Early Breakfast Lunch Dinner Night", start=0)
HazardType = Enum("HazardType", "Snow Bandits No", start=0) 

Segment = namedtuple("Segment", "tf nconv ht day tarrive tdepart city country")
segments = [Segment(TimeFrame.Early,    0,HazardType.No     ,1,   0,1430,"London","England"),
            Segment(TimeFrame.Breakfast,2,HazardType.No     ,1,1855,1919,"Calais","France"),
            Segment(TimeFrame.Early,    1,HazardType.No     ,1,2233,2253,"Paris (Nord)","France"),
            Segment(TimeFrame.Night,    0,HazardType.No     ,1,2316,2350,"Paris (Lyon)","France"),
            Segment(TimeFrame.Night,    0,HazardType.Snow   ,2, 600, 620,"Vallorbe","Switzerland"),
            Segment(TimeFrame.Early,    1,HazardType.No     ,2, 700, 707,"Lausanne","Switzerland"),
            Segment(TimeFrame.Dinner,   1,HazardType.Snow   ,2, 732, 734,"Montreux","Switzerland"),
            Segment(TimeFrame.Early,    1,HazardType.Snow   ,2, 919, 927,"Brig","Switzerland"),
            Segment(TimeFrame.Early,    3,HazardType.No     ,2,1005,1025,"Domodossola","Italy"),
            Segment(TimeFrame.Lunch,    2,HazardType.No     ,2,1223,1320,"Milan","Italy"),
            Segment(TimeFrame.Breakfast,2,HazardType.No     ,2,1705,1730,"Venice (S. Lucia)","Italy"),
            Segment(TimeFrame.Early,    1,HazardType.No     ,2,1954,2014,"Trieste","(Free State)"),
            Segment(TimeFrame.Early,    1,HazardType.No     ,2,2044,2110,"Opicina","Italy"),
            Segment(TimeFrame.Early,    2,HazardType.No     ,2,2119,2225,"Sezana","Slovenia"),
            Segment(TimeFrame.Night,    0,HazardType.No     ,3,  21, 107,"Ljubljana","Slovenia"),
            Segment(TimeFrame.Night,    0,HazardType.No     ,3, 310, 330,"Zagreb","Croatia"),
            Segment(TimeFrame.Dinner,   2,HazardType.No     ,3, 900, 956,"Belgrade","Serbia"),
            Segment(TimeFrame.Lunch,    1,HazardType.No     ,3,1334,1356,"Crveni Krst","Serbia"),
            Segment(TimeFrame.Early,    2,HazardType.No     ,3,1555,1634,"Caribrod","Serbia"),
            Segment(TimeFrame.Breakfast,2,HazardType.No     ,3,1856,1935,"Sofia","Bulgaria"),
            Segment(TimeFrame.Night,    0,HazardType.Bandits,4,  45, 120,"Svilengrad","Bulgaria"),
            Segment(TimeFrame.Night,    0,HazardType.Bandits,4, 406, 445,"Pithion","Greece"),
            Segment(TimeFrame.Dinner,   0,HazardType.No     ,4, 505, 545,"Uzunkopru","Turkey"),
            Segment(TimeFrame.Early,    0,HazardType.No     ,4,1230,   0,"Constantinople","Turkey") ]

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


# ######################################################################################
# The Game Logic
title = """


                       The Orient Express, 1923


                      (c) by David H. Ahl, 1986 



"""

scenario = """
                       The Mysterious Arms Deal

        It is February 1923.  The following note is received at
   Whitehall: 'If you will furnish me with a new identity and a
   lifetime supply of Scotch, I will give up my life of arms dealing
   and will provide you with much valuable information.  I will be
   on the Orient Express tonight.  But you must contact me before
   the train reaches Uzunkopru or that swine dealer of Maxim machine
   guns will have me killed by bandits like he did to Baron Wunster
   last month.'  The note is not signed.
        You, a British agent, are assigned to take the train, rescue
   the defector, and arrest the killer.
        You know there are five notorious arms dealers of different
   nationalities operating in Europe under an uneasy truce as each
   deals in a different kind of weapon.  But it is obvious that the
   truce has ended.


"""

def run_hazards(gs: GameState) -> None:
    """On some days we have snow or bandits...and any day we could derail"""
    if gs.segment.ht != HazardType.No:
        [snow,bandits][gs.segment.ht.value](gs)
    derail(gs)

def intro() -> None:
    cls()
    print(title)
    pause()
    print(scenario)
    pause("Press <return> to call a taxi...") 

def run_game() -> None:
    gs = GameState()
    random.shuffle(conversations)
    intro()
    for j,seg in zip(range(1,25),segments):
        gs.segment = seg 
        cls(4)
        print(centered(f'Segment {j}'))
        cls(2)
        run_hazards(gs)
        time.sleep(1.0)

if __name__ == "__main__":
    while True:
        run_game()
        cls(3)
        if not said_y('Would you like to play again? '):
            break

