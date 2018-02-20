/** Voyage to Neptune */
import * as bca from './bca.js'
import UI = bca.UI

const scenario = [
    `It is the Year 2100 and you are in command of the first manned
        spaceship to Neptune.  Manned space stations have been established
        which orbit Callisto, Titan, and Ariel, as well as at two intermediate
        points between Saturn and Uranus, and Uranus and Neptune.
        You must travel about 2700 million miles.  At an average speed of
        over 50,000 miles per hour, the entire trip should take about
        six years.`,
    `Your spaceship is a marvel of 21st century engineering.  Since
        you may have to stop at space stations along the way, you will not
        be able to use the gravitational 'slingshot' effect of the planets.
        However, your engines are highly efficient using both energy from
        the sun captured by giant parabolic arrays and nuclear fuel carried
        on board.  You will not be able to carry enough fuel for the whole
        trip, so you also have a multi-celled nuclear breeder reactor
        (which takes spent fuel from your engines along with a small amount
        of primary fuel and turns it into a much greater amount of primary
        fuel).`,
    `The space stations along the way usually have a small stock of
        engine repair parts, breeder reactor cells, and nuclear fuel which
        are available to you on a barter basis.`
]


async function intro(ui: UI) {
    ui.section('Space Voyage to Neptune')
    ui.printClass('copyright', 'Original BASIC Adventure by David Ahl, (c) 1986')
    scenario.forEach(s => ui.print(s))
    await ui.pause()
}


class Segment {
    stage: number
    place: string
    distance: number
    constructor(st: number, pl: string, dis: number) {
        this.stage = st
        this.place = pl
        this.distance = dis
    }
}

const trip = [
    new Segment(1, 'Earth', 391),
    new Segment(2, 'Callisto', 403),
    new Segment(3, 'Titan', 446),
    new Segment(4, 'Alpha 1', 447),
    new Segment(5, 'Ariel', 507),
    new Segment(6, 'Theta 2', 507),
    new Segment(7, 'Neptune', 0)
]

class GameState {
    totime = 0    // total cumulative time 
    breed = 120   // breeder-reactor cells
    futot = 3000  // fuel cells
    seg: Segment     // segment of the trip
    distance = 0  // distance travelled

    efail = 0     // engine failure percentage
    fuseg = 0     // amount of fuel to use this segment
    rate = 0     // rate of speed (last seg)
    time = 0      // time spent (last seg)
    ubreed = 0    // used breeder cells (last seg)
    fubr = 0      // fuel used per breeder cell (last seg)
    fudcy = 0     // how much fuel decays (last seg)
}

/** format a summary of time, based on a given number of days  */
function fmt_days(t: number): string {
    let result: string[] = []
    const years = Math.floor(t / 365)
    let days = t % 365
    const months = Math.floor(days / 30.5)
    days = Math.floor(days % 30.5)
    if (years > 0) result.push(bca.plural(years, 'year'))
    if (months > 0) result.push(bca.plural(months, 'month'))
    if (days > 0) result.push(bca.plural(days, 'day'))
    return result.join(', ')
}

function printConditions(ui: UI, gs: GameState): void {
    ui.section(`${gs.seg.place}`)

    ui.print("Current conditions are as follows:")
    ui.print(`Location:  ${gs.seg.place}<br>
        Distance to Neptune: ${2701 - gs.distance} million miles.<br>
        Distance from Earth: ${gs.distance} million miles.`)
    if (gs.seg.stage > 1) {
        ui.print(`Over the last segment, your average speed was ${Math.floor(gs.rate)} mph,
                      and you covered ${trip[gs.seg.stage - 2].distance} million miles in ${gs.time} days.`)
        ui.print(`Planned time for this total distance: ${fmt_days(0.81 * gs.distance)}<br>
                      Your actual cumulative time was: ${fmt_days(gs.totime)}<br>
                      You used ${gs.ubreed} cells which produced ${gs.fubr} pounds of fuel each.`)

        if (gs.fudcy > 0) {
            ui.print(`${gs.fudcy} pounds of fuel in storage decayed into an unusable state.`)
        }
    }
}

async function banner(ui: UI, n: number, msg: string, msgClass = 'centered') {
    for (let i = 0; i < n; i++) {
        ui.printClass(msgClass, msg)
        await ui.sleep(1.0)
    }
}

async function tradingInterface(ui: UI, gs: GameState) {
    const trade = Math.floor(150 + 80 * Math.random())
    const prefix = (gs.seg.stage == 1) ? "Before leaving, you can trade fuel for breeder reactor cells at" :
        `Here at ${gs.seg.place}, breeder cells and nuclear fuel trade at`
    ui.print(`${prefix} the rate of ${trade} pounds of fuel per cell.`)
    ui.print('Adjust your breeder cell count to buy or sell:')

    const slider_div = document.createElement('div')
    slider_div.setAttribute('class', 'tradefuel')
    const label_cs = document.createElement('label')
    const cell_slider = document.createElement('input')
    const cell_out = document.createElement('output')
    const csname = `${gs.seg.stage}tradeslider`
    cell_slider.setAttribute('id', csname)
    label_cs.setAttribute('for', csname)
    label_cs.innerText = "Breeder Cells: "
    cell_out.setAttribute('for', csname)

    const cellsmax = Math.floor(Math.max((gs.futot - 1500) / trade, 0) + gs.breed)
    cell_slider.setAttribute('type', 'range')
    cell_slider.setAttribute('min', '50')
    cell_slider.setAttribute('max', cellsmax.toString())
    cell_slider.setAttribute('step', '1')
    cell_slider.setAttribute('value', gs.breed.toString())

    const updater = function (x: number) {
        const delta = x - gs.breed
        const y = gs.futot - trade * delta
        cell_out.value = `${x} cells / ${y} lbs fuel`
    }

    updater(gs.breed)
    cell_slider.addEventListener('input', _ => updater(cell_slider.valueAsNumber))

    slider_div.appendChild(label_cs)
    slider_div.appendChild(cell_slider)
    slider_div.appendChild(cell_out)
    ui.appendNode(slider_div)
    await ui.pause('Done trading!')
    cell_slider.disabled = true

    const delta = cell_slider.valueAsNumber - gs.breed
    gs.breed += delta
    gs.futot -= delta * trade
}

async function enginePower(ui: UI, gs: GameState) {
    ui.print(`At this distance from the sun, your solar collectors can fulfill
        ${56 - (gs.seg.stage) * 8}% of the fuel requirements of the engines.  How many pounds
        of nuclear fuel do you want to use on this segment, and how many reactor cells 
        do you want to operate?`)

    const slider_div = document.createElement('div')
    slider_div.setAttribute('class', 'pickfuel')
    const label_fs = document.createElement('label')
    const label_cs = document.createElement('label')
    const fuel_slider = document.createElement('input')
    const cell_slider = document.createElement('input')
    const fuel_out = document.createElement('output')
    const cell_out = document.createElement('output')
    const fsname = `${gs.seg.stage}fslider`
    const csname = `${gs.seg.stage}cslider`
    fuel_slider.setAttribute('id', fsname)
    cell_slider.setAttribute('id', csname)
    label_fs.setAttribute('for', fsname)
    label_fs.innerText = "Fuel: "
    label_cs.setAttribute('for', csname)
    label_cs.innerText = "Breeder Cells: "
    fuel_out.setAttribute('for', fsname)
    cell_out.setAttribute('for', csname)

    fuel_slider.setAttribute('type', 'range')
    fuel_slider.setAttribute('min', '0')
    fuel_slider.setAttribute('max', gs.futot.toString())
    fuel_slider.setAttribute('step', '1')
    fuel_slider.setAttribute('value', '0')

    cell_slider.setAttribute('type', 'range')
    cell_slider.setAttribute('min', '0')
    cell_slider.setAttribute('step', '1')
    cell_slider.setAttribute('value', '0')

    const cell_updater = function (fuel_val: number) {
        const newmax = Math.min(gs.breed, Math.floor(fuel_val / 20), Math.floor((gs.futot - fuel_val) / 5))
        cell_slider.setAttribute('max', newmax.toString())
        if (cell_slider.valueAsNumber > newmax) {
            cell_slider.setAttribute('value', newmax.toString())
        }
        fuel_out.value = `${fuel_val} Max: ${gs.futot}`
        cell_out.value = `${cell_slider.valueAsNumber} Max: ${newmax}`
    }
    cell_updater(0) // set the initial max cells...
    fuel_slider.addEventListener('input', _ => cell_updater(fuel_slider.valueAsNumber))
    cell_slider.addEventListener('input', _ => cell_updater(fuel_slider.valueAsNumber))
    slider_div.appendChild(label_fs)
    slider_div.appendChild(fuel_slider)
    slider_div.appendChild(fuel_out)
    slider_div.appendChild(document.createElement('br'))
    slider_div.appendChild(label_cs)
    slider_div.appendChild(cell_slider)
    slider_div.appendChild(cell_out)
    ui.appendNode(slider_div)
    await ui.pause('Done setting fuel!')
    fuel_slider.disabled = true
    cell_slider.disabled = true

    gs.fuseg = fuel_slider.valueAsNumber
    gs.futot -= gs.fuseg
    gs.ubreed = cell_slider.valueAsNumber
    gs.futot -= 5 * gs.ubreed
}

function doCalculations(gs: GameState): void {
    let eff = Math.min(54 - (gs.seg.stage) * 8 + gs.fuseg / 40, 104)  // efficiency

    const engine_fail = Math.random()
    if (engine_fail < 0.1) {
        gs.efail = 3 * engine_fail
        eff *= (1 - gs.efail)
    } else {
        gs.efail = 0
    }

    gs.rate = eff * 513.89                  // mph
    gs.distance += gs.seg.distance    // millions of miles
    gs.time = Math.floor(gs.seg.distance * 41667 / gs.rate)  // days
    gs.totime += gs.time                   // total trip time
    gs.fubr = Math.floor(16 + 18 * Math.random())
    gs.futot += gs.fubr * gs.ubreed          // new fuel from breeder
    const fuel_decay = Math.random()
    if (fuel_decay < 0.2) {                   // did fuel decay?
        gs.fudcy = Math.floor(fuel_decay * gs.futot)
    }
    else {
        gs.fudcy = 0     //  I think this fixes a bug in the original BASIC code
    }
    gs.futot -= gs.fudcy
}

async function travel(ui: UI, gs: GameState) {
    ui.section('')
    if (gs.efail > 0) {
        await banner(ui, 3, '* * ENGINE MALFUNCTION! * *', 'problem')
        ui.print(`You will have to operate your engines at a ${(gs.efail * 100).toFixed(2)}% reduction   
                      in speed until you reach ${trip[gs.seg.stage].place}.`)
        await ui.pause()
    }
    await banner(ui, 3, '* * Travelling * *')
}

async function endgame(ui: UI, gs: GameState) {
    ui.section('Neptune')
    ui.print(`You finally reached Neptune in ${fmt_days(gs.totime)}.
        Had your engines run at 100% efficiency the entire way, you would
        have averaged 51,389 mph and completed the trip in exactly 6 years.`)
    if (gs.totime <= 2220) {
        ui.printClass('centered', "Congratulations!  Outstanding job!")
    }
    else {
        const tm = gs.totime - 2190
        const years_over = Math.floor(Math.min(tm / 365, 3))
        const scale = ["excellent (room for slight improvement).",
            "quite good (but could be better).",
            "marginal (could do much better).",
            "abysmal (need lots more practice)."]
        ui.print(`Your trip took longer than this by ${fmt_days(tm)}.
            Your performance was ${scale[years_over]}`)
    }
    await ui.pause()
    if (gs.breed < 105) {
        ui.print(`I guess you realize that the return trip will be extremely
            chancy with only ${gs.breed} breeder reactor cells operational.`)
    } else {
        ui.print(`Fortunately you have ${gs.breed} operational breeder reactor cells
            for your return trip.  Very good.`)
    }
    const back_to_2 = Math.max(Math.floor(42250.0 / (8.0 + gs.futot / 40.0)), 405)
    ui.print(`With your remaining ${gs.futot} pounds of fuel and ${gs.breed} breeder
        cells, to get back to Theta 2 will take ${fmt_days(back_to_2)}.`)
    await ui.pause()
}

async function runGame(ui: UI) {
    await intro(ui)
    const gs = new GameState()
    for (let idx = 0; idx < trip.length - 1; idx++) {
        gs.seg = trip[idx]
        printConditions(ui, gs)
        await ui.pause('Press here to trade fuel....')
        await tradingInterface(ui, gs) // trading fuel for cells
        await enginePower(ui, gs) // how many pounds of fuel to use
        doCalculations(gs) // figure out how fast we went
        await travel(ui, gs)
    }
    await endgame(ui, gs)
}

export async function main(ui: UI) {
    while (true) {
        await runGame(ui)
        ui.section('Play Again?')
        await ui.pause('Press here to restart the game...')
        ui.clearScreen()
    }
}
