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
# I found.  `defector` re-creates the original computation, which was distributed
# across the original program.  `killer()` can't do that for technical reasons,
# and instead hides the answer behind base64 encoding.

def defector() -> int:
    """works out the defector by retracing the steps of the original BASIC program"""
    posx=len("Press any key when you have finished eating")+18
    meals = enumerate([0, 1, 0, 4, 4, 0, 3, 0, 0, 2, 1, 0, 0, 0, 4, 4, 3, 2, 0, 1, 4, 4, 3, 0], 1)
    a3 = 0
    for j in (j for j,meal in meals if meal in [1,3] and j < 23):
       a3 = a3 + 5*(j+1)-posx
    return a3

def killer() -> int:
    """i can't retrace the program for the killer, because it relies
       gw-basic's ON ERROR GOTO mechanism for OUT OF DATA, 
       which is brilliant.  I'll just hide it behind base64 for now,
       so you can't see who it is by accident."""
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
        self.conversations = random.sample(conversations,len(conversations))  
        self.my_defector = None     # player choice
        self.my_killer = None       # player choice
        self.perfection = False     # did you get everything right?
        self.alive = True           # are we alive?

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
    cls(2)
    pause()

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
    ring_doorbell()
    print()
    print("You are shocked to see a bandit waving a gun in your face.")
    print("He demands you give him your wallet, jewelry, and watch.")
    time.sleep(1.0) 
    print()
    print("The bandits are off the train in a few moments with")
    print("their loot.  They disappear into the forest.  No one")
    print("was injured, and the train resumes its journey.")
    cls(3)
    pause()

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
    print(f"The train is now exactly {plural(gs.hazard_delay,'day')} behind schedule.")
    print()
    pause()

# ######################################################################################


# ######################################################################################
# Trip Data (segments, conversations, etc.)

class TimeFrame(Enum):  # mypy doesn't like the functional form, so write out the class
  Early = 0,
  Breakfast = 1, 
  Lunch = 2,
  Dinner = 3,
  Night = 4

Segment = namedtuple("Segment", "tf nconv ht day tarrive tdepart city country")
segments = [Segment(TimeFrame.Early,    0,None   ,1,   0,1430,"London","England"),
            Segment(TimeFrame.Breakfast,2,None   ,1,1855,1919,"Calais","France"),
            Segment(TimeFrame.Early,    1,None   ,1,2233,2253,"Paris (Nord)","France"),
            Segment(TimeFrame.Night,    0,None   ,1,2316,2350,"Paris (Lyon)","France"),
            Segment(TimeFrame.Night,    0,snow   ,2, 600, 620,"Vallorbe","Switzerland"),
            Segment(TimeFrame.Early,    1,None   ,2, 700, 707,"Lausanne","Switzerland"),
            Segment(TimeFrame.Dinner,   1,snow   ,2, 732, 734,"Montreux","Switzerland"),
            Segment(TimeFrame.Early,    1,snow   ,2, 919, 927,"Brig","Switzerland"),
            Segment(TimeFrame.Early,    3,None   ,2,1005,1025,"Domodossola","Italy"),
            Segment(TimeFrame.Lunch,    2,None   ,2,1223,1320,"Milan","Italy"),
            Segment(TimeFrame.Breakfast,2,None   ,2,1705,1730,"Venice (S. Lucia)","Italy"),
            Segment(TimeFrame.Early,    1,None   ,2,1954,2014,"Trieste","(Free State)"),
            Segment(TimeFrame.Early,    1,None   ,2,2044,2110,"Opicina","Italy"),
            Segment(TimeFrame.Early,    2,None   ,2,2119,2225,"Sezana","Slovenia"),
            Segment(TimeFrame.Night,    0,None   ,3,  21, 107,"Ljubljana","Slovenia"),
            Segment(TimeFrame.Night,    0,None   ,3, 310, 330,"Zagreb","Croatia"),
            Segment(TimeFrame.Dinner,   2,None   ,3, 900, 956,"Belgrade","Serbia"),
            Segment(TimeFrame.Lunch,    1,None   ,3,1334,1356,"Crveni Krst","Serbia"),
            Segment(TimeFrame.Early,    2,None   ,3,1555,1634,"Caribrod","Serbia"),
            Segment(TimeFrame.Breakfast,2,None   ,3,1856,1935,"Sofia","Bulgaria"),
            Segment(TimeFrame.Night,    0,bandits,4,  45, 120,"Svilengrad","Bulgaria"),
            Segment(TimeFrame.Night,    0,bandits,4, 406, 445,"Pithion","Greece"),
            Segment(TimeFrame.Dinner,   0,None   ,4, 505, 545,"Uzunkopru","Turkey"),
            Segment(TimeFrame.Early,    0,None   ,4,1230,   0,"Constantinople","Turkey") ]

people = [ "R. Brundt (a waiter)","C. D'Arcy (a chef)",
           "Herbert Hoover","Baron Rothschild","Guido Famadotta","Gustav Mahler",
           "Robert Baden-Powell","Fritz Kreisler","Dame Melba","Gerald Murphy",
           "Calouste Gulbenkian","Captain G.T. Ward","Sir Ernest Cassel",
           "Major Custance","F. Scott Fitzgerald","Elsa Maxwell","Mata Hari",
           "Clayton Pasha","Arturo Toscanini","Maharajah Behar","Leon Wenger",
           "Sarah Bernhardt","Arthur Vetter","Isadora Duncan","David K.E. Bruce" ]

Conversation = namedtuple("Conversation", "who msg")
conversations = [
  Conversation(None,"I've heard they all have different color chalets\non a north-south ridge in the Tyrol region."),
  Conversation(None,"The Austrian said he likes the look of natural wood\nand would never paint his chalet."),
  Conversation(None,"They gave the waiter a difficult time.  The Turk\nordered beer and the other four all ordered different drinks."),
  Conversation(None,"The Greek told me he hunts deer, but he never hunts\nwith any of the others because they all hunt different animals."),
  Conversation(people[0],"My brother delivered a case of Kirsch to the green chalet.\nHe remembers it being just south of the gaudy red chalet."),
  Conversation(None,"The Pole asked me--can you imagine that?--if I wanted to buy\nany howitzers."),
  Conversation(people[1],"One of them asked me to cook some pheasant that he shot.  He\nsaid that I should come to the yellow chalet."),
  Conversation(people[0],"One time my brother said he delivered a case of\nCognac to the middle chalet."),
  Conversation(None,"The Rumanian said he had the shortest distance to drive\nfrom his chalet to the railroad station at Munich."),
  Conversation(None,"One of them bragged that his military rifles were so\naccurate that he bagged a fox with one of them."),
  Conversation(None,"The man who hunts wild boar said that the pistol dealer\nwho lives in the chalet next to his often gives loud parties."),
  Conversation(None,"The pheasant hunter complained that the arms dealer in the\nchalet next to his makes far too much noise testing his mortars."),
  Conversation(None,"The gin drinker bragged that he shot sixty wart hogs on\na single day last August."),
  Conversation(None,"The Rumanian said he looks out on a blue chalet."),
  Conversation(None,"The Cognac drinker bragged that he is the best hunter and\ncan drink more than all of the rest of them combined."),
  Conversation(None,"The one carrying the pistol said he thinks the boar's head\nover his neighbor's doorway is revolting."),
  Conversation(None,"One of them said that one day he'd like to lob a mortar\nshell at the string of pheasants drying in his neighbor's yard."),
  Conversation(None,"The Kirsch drinker said he loved the roast chicken he had\nto eat last night."),
  Conversation(None,"The one carrying the pistol had a second helping of pie."),
  Conversation(None,"One commented that his beef dinner wasn't nearly as good\nas the boar that he shot last week."),
  Conversation(None,"The Pole asked for more soup."),
  Conversation(None,"The one eating all the cheese mumbled that it was the same\ncolor as his chalet."),
  Conversation(None,"The Rumanian and Austrian got completely drunk last night."),
  Conversation(None,"I'd like to visit the blue chalet.  The owner is said to\nserve excellent lobster.") ]


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
    if callable(gs.segment.ht): gs.segment.ht(gs)
    derail(gs)

def ring_doorbell() -> None:
    print(centered("*  * BRRRINNNG! *  *"))
    print()
    time.sleep(1.0) 
    if random.randrange(0,5) == 0:
        print(centered("*  * Knock knock knock! *  *"))
        print()
        time.sleep(1.0) 
    print('You open the door:')
    # pause('Press <return> to open the door...')
    print()

def run_meals(gs: GameState) -> None:
    if gs.segment.tf == TimeFrame.Breakfast:  serve_breakfast()
    elif gs.segment.tf == TimeFrame.Lunch:  serve_lunch()
    elif gs.segment.tf == TimeFrame.Dinner:  serve_dinner()
       
def run_convo(gs: GameState) -> None:
    if gs.segment.nconv == 0: return
    cls(2)
    print("Later, in your compartment: ")
    for i in range(gs.segment.nconv):
        cls(2)
        convo = gs.conversations.pop()
        ring_doorbell()
        person = convo.who or people[random.randrange(2,25)]
        print(f'Standing there is {person}, who tells you:')
        print(convo.msg)  
        cls(2)
        pause('Press <return> when finished with the conversation...')

def intro() -> None:
    cls()
    print(title)
    pause()
    print(scenario)
    pause("Press <return> to call a taxi...") 

def fmt_time(t):
    t += 10000 
    if (t % 100) > 59: t+= 40
    t = str(t) 
    return t[1:3] + ':' + t[3:]

def announce_arrival(seg):
    minutes_late = 18 - random.randrange(0,27)
    ta = seg.tarrive + minutes_late
    print(f'You have arrived at {seg.city} at {fmt_time(ta)}, ', end='')
    if minutes_late > 0:  print(f'just {plural(minutes_late,"minute")} late.')
    elif minutes_late < 0: print(f'almost {plural(-minutes_late,"minute")} early.')
    else: print('right on time!')
    return ta

def first_departure() -> None:
    print("The taxi has dropped you at Victoria Station in London.")
    print("The Orient Express is standing majestically on Track 14.")
    print('All aboard....')
    time.sleep(1.0)
    pause('Press <return> to board the train...')
    print('The train is leaving.')
    time.sleep(1.0)
    whoIdx = random.randrange(3,23)
    who = people[whoIdx:whoIdx+3] 
    print()
    print(f'"You speak to some of the passengers--{who[0]},')
    print(f'{who[1]}, {who[2]} and others--and ask them to keep')
    print('their eyes and ears open and to pass any information--no')
    print('matter how trivial--to you in compartment 13.  The Channel')
    print('crossing is pleasant and the first part of the trip uneventful.')
    cls(4)
    pause()

def turkish_police(gs: GameState) -> None:
    ci = CheckedInput('Who do you identify? ',int)
    ci.choices([1,2,3,4,5],"Please enter the number for your choice ([1-5])") 

    cls(4)
    print("The Turkish police have boarded the train.  They have been")
    print("asked to assist you, but for them to do so you will have to")
    print("identify the killer (the dealer in machine guns) and the defector")
    print("(the Scotch drinker) to them.  The arms dealers are lined")
    print("up as follows:")
    print()
    print("  (1) Austrian, (2) Turk, (3) Pole, (4) Greek, (5) Rumanian.") 
    print()
    print("They ask who the defector is. ", end='')
    gs.my_defector = ci.run()
    time.sleep(1.0)
    print()
    print("They ask who the killer is. ", end='')
    ci.ensure(lambda c: c != gs.my_defector, 
             "You already chose him for the defector!")
    gs.my_killer = ci.run()
    time.sleep(1.5)
    print()
    print("The police take into custody the man you identified as the")
    print("killer and provide a guard to ride on the train with the")
    print("defector.  You return to your compartment, praying that")
    print("you made the correct deductions and identified the right men.")
    print()
    pause()
    print()

def arrive_depart(j: int, gs: GameState) -> None:
    seg = gs.segment
    ta = announce_arrival(seg)
    td = seg.tdepart
    if ta > (td - 2):  td = ta + 4  # ensure depart after arrival
    
    if j == 24: return  # end of game...

    if seg.tf == TimeFrame.Night:
        print("Asleep in your compartment, you barely notice that the")
        print(f"departure was right on time at {fmt_time(td)}.")
        cls(2)
        pause()
        return
       
    if j == 23: turkish_police(gs)
  
    print(f'Departure is at {fmt_time(td)}.')
    print()
    if said_y('Would you like to get off the train and stretch your legs? '):
        print('Ok, but be sure not to miss the train.') 
        time.sleep(1.0)
    else:
        print('Ok, you stay in your compartment.') 
    print()
    print('All aboard....')
    time.sleep(1.0)
    print('The train is leaving.')

def determine_outcome(gs: GameState) -> None:
    d, k = defector(), killer()

    # Did you get everything right?
    if gs.my_defector == d and gs.my_killer == k:
        gs.perfection = True
        return
    
    # The defector is killed by bandits if you didn't either
    # protect him or arrest him
    if d not in [gs.my_defector, gs.my_killer]:
        print()
        print("You are suddenly awakened by what sounded like a gunshot.")
        print("You rush to the defector's compartment, but he is okay.")
        print("However, one of the other arms dealers has been shot.")
        time.sleep(2.0)
        print()
        print("You review the details of the case in your mind and realize")
        print("that you came to the wrong conclusion and due to your mistake")
        print("a man lies dead at the hand of bandits.  You return to your")
        print("compartment and are consoled by the thought that you correctly")
        print("identified the killer and that he will hang for his crimes.")
        print()
        print("At least, you hope that's true...")
        pause()

    # if you didn't identify the killer, he kills you!
    if k != gs.my_killer:
        ring_doorbell()
        print("A man is standing outside.  He says, 'You made a")
        print("mistake.  A bad one.  You see, I am the machine gun dealer.'")
        if gs.my_killer == d:
            print()
            print("'Moreover,' he says, 'you identified the man who was cooperating")
            print("with you as the killer.  So the state will take care of him.  Ha.'")
        print()
        time.sleep(2.0)
        print("He draws a gun.  BANG.  You are dead.")
        print()
        print("You never know that the train arrived at 12:30, right on")
        print("time at Constantinople, Turkey.") 
        cls(3)
        gs.alive = False
        pause()

def endgame(gs: GameState) -> None:
    cls(4)
    print("Your journey has ended.  Georges Nagelmackers and the")
    print("management of Cie. Internationale des Wagons-Lits ")
    print("hope you enjoyed your trip on the Orient Express, the")
    print("most famous train in the world.")
    if gs.perfection:
        print()
        print("Whitehall telegraphs congratulations for identifying both")
        print("the killer and defector correctly.")
        time.sleep(1.0) 
        for _ in range(3):
            cls(2)
            print(centered('* * CONGRATULATIONS! * *'))
            time.sleep(1.5) 
    cls(4)
    pause()

def run_game() -> None:
    random.seed()
    gs = GameState()
    intro()
    for j,seg in enumerate(segments,1):
        gs.segment = seg 
        cls(4)
        print(centered(f'~ February {seg.day + 13 + gs.hazard_delay} 1923 ~'))
        print(centered(f'~ {seg.city}, {seg.country} ~'))
        print()

        if j == 1: 
            first_departure()
        elif j < 24:
            arrive_depart(j,gs)
        else:
            if gs.alive: announce_arrival(seg)
            endgame(gs)
            return

        # TODO: train noises??
        if j == 23:  determine_outcome(gs)
   
        if gs.alive:
            run_meals(gs)
            run_convo(gs)
            run_hazards(gs)
            time.sleep(1.0)

if __name__ == "__main__":
    while True:
        run_game()
        cls(3)
        if not said_y('Would you like to play again? '):
            break

