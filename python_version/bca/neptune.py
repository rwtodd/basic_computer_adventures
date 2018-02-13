# Voyage to Neptune

from bca import centered, CheckedInput, cls, pause, plural, said_y
import random
from collections import namedtuple
import time

def fmt_days(days: int) -> str:
    """format a summary of time, based on a given number of days"""
    result = []
    years, days = int(days//365), days % 365
    months, days = int(days/30.5), int(days % 30.5)
    if years > 0: result.append(plural(years,'year'))
    if months > 0: result.append(plural(months,'month'))
    if days > 0: result.append(plural(days, 'day'))
    return ', '.join(result)

# Define the trip's segments in terms of locations and distances.
Segment = namedtuple("Segment", "location distance")
trip = [ Segment('Earth', 391), Segment('Callisto', 403), Segment('Titan', 446),
         Segment('Alpha 1', 447), Segment('Ariel', 507), Segment('Theta 2', 507),
         Segment('Neptune', 0)  ]

class GameState():
    def __init__(self):
        self.totime = 0    # total cumulative time 
        self.breed = 120   # breeder-reactor cells
        self.futot = 3000  # fuel cells
        self.seg   = 0     # segment of the trip
        self.distance = 0  # distance travelled

        self.fuseg = 0     # amount of fuel to use this segment
        self.rate = 0      # rate of speed (last seg)
        self.time = 0      # time spent (last seg)
        self.ubreed = 0    # used breeder cells (last seg)
        self.fubr = 0      # fuel used per breeder cell (last seg)
        self.fudcy = 0     # how much fuel decays (last seg)

def fuel_report(gs: GameState) -> None:
    print()
    print(f'Pounds of of nuclear fuel ready for use: {gs.futot}')
    print(f'Operational breeder reactor cells: {gs.breed}')
    print()

def print_conditions(gs: GameState) -> None:
    print()
    print("Current conditions are as follows:\n")
    print(f'  Location:  {trip[gs.seg].location}')
    print(f'  Distance to Neptune: {2701 - gs.distance} million miles.')
    if gs.seg > 0:
        print(f'  Distance from Earth: {gs.distance} million miles.')
        print()
        print(f'Over the last segment, your average speed was {int(gs.rate)} mph,')
        print(f'  and you covered {trip[gs.seg-1].distance} million miles in {gs.time} days.')
        print(f'Time est for this total distance: {fmt_days(0.81*gs.distance)}')
        print(f'Your actual cumulative time was: {fmt_days(gs.totime)}')
        print(f'You used {gs.ubreed} cells which produced {gs.fubr} pounds of fuel each.')
        if gs.fudcy > 0:
            print(f'{gs.fudcy} pounds of fuel in storage decayed into an unusable state.')
    fuel_report(gs)

def timed_banner(n, msg, delay):
    cmsg = centered(msg)
    for _ in range(n):
        print(cmsg)
        print()
        time.sleep(delay)

def engine_malfunction(gs: GameState, reduction: float) -> None:
    cls(10)
    timed_banner(3, '* * ENGINE MALFUNCTION!!! * *', 0.5)
    cls(5)
    print(f'You will have to operate your engines at a {int(reduction*100)}% reduction')   
    print(f'in speed until you reach {trip[gs.seg+1].location}.')
    print()
    pause()
    

def trade_fuel(gs: GameState) -> None:
    """Trade fuel for breeder reactor cells, or vice versa"""
    trade = 150 + int(80*random.random())
    if gs.seg == 0:
        print("Before leaving, you can trade fuel for breeder reactor cells at")
    else:
        print(f'Here at {trip[gs.seg].location}, breeder cells and nuclear fuel trade at')
    print(f"the rate of {trade} pounds of fuel per cell.")
    print()

    enough_fuel = (gs.futot - trade) > 1500
    if not enough_fuel: print("You have too little fuel to trade.")
    if enough_fuel and said_y("Would you like to procure more breeder cells? "):
        ncells = CheckedInput('How many cells do you want? ', int)
        ncells.ensure_nonneg()
        ncells.ensure(lambda c: (gs.futot - c*trade) > 1500,
                      "That doesn't leave enough fuel to run the engines.")
        ncells = ncells.run()
        gs.futot -= ncells*trade
        gs.breed += ncells
        return
    
    enough_cells = (gs.breed > 50)
    if not enough_cells: print("You have too few breeder cells to trade.")
    if enough_cells and said_y("Would you like to trade some breeder cells for fuel? "):
        ncells = CheckedInput('How many cells would you like to trade? ', int)
        ncells.ensure_nonneg()
        ncells.ensure_lessthan(gs.breed, "That's more cells than you have!")
        ncells.ensure_lessthan(gs.breed - 50,
                               lambda c: f'That would leave only {gs.breed - c} cells. The reactor requires a minimum\n    of 50 cells to remain operational.')
        ncells = ncells.run()
        gs.breed -= ncells
        gs.futot += ncells*trade

def engine_power(gs: GameState) -> None:
    print()
    print("At this distance from the sun, your solar collectors can fulfill")
    print(f'{56-(gs.seg+1)*8}% of the fuel requirements of the engines.  How many pounds')
    lbs = CheckedInput('of nuclear fuel do you want to use on this segment? ', int)
    lbs.ensure_nonneg()
    lbs.ensure_lessthan(gs.futot + 1, "That's more fuel than you have.  Now then, how many pounds")
    gs.fuseg = lbs.run()

def check(c: bool, carp: str) -> bool:
    """complain with CARP if C is not True"""
    if not c:
        print(carp)
    return c

def breeder_usage(gs: GameState) -> None:
    bu = CheckedInput("How many breeder reactor cells do you want to operate? ", int)
    bu.ensure_nonneg()
    bu.ensure_lessthan(gs.breed + 1, "You don't have that many cells.")
    bu.ensure_lessthan(gs.fuseg/20+1, f'The spent fuel from your engines is only enough to operate {int(gs.fuseg/20)}\n    breeder reactor cells.  Again please...')
    bu.ensure_lessthan(int(gs.futot/5)+1, f'You have only enough fuel to seed {int(gs.futot/5)} breeder cells.\n    Please adust your number accordingly.')
    gs.ubreed = bu.run()

def calculate_results(gs: GameState) -> None:
    """calculate what happens next, after user input"""
    eff = min(54 - (gs.seg+1)*8+gs.fuseg/40, 104)  # efficiency
    engine_fail = random.random()
    if engine_fail < 0.1:                   # 10% chance of engine problem
        reduction = 3*engine_fail
        engine_malfunction(gs, reduction)
        eff *= (1-reduction)
    gs.rate = eff * 513.89                  # mph
    gs.distance += trip[gs.seg].distance    # millions of miles
    gs.time = int(trip[gs.seg].distance * 
                  41667 / gs.rate)          # days
    gs.totime += gs.time                    # total trip time
    gs.fubr = int(16+18*random.random())    
    gs.futot += gs.fubr*gs.ubreed           # new fuel from breeder
    fuel_decay = random.random()
    if fuel_decay < 0.2:                    # did fuel decay?
        gs.fudcy = int(fuel_decay*gs.futot)
    else:
        gs.fudcy = 0                        # I think this fixes a bug in the original BASIC code
    gs.futot -= gs.fudcy

def one_segment(gs: GameState) -> None:
    cls(7)
    print_conditions(gs)
    trade_fuel(gs)
    print('\nAfter trading:')
    fuel_report(gs)
    engine_power(gs)
    gs.futot -= gs.fuseg
    breeder_usage(gs)
    gs.futot -= 5*gs.ubreed
    calculate_results(gs)
    gs.seg += 1
    cls(8)
    timed_banner(3, '* * Travelling * *', 0.5)
    
def endgame(gs: GameState) -> None:
    cls(6)
    print(centered(" * * N E P T U N E ! * *"))
    cls(2)
    print(f'You finally reached Neptune in {fmt_days(gs.totime)}.')
    print("Had your engines run at 100% efficiency the entire way, you would")
    print("have averaged 51,389 mph and completed the trip in exactly 6 years.")
    print()
    if gs.totime <= 2220:
        print(centered("Congratulations!  Outstanding job!"))
    else:   
        tm = gs.totime - 2190
        print(f'Your trip took longer than this by {fmt_days(tm)}.')
        print()
        years_over = min(tm // 365, 3)
        scale = ["excellent (room for slight improvement).",
                 "quite good (but could be better).",
                 "marginal (could do much better).",
                 "abysmal (need lots more practice)."  ]
        print(f'Your performance was {scale[years_over]}')
    print()
    if gs.breed < 105:
        print('I guess you realize that the return trip will be extremely')
        print(f'chancy with only {gs.breed} breeder reactor cells operational.')
    else:
        print(f'Fortunately you have {gs.breed} operational breeder reactor cells')
        print("for your return trip.  Very good.")
    print()  
    back_to_2 = max(int(42250.0/(8.0+gs.futot/40.0)), 405)
    print(f'With your remaining {gs.futot} pounds of fuel and {gs.breed} breeder')
    print(f'cells, to get back to Theta 2 will take {fmt_days(back_to_2)}.')
    print()

title = """


                 Space Voyage to Neptune, 2100


                  (c) by David H. Ahl, 1986 



"""

scenario = """
                    Space Voyage to Neptune

     It is the Year 2100 and you are in command of the first manned
spaceship to Neptune.  Manned space stations have been established
which orbit Callisto, Titan, and Ariel, as well as at two inter-
mediate points between Saturn and Uranus, and Uranus and Neptune.
You must travel about 2700 million miles.  At an average speed of
over 50,000 miles per hour, the entire trip should take about
six years.
     Your spaceship is a marvel of 21st century engineering.  Since
you may have to stop at space stations along the way, you will not
be able to use the gravitational 'slingshot' effect of the planets.
However, your engines are highly efficient using both energy from
the sun captured by giant parabolic arrays and nuclear fuel carried
on board.  You will not be able to carry enough fuel for the whole
trip, so you also have a multi-celled nuclear breeder reactor
(which takes spent fuel from your engines along with a small amount
of primary fuel and turns it into a much greater amount of primary
fuel).
     The space stations along the way usually have a small stock of
engine repair parts, breeder reactor cells, and nuclear fuel which
are available to you on a barter basis.


"""

def run_game():
    random.seed()
    cls()
    print(title)
    pause()
    print(scenario)
    pause()
    state = GameState()
    while state.seg < (len(trip) - 1):
        one_segment(state)
    endgame(state)

if __name__ == "__main__":
    while True:
        run_game()
        cls(3)
        if not said_y('Would you like to play again? '):
            break
