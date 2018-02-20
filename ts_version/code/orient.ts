import * as bca from './bca.js';
import UI = bca.UI

/* 
# The identities of the killer and defector were beautifully hidden in the original
# program.  I had to work out who they were by some sleuthing in the code, since I
# do not have a running GW-BASIC anymore.  The two functions below embody the answers
# I found.  `defector` re-creates the original computation, which was distributed
# across the original program.  `killer()` can't do that for technical reasons,
# and instead hides the answer behind base64 encoding.
*/

/** works out the defector by retracing the steps of the original BASIC program
  */
function defector() {
    const posx = "Press any key when you have finished eating".length + 18
    const meals = [0, 1, 0, 4, 4, 0, 3, 0, 0, 2, 1, 0, 0, 0, 4, 4, 3, 2, 0, 1, 4, 4, 3, 0]
    let a3 = 0
    meals.forEach((n, j) => {
        if ((j < 22) && (n & 1)) {
            a3 += 5 * (j + 2) - posx
        }
    })
    return a3
}

/**
 *     I can't retrace the program for the killer, because it relies
       gw-basic's ON ERROR GOTO mechanism for OUT OF DATA, 
       which is brilliant.  I'll just hide it behind base64 for now,
       so you can't see who it is by accident.
 */
function killer() {
    return parseInt(atob('NA=='))
}


var breakfasts = ["Variete Jus de Fruits", "Prunes Macerees dans le Vin",
    "Demi Pamplemouse", "Trois Oeufs sur le Plat", "Oeufs Poches",
    "Omlette aux Champagnons", "Tranches de Pain Beurees et Confiturees",
    "Galettes", "Pommes-Frites", "Patisseries", "Croissants", "Yogurt",
    "Cafe, The, Lait, Vin, au Eau Minerale"]

var dinners = ["Huitres de Beernham", "Cantalop glace au Marsale",
    "Compotee de Tomates Fraiches", "Potage Reine",
    "La Natte de Sole au Beurre", "Truite de riviere meuniere",
    "Poulet de grain grille a Diable", "Roti de Veau a l'Osille",
    "Truite Saumonee a la Chambord", "Chaud-froid de Caneton",
    "Chaudfroix de Langouste a la Parisienne",
    "Les Noisettes de Chevreuil Renaissance", "Becasses a la Monaco",
    "Pointes d'asperge a la creme", "Parfait de foies gras",
    "Salade Catalane", "Truffes au Champagne",
    "Tagliatelle de carottes et courgettes", "Souffle d'Anisette",
    "Creme de Caramel blond", "Sorbet aux Mures de Framboisier",
    "La selection du Maitre Fromager", "Corbeille de Fruits",
    "Les Mignardises", "Selection du vins et liquors"]


function do_menu(ui: UI, title: string, items: string[]): void {
    ui.printClass('menutitle', title)
    const mlist = document.createElement('ul')
    mlist.setAttribute('class', 'menulist')
    items.map(txt => {
        const n = document.createElement('li')
        n.innerText = txt
        return n
    }).forEach(mlist.appendChild, mlist)
    ui.appendNode(mlist)
}

async function serve_breakfast(ui: UI): Promise<void> {
    ui.section('Breakfast')
    ui.print("Breakfast is now being served in the restaurant car.")
    await ui.pause()
    let menu = []
    for (let i = 0; i < 4; i++) {
        menu.push(breakfasts[Math.floor(3 * (i + Math.random()))])
    }
    do_menu(ui, 'BREAKFAST MENU', menu)
    await ui.pause('Press when finished eating.')
}

async function serve_lunch(ui: UI): Promise<void> {
    ui.section('Lunch')
    ui.print("An enormous buffet luncheon has been laid out in the restaurant car.")
    await ui.pause('Press when finished eating.')
    ui.printClass('centered', " * * B-U-R-P ! * * ")
    await ui.sleep(1.0)
}

async function serve_dinner(ui: UI): Promise<void> {
    ui.section('Dinner')
    ui.print("Dinner is now being served in the restaurant car.")
    await ui.pause()
    let menu = []
    for (let i = 0; i < 7; i++) {
        menu.push(dinners[Math.floor(3 * (i + Math.random()))])
    }
    menu.push(dinners[22], dinners[23], dinners[24])
    do_menu(ui, 'DINNER MENU', menu)
    await ui.pause('Press when finished eating.')
}


const people = ["R. Brundt (a waiter)", "C. D'Arcy (a chef)",
    "Herbert Hoover", "Baron Rothschild", "Guido Famadotta", "Gustav Mahler",
    "Robert Baden-Powell", "Fritz Kreisler", "Dame Melba", "Gerald Murphy",
    "Calouste Gulbenkian", "Captain G.T. Ward", "Sir Ernest Cassel",
    "Major Custance", "F. Scott Fitzgerald", "Elsa Maxwell", "Mata Hari",
    "Clayton Pasha", "Arturo Toscanini", "Maharajah Behar", "Leon Wenger",
    "Sarah Bernhardt", "Arthur Vetter", "Isadora Duncan", "David K.E. Bruce"]

class Conversation {
    constructor(public who: string | null, public msg: string) {}
}

const conversations = [
    new Conversation(null, "I've heard they all have different color chalets on a north-south ridge in the Tyrol region."),
    new Conversation(null, "The Austrian said he likes the look of natural wood and would never paint his chalet."),
    new Conversation(null, "They gave the waiter a difficult time.  The Turk ordered beer and the other four all ordered different drinks."),
    new Conversation(null, "The Greek told me he hunts deer, but he never hunts with any of the others because they all hunt different animals."),
    new Conversation(people[0], "My brother delivered a case of Kirsch to the green chalet. He remembers it being just south of the gaudy red chalet."),
    new Conversation(null, "The Pole asked me--can you imagine that?--if I wanted to buy any howitzers."),
    new Conversation(people[1], "One of them asked me to cook some pheasant that he shot.  He said that I should come to the yellow chalet."),
    new Conversation(people[0], "One time my brother said he delivered a case of Cognac to the middle chalet."),
    new Conversation(null, "The Rumanian said he had the shortest distance to drive from his chalet to the railroad station at Munich."),
    new Conversation(null, "One of them bragged that his military rifles were so accurate that he bagged a fox with one of them."),
    new Conversation(null, "The man who hunts wild boar said that the pistol dealer who lives in the chalet next to his often gives loud parties."),
    new Conversation(null, "The pheasant hunter complained that the arms dealer in the chalet next to his makes far too much noise testing his mortars."),
    new Conversation(null, "The gin drinker bragged that he shot sixty wart hogs on a single day last August."),
    new Conversation(null, "The Rumanian said he looks out on a blue chalet."),
    new Conversation(null, "The Cognac drinker bragged that he is the best hunter and can drink more than all of the rest of them combined."),
    new Conversation(null, "The one carrying the pistol said he thinks the boar's head over his neighbor's doorway is revolting."),
    new Conversation(null, "One of them said that one day he'd like to lob a mortar shell at the string of pheasants drying in his neighbor's yard."),
    new Conversation(null, "The Kirsch drinker said he loved the roast chicken he had to eat last night."),
    new Conversation(null, "The one carrying the pistol had a second helping of pie."),
    new Conversation(null, "One commented that his beef dinner wasn't nearly as good as the boar that he shot last week."),
    new Conversation(null, "The Pole asked for more soup."),
    new Conversation(null, "The one eating all the cheese mumbled that it was the same color as his chalet."),
    new Conversation(null, "The Rumanian and Austrian got completely drunk last night."),
    new Conversation(null, "I'd like to visit the blue chalet.  The owner is said to serve excellent lobster.")
]

enum TimeFrame { Early, Breakfast, Lunch, Dinner, Night }

class Segment {
    constructor(
        public tf: TimeFrame,    
        public nconv: number,   // number of conversations
        public ht: ((ui: UI, gs: GameState) => Promise<void>) | null,  // hazard type 
        public day: number,     // days into the journey
        public tarrive: number,  // arrival time
        public tdepart: number,  // departure time
        public city: string,    
        public country: string
    ) { }
}

const segments = [
    new Segment(TimeFrame.Early, 0, null, 1, 0, 1430, "London", "England"),
    new Segment(TimeFrame.Breakfast, 2, null, 1, 1855, 1919, "Calais", "France"),
    new Segment(TimeFrame.Early, 1, null, 1, 2233, 2253, "Paris (Nord)", "France"),
    new Segment(TimeFrame.Night, 0, null, 1, 2316, 2350, "Paris (Lyon)", "France"),
    new Segment(TimeFrame.Night, 0, snow, 2, 600, 620, "Vallorbe", "Switzerland"),
    new Segment(TimeFrame.Early, 1, null, 2, 700, 707, "Lausanne", "Switzerland"),
    new Segment(TimeFrame.Dinner, 1, snow, 2, 732, 734, "Montreux", "Switzerland"),
    new Segment(TimeFrame.Early, 1, snow, 2, 919, 927, "Brig", "Switzerland"),
    new Segment(TimeFrame.Early, 3, null, 2, 1005, 1025, "Domodossola", "Italy"),
    new Segment(TimeFrame.Lunch, 2, null, 2, 1223, 1320, "Milan", "Italy"),
    new Segment(TimeFrame.Breakfast, 2, null, 2, 1705, 1730, "Venice (S. Lucia)", "Italy"),
    new Segment(TimeFrame.Early, 1, null, 2, 1954, 2014, "Trieste", "(Free State)"),
    new Segment(TimeFrame.Early, 1, null, 2, 2044, 2110, "Opicina", "Italy"),
    new Segment(TimeFrame.Early, 2, null, 2, 2119, 2225, "Sezana", "Slovenia"),
    new Segment(TimeFrame.Night, 0, null, 3, 21, 107, "Ljubljana", "Slovenia"),
    new Segment(TimeFrame.Night, 0, null, 3, 310, 330, "Zagreb", "Croatia"),
    new Segment(TimeFrame.Dinner, 2, null, 3, 900, 956, "Belgrade", "Serbia"),
    new Segment(TimeFrame.Lunch, 1, null, 3, 1334, 1356, "Crveni Krst", "Serbia"),
    new Segment(TimeFrame.Early, 2, null, 3, 1555, 1634, "Caribrod", "Serbia"),
    new Segment(TimeFrame.Breakfast, 2, null, 3, 1856, 1935, "Sofia", "Bulgaria"),
    new Segment(TimeFrame.Night, 0, bandits, 4, 45, 120, "Svilengrad", "Bulgaria"),
    new Segment(TimeFrame.Night, 0, bandits, 4, 406, 445, "Pithion", "Greece"),
    new Segment(TimeFrame.Dinner, 0, null, 4, 505, 545, "Uzunkopru", "Turkey"),
    new Segment(TimeFrame.Early, 0, null, 4, 1230, 0, "Constantinople", "Turkey")]

class GameState {
    segment: Segment = segments[0]         // which segment of the trip are we on? 
    derailed = false       // have we derailed yet?
    bandits = false       // have bandits attacked?
    hazard_delay = 0       // days delayed by hazards
    convos: Conversation[] = bca.shuffle(conversations.slice())
    my_defector = -1     // player choice
    my_killer = -1       // player choice
    perfection = false     // did you get everything right?
    alive = true           // are we alive?
}

async function snow(ui: UI, gs: GameState): Promise<void> {
    const x = Math.random()
    if (x > 0.65) return   // 65% chance of snow
    ui.section('Snow!')
    if (x > 0.02) {  // 2% chance of heavy snow
        ui.print(`It is snowing heavily but the tracks have been cleared and the train
        will not be delayed.`)
    } else {
        ui.print(`It is snowing heavily and the train is forced to slow down.`)
        ui.print(`Oh no!  The train is coming to a stop.  Let's hope this is
        not a repeat of the trip of January 29, 1929 when the Orient
        Express was stuck in snowdrifts for five days.`)
        await ui.sleep(1.0)
        ui.print("But it looks like it is!")
        await ui.sleep(1.0)
        gs.hazard_delay += 2
        ui.print(`You are stranded for two days until a snowplow clears the track.
        The train is now exactly ${gs.hazard_delay} days behind schedule.`)
    }
    await ui.pause()
}

async function ring_doorbell(ui: UI): Promise<void> {
    ui.printClass('centered', "*  * BRRRINNNG! *  *")
    await ui.sleep(1.0)
    if (Math.random() < 0.2) {
        ui.printClass('centered', "*  * Knock Knock Knock! *  *")
        await ui.sleep(1.0)
    }
    ui.print('You open the door...')
}

async function bandits(ui: UI, gs: GameState): Promise<void> {
    if (gs.bandits || (Math.random() > 0.04)) return  // 4% chance of bandits
    gs.bandits = true
    ui.section('Bandits!')
    ui.printClass('centered', "* * CLANG! * *")
    await ui.sleep(1.0)
    ui.print(`You are rudely awakened from a deep sleep by a loud noise
    as the train jerks to a halt.`)
    await ui.sleep(1.0)
    await ring_doorbell(ui)
    ui.print(`You are shocked to see a bandit waving a gun in your face.
    He demands you give him your wallet, jewelry, and watch.`)
    await ui.sleep(1.0)
    ui.print(`The bandits are off the train in a few moments with
    their loot.  They disappear into the forest.  No one
    was injured, and the train resumes its journey.`)
    await ui.pause()
}

async function derail(ui: UI, gs: GameState): Promise<void> {
    if (gs.derailed || (Math.random() > 0.02)) return  //  2% chance of derailment
    gs.derailed = true
    gs.hazard_delay += 1
    ui.section('Derailed!')
    ui.printClass('centered', "* * SCREEECH! * *")
    await ui.sleep(1.0)
    ui.print(`You hear a loud screeching noise as the train comes to a
    crashing stop.  The engine, tender, and first coach are
    leaning at a crazy angle.  People are screaming.`)
    await ui.sleep(1.0)
    ui.print(`While not as bad as the derailment at Vitry-le-Francois in
    November 1911, there is no question that the front of the
    train has left the track.`)
    await ui.sleep(1.0)
    ui.print(`You are stranded for exactly one day while the track is
    repaired and a new locomotive obtained. The train is now 
    exactly ${bca.plural(gs.hazard_delay, 'day')} behind schedule.`)
    await ui.pause()
}

const scenario = [
    `It is February 1923.  The following note is received at
     Whitehall: 'If you will furnish me with a new identity and a
     lifetime supply of Scotch, I will give up my life of arms dealing
     and will provide you with much valuable information.  I will be
     on the Orient Express tonight.  But you must contact me before
     the train reaches Uzunkopru or that swine dealer of Maxim machine
     guns will have me killed by bandits like he did to Baron Wunster
     last month.'  The note is not signed.`,

    `You, a British agent, are assigned to take the train, rescue
     the defector, and arrest the killer.`,

    `You know there are five notorious arms dealers of different
     nationalities operating in Europe under an uneasy truce as each
     deals in a different kind of weapon.  But it is obvious that the
     truce has ended.`  ]

async function intro(ui: UI): Promise<void> {
    ui.section('Orient Express, 1923');
    ui.printClass('copyright', 'Original BASIC Adventure by David Ahl, (c) 1986');
    ui.printClass('centered', "The Mysterious Arms Deal")
    scenario.forEach(ui.print, ui);
    await ui.pause('Press here to call a taxi...');
}

/** On some days we have snow or bandits...and any day we could derail  */
async function run_hazards(ui: UI, gs: GameState): Promise<void> {
    if (gs.segment.ht) { await gs.segment.ht(ui, gs) }
    await derail(ui, gs)
}

async function run_meals(ui: UI, gs: GameState): Promise<void> {
    switch (gs.segment.tf) {
        case TimeFrame.Breakfast: await serve_breakfast(ui); break
        case TimeFrame.Lunch: await serve_lunch(ui); break
        case TimeFrame.Dinner: await serve_dinner(ui); break
    }
}

async function run_convo(ui: UI, gs: GameState): Promise<void> {
    if (gs.segment.nconv == 0) return
    ui.section('Visitors')
    ui.print("Later, in your compartment...")
    for (let i = 0; i < gs.segment.nconv; i++) {
        const c  = gs.convos.pop() || { who: null, msg: "hmphrr... (incoherent rambling)" }
        await ring_doorbell(ui)
        const person = c.who || people[Math.floor(Math.random() * 23 + 2)]
        ui.print(`Standing there is ${person}, who tells you: ${c.msg}`)
        await ui.pause()
    }
}

function fmt_time(t: number): string {
    t += 10000
    if ((t % 100) > 59) t += 40
    const tstr = t.toString()
    return `${tstr.slice(1, 3)}:${tstr.slice(3)}`
}

function announce_arrival(ui: UI, seg: Segment): number {
    const minutes_late = Math.floor(18 - 27 * Math.random())
    const ta = seg.tarrive + minutes_late
    let expound = ''
    if (minutes_late > 0) expound = `just ${bca.plural(minutes_late, "minute")} late.`
    else if (minutes_late < 0) expound = `almost ${bca.plural(-minutes_late, "minute")} early.`
    else expound = `right on time!`

    ui.print(`You have arrived at ${seg.city} at ${fmt_time(ta)}, ${expound}`)
    return ta
}

async function first_departure(ui: UI): Promise<void> {
    // ui.section('Departure!')
    ui.print(`The taxi has dropped you at Victoria Station in London.
    The Orient Express is standing majestically on Track 14.
    All aboard....`)
    await ui.sleep(1.0)
    await ui.pause('Press here to board the train...')
    ui.print('The train is leaving.')
    await ui.sleep(1.0)
    const idx = Math.floor(3 + Math.random() * 20)
    const who = people.slice(idx, idx + 3)
    ui.print(`You speak to some of the passengers--${who[0]},
    ${who[1]}, ${who[2]} and others--and ask them to keep
    their eyes and ears open and to pass any information--no
    matter how trivial--to you in compartment 13.  The Channel
    crossing is pleasant and the first part of the trip uneventful.`)
    await ui.pause()
}

async function banner(ui: UI, n: number, msg: string, msgClass = 'centered'): Promise<void> {
    for (let i = 0; i < n; i++) {
        ui.printClass(msgClass, msg);
        await ui.sleep(1.0);
    }
}

async function turkish_police(ui: UI, gs: GameState): Promise<void> {
    const full_choices = ["Austrian", "Turk", "Pole", "Greek", "Rumanian"]

    ui.section('Turkish Police!')

    ui.print(`The Turkish police have boarded the train.  They have been
    asked to assist you, but for them to do so you will have to
    identify the killer (the dealer in machine guns) and the defector
    (the Scotch drinker) to them.  The arms dealers are lined up.`)

    const myd = await ui.choices("Who do you identify as the defector?", full_choices)
    await ui.sleep(1.0)
    const reduced_choices = full_choices.filter(c => c != myd)
    const myk = await ui.choices("Now they want you to identify the killer...", reduced_choices)
    await ui.sleep(1.5)
    ui.print(`The police take into custody the man you identified as the
    killer and provide a guard to ride on the train with the
    defector.  You return to your compartment, praying that
    you made the correct deductions and identified the right men.`)
    await ui.pause()
    ui.section('Later on...')

    gs.my_defector = full_choices.findIndex(c => c == myd) + 1
    gs.my_killer = full_choices.findIndex(c => c == myk) + 1
}

async function endgame(ui: UI, gs: GameState): Promise<void> {
    ui.section('End of Journey!')
    ui.print(`Your journey has ended.  Georges Nagelmackers and the
    management of Cie. Internationale des Wagons-Lits 
    hope you enjoyed your trip on the Orient Express, the
    most famous train in the world.`)
    if (gs.perfection) {
        ui.print(`Whitehall telegraphs congratulations for identifying both
        the killer and defector correctly.`)
        await ui.sleep(1.0)
        await banner(ui, 3, '* * CONGRATULATIONS! * *')
    }
    await ui.pause()
}

async function arrive_depart(ui:  UI, j: number, gs: GameState): Promise<void> {
    const seg = gs.segment
    const ta = announce_arrival(ui, seg)
    let td = seg.tdepart
    if (ta > (td - 2)) td = ta + 4  // ensure depart after arrival

    if (j === 23) return  // end of game...

    if (seg.tf === TimeFrame.Night) {
        ui.print(`Asleep in your compartment, you barely notice that the
        departure was right on time at ${fmt_time(td)}.`)
        await ui.pause()
        return
    }

    if (j === 22) await turkish_police(ui, gs)

    ui.print(`Departure is at ${fmt_time(td)}.`)
    const get_off = await ui.choices("Would you like to get off the train and stretch your legs?", ["Yes", "No"])
    if (get_off === 'Yes') {
        ui.print('Ok, but be sure not to miss the train.')
    } else {
        ui.print('Ok, you stay in your compartment.')
    }
    await ui.sleep(1.0)
    ui.print('All aboard....')
    await ui.sleep(0.5)
    ui.print('The train is leaving.')
}

async function determine_outcome(ui: UI, gs: GameState): Promise<void> {
    const [d, k] = [defector(), killer()]

    // Did you get everything right?
    if (gs.my_defector == d && gs.my_killer == k) {
        gs.perfection = true
        return
    }

    // The defector is killed by bandits if you didn't either
    // protect him or arrest him
    if (d !== gs.my_defector && d !== gs.my_killer) {
        ui.print(`You are suddenly awakened by what sounded like a gunshot.
        You rush to the defector's compartment, but he is okay.
        However, one of the other arms dealers has been shot.`)
        await ui.sleep(2.0)
        ui.print(`You review the details of the case in your mind and realize
        that you came to the wrong conclusion and due to your mistake
        a man lies dead at the hand of bandits.  You return to your
        compartment and are consoled by the thought that you correctly
        identified the killer and that he will hang for his crimes.`)

        ui.print("At least, you hope that's true...")
        await ui.pause()
    }

    // if you didn't identify the killer, he kills you!
    if (k !== gs.my_killer) {
        await ring_doorbell(ui)
        ui.print(`A man is standing outside.  He says, 'You made a
        mistake.  A bad one.  You see, I am the machine gun dealer.'`)
        if (gs.my_killer == d) {
            ui.print(`'Moreover,' he says, 'you identified the man who was cooperating
            with you as the killer.  So the state will take care of him.  Ha.'`)
        }
        await ui.sleep(2.0)
        ui.print("He draws a gun.  BANG.  You are dead.")
        ui.print(`You never know that the train arrived at 12:30, right on
        time at Constantinople, Turkey.`)
        gs.alive = false
        await ui.pause()
    }
}


async function run_game(ui: UI): Promise<void> {
    const gs = new GameState()
    await intro(ui)
    for (let j = 0; j < segments.length; ++j) {
        gs.segment = segments[j]
        const seg = gs.segment
        ui.section(`${seg.city}`)
        ui.printClass('centered', `~ February ${seg.day + 13 + gs.hazard_delay} 1923 ~`)
        ui.printClass('centered', `~ ${seg.city}, ${seg.country} ~`)

        if (j === 0) {
            await first_departure(ui)
        } else if (j < 23) {
            await arrive_depart(ui, j, gs)
        } else {
            if (gs.alive) {
                announce_arrival(ui, seg)
            }
            await endgame(ui, gs)
            return
        }

        if (j === 22) {
            await determine_outcome(ui, gs)
        }

        if (gs.alive) {
            await run_meals(ui, gs)
            await run_convo(ui, gs)
            await run_hazards(ui, gs)
            await ui.sleep(1.0)
        }
    }
}

export async function main(ui: UI): Promise<void> {
    while (true) {
        await run_game(ui);
        ui.section('Play Again?');
        await ui.pause('Press here to restart the game...');
        ui.clearScreen();
    }
}
