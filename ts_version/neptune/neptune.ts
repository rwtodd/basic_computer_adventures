/// <reference path="../js/bca.d.ts" />

/** Voyage to Neptune */
namespace Neptune {
    import AUI = AdventureUtils.UI

    const scenario = [
        `It is the Year 2100 and you are in command of the first manned
        spaceship to Neptune.  Manned space stations have been established
        which orbit Callisto, Titan, and Ariel, as well as at two inter-
        mediate points between Saturn and Uranus, and Uranus and Neptune.
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


    async function intro(ui: AUI) {
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

        fuseg = 0     // amount of fuel to use this segment
        rate = 0     // rate of speed (last seg)
        time = 0      // time spent (last seg)
        ubreed = 0    // used breeder cells (last seg)
        fubr = 0      // fuel used per breeder cell (last seg)
        fudcy = 0     // how much fuel decays (last seg)
    }

    function fmt_days(t:number):string {
        return "5 days"
    }

    function printConditions(ui: AUI, gs: GameState): void {
        ui.section(`${gs.seg.place}`)
        
        ui.print("Current conditions are as follows:")
        ui.print(`Location:  ${gs.seg.place}<br>
        Distance to Neptune: ${2701 - gs.distance} million miles.<br>
        Distance from Earth: ${gs.distance} million miles.`)
        if(gs.seg.stage > 1) {
            ui.print(`Over the last segment, your average speed was ${Math.floor(gs.rate)} mph,
                      and you covered ${trip[gs.seg.stage-2].distance} million miles in ${gs.time} days.`)
            ui.print(`Planned time for this total distance: ${fmt_days(0.81*gs.distance)}<br>
                      Your actual cumulative time was: ${fmt_days(gs.totime)}<br>
                      You used ${gs.ubreed} cells which produced ${gs.fubr} pounds of fuel each.`)
        
            if(gs.fudcy > 0) {
                ui.print(`${gs.fudcy} pounds of fuel in storage decayed into an unusable state.`)
            }
        }
    }

    async function banner(ui:AUI, n:number, msg:string) {
        for(let i = 0; i < n; i++) {
            ui.printClass('centered',msg)
            await ui.sleep(1.0)
        }
    }

    function tradingInterface(ui:AUI, gs:GameState) {
        return ui.pause(`Here's where the trading interface will be`)
    }

    function enginePower(ui:AUI, gs:GameState) {
        return ui.pause(`Here's where the engine power questions will be`)
    }

    function doCalculations(gs:GameState): void {
        // here's where we would calculate things
    }

    async function runGame(ui: AUI) {
        await intro(ui)
        const gs = new GameState()
        for(const seg of trip) {
            gs.seg = seg
            printConditions(ui,gs)
            await ui.pause('Press here to trade fuel....')
            await tradingInterface(ui,gs) // trading fuel for cells
            await enginePower(ui,gs) // how many pounds of fuel to use
            doCalculations(gs) // figure out how fast we went

            ui.section('')
            await banner(ui,3,'* * Travelling * *')
        }
    }

    export async function main(ui: AUI) {
        while (true) {
            await runGame(ui)
            ui.section('Play Again?')
            await ui.pause('Press here to restart the game...')
            ui.clearScreen()
        }
    }
}