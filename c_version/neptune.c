#include<stdarg.h>
#include<time.h>
#include<stdlib.h>
#include<stdio.h>
#include<string.h>
#include<ncurses.h>

#define GM_WID 67
#define GM_HGT 23

#define stringify1(x) #x
#define stringify(x) stringify1(x)
#define percentage ((rand() % 100)/100.0)

static char buffer[GM_WID+1]; /* oh no, it's not ... thread safe! LOL */
static const char spc[] = " ";          /* just define it once here */
static int voffs = 0, hoffs = 0;        /* center the game 'window' */
static int game_cur_line = 0;           /* current last line in game buffer */

static void
kill_program (const char *msg)
{
  endwin ();
  fputs (msg, stderr);
  putc ('\n', stderr);
  exit (-1);
}

/* format the duration in days into a static buffer and
 * return it to the caller.  Yeah, it's not thread safe,
 * maybe I should re-write it in Rust(TM) LOL
 */
static char *
format_days(int days)
{
   static char fdbuff[50];
   int years = days / 365, jday = days % 365;
   float months = jday / 30.5;
   if(years > 0)
   {
      snprintf(fdbuff, 50, "%d year%s %0.2f months",
        years, 
	years == 1 ? "," : "s,", 
	months);
   } else {
      snprintf(fdbuff, 50, "%f months", months);
   }
   return fdbuff;
}

#define HEADING_COLOR COLOR_PAIR(1)|A_BOLD
#define DESC_COLOR COLOR_PAIR(2)
#define PROMPT_COLOR COLOR_PAIR(3)|A_BOLD
#define USER_COLOR COLOR_PAIR(4)
#define STAR_COLOR1 5           /* others are 6,7 */
static void
setup_palette (void)
{
  static const char msg[] = "problem setting up colors!";
  if (start_color () != OK)
    kill_program (msg);
  int err_count = 0;

  if (COLORS >= 256)
    {
      err_count += init_pair (1, 207, COLOR_BLACK) != OK;
      err_count += init_pair (2, 252, COLOR_BLACK) != OK;
      err_count += init_pair (3, 220, COLOR_BLACK) != OK;
      err_count += init_pair (4, 252, COLOR_BLACK) != OK;
      err_count += init_pair (5, 252, COLOR_BLACK) != OK;
      err_count += init_pair (6, 245, COLOR_BLACK) != OK;
      err_count += init_pair (7, 44, COLOR_BLACK) != OK;
    }
  else
    {
      err_count += init_pair (1, COLOR_MAGENTA, COLOR_BLACK) != OK;
      err_count += init_pair (2, COLOR_WHITE, COLOR_BLACK) != OK;
      err_count += init_pair (3, COLOR_YELLOW, COLOR_BLACK) != OK;
      err_count += init_pair (4, COLOR_WHITE, COLOR_BLACK) != OK;
      err_count += init_pair (5, COLOR_WHITE, COLOR_BLACK) != OK;
      err_count += init_pair (6, COLOR_YELLOW, COLOR_BLACK) != OK;
      err_count += init_pair (7, COLOR_BLUE, COLOR_BLACK) != OK;
    }
  if (err_count)
    kill_program (msg);
}

static void
write_heading (int line, const char *const msg)
{
  size_t mslen = strlen (msg) + 10;
  int spacing = (GM_WID - mslen + 1) / 2;
  char fmtstring[23]; /* "%999s~~([ %s ])~~%999s" */
  sprintf (fmtstring, "%%%ds~~([ %%s ])~~%%%ds", spacing, (int)(GM_WID - spacing - mslen));
  attrset (HEADING_COLOR);
  mvprintw (voffs + line, hoffs, fmtstring, spc, msg, spc);
}

/* clear from game-screen line `line` to the bottom of the game screen. */
static void
clear_game_tobot (int line)
{
  game_cur_line = line >= 2 ? line : 2;
  while (line < GM_HGT)
    mvprintw (voffs + line++, hoffs, "%" stringify (GM_WID) "s", spc);
}

static void
write_desc (const char *const msg, ...)
{
  va_list args;
  va_start(args,msg);
  vsnprintf(buffer, sizeof(buffer), msg, args);
  va_end(args);
  attrset (DESC_COLOR);
  mvprintw (voffs + game_cur_line++, hoffs, "%-" stringify (GM_WID) "s", buffer);
}

static void
write_prompt (const char *const msg, ...)
{
  va_list args;
  va_start(args,msg);
  vsnprintf(buffer, sizeof(buffer), msg, args);
  va_end(args);
  attrset (PROMPT_COLOR);
  /* a little wasteful writing over the line twice, but easier */
  mvprintw (voffs + game_cur_line, hoffs, "%" stringify (GM_WID) "s", spc);
  mvprintw (voffs + game_cur_line++, hoffs, "%s", buffer);
  attrset (USER_COLOR);
}

static void
write_instructions (const char *const msg)
{
  attrset (PROMPT_COLOR);
  mvprintw (voffs + GM_HGT - 1, hoffs, "%" stringify (GM_WID) "s", msg);
}

/* several times in the game you have to press a key to
 * continue... we'll get to that now
 */
static void
press_any_key(int clear_level)
{
  write_instructions("Press any key... ");
  move(voffs + GM_HGT - 1, hoffs + GM_WID - 1);
  refresh();
  getch();
  if(clear_level > 0) clear_game_tobot(clear_level);
  else write_instructions(" ");
}

static void
do_intro (void)
{
  static const char *intro_p1[] = {
    "     It is the Year 2100 and you are in command of the first manned",
    "spaceship to Neptune.  Manned space stations have been established",
    "which orbit Callisto, Titan, and Ariel, as well as at two inter-",
    "mediate points between Saturn and Uranus, and Uranus and Neptune.",
    "You must travel about 2700 million miles.  At an average speed of",
    "over 50,000 miles per hour, the entire trip should take about",
    "six years."
  };
  static const char *intro_p2[] = {
    "     Your spaceship is a marvel of 21st century engineering.  Since",
    "you may have to stop at space stations along the way, you will not",
    "be able to use the gravitational 'slingshot' effect of the planets.",
    "However, your engines are highly efficient using both energy from",
    "the sun captured by giant parabolic arrays and nuclear fuel carried",
    "on board.  You will not be able to carry enough fuel for the whole",
    "trip, so you also have a multi-celled nuclear breeder reactor",
    "(which takes spent fuel from your engines along with a small amount",
    "of primary fuel and turns it into a much greater amount of primary",
    "fuel)."
  };
  static const char *intro_p3[] = {
    "     The space stations along the way usually have a small stock of",
    "engine repair parts, breeder reactor cells, and nuclear fuel which",
    "are available to you on a barter basis."
  };

  write_heading (0, "S P A C E   V O Y A G E   TO   N E P T U N E");
  int lnum;
#define do_para(n) \
  game_cur_line = 2; \
  for(lnum = 0; lnum < sizeof(intro_p ## n)/sizeof(const char *); ++lnum) \
    write_desc(intro_p ## n[lnum]);  \
  while(lnum++ < 10) write_desc(" "); \
  press_any_key(-1)

  do_para (1);
  do_para (2);
  do_para (3);
#undef do_para
}

/* Make a random ASCII star-field! 
 * Avoid the columns on either side of the game text at `hoffs`
 */
static void
make_starfield (int cols, int rows)
{
  static const char stars[] = ".+*";
  int count = rows * cols / 30;
  for (int snum = 0; snum < count; ++snum)
    {
      int x = rand () % cols, y = rand () % rows;
      char c = stars[rand () % 3];
      attrset (COLOR_PAIR (STAR_COLOR1 + (rand () % 3)) | A_BOLD);
      if (x != hoffs - 1 && x != cols - hoffs + 1)
        mvaddch (y, x, c);
    }
}

/* **********************************************************************
 * G A M E   L O G I C
 * **********************************************************************
 */
static struct gm_segment {
   const char *location;
   int distance;
} trip[] = {
         {"Earth", 391}, {"Callisto", 403}, {"Titan", 446},
         {"Alpha 1", 447}, {"Ariel", 507}, {"Theta 2", 507},
         {"Neptune", 0}  
};

static struct gm_state {
        double rate;    /* rate of speed (last seg) */
        int totime;    /* total cumulative time  */
        int breed;     /* breeder-reactor cells */
        int futot;     /* fuel cells */

        int time;    /* time spent (last seg) */
        int ubreed;  /* used breeder cells (last seg) */
        int fubr;    /* fuel used per breeder cell (last seg) */
        int fudcy;   /* how much fuel decays (last seg) */

        int fuseg;      /* amount of fuel to use this segment */
        int seg;        /* segment of the trip */
        int distance;   /* distance travelled */
} game = {
 .breed = 120, .futot = 3000
};

static void
fuel_report(void)
{
    ++game_cur_line;
    write_desc("Pounds of of nuclear fuel ready for use: %d", game.futot);
    write_desc("Operational breeder reactor cells: %d", game.breed);
    ++game_cur_line;
}

static void
print_conditions(void)
{
    write_heading (0, trip[game.seg].location);
    write_desc("Current conditions are as follows:");
    write_desc("  Location: %s", trip[game.seg].location);
    write_desc("  Distance to Neptune: %d million miles.", 2701 - game.distance);
    if(game.seg > 0)
      {
        write_desc("  Distance from Earth: %d million miles.", game.distance);
	++game_cur_line;
        write_desc("Over the last segment, your average speed was %d mph", (int)game.rate);
        write_desc("  and you covered %d million miles in %d days.", trip[game.seg-1].distance, game.time);
        write_desc("Time est for this total distance: %s", format_days(0.81*game.distance));
        write_desc("Your actual cumulative time was: %s", format_days(game.totime));
        write_desc("You used %d cells which produced %d pounds of fuel each.", game.ubreed, game.fubr);
        if(game.fudcy > 0) 
           write_desc("%d pounds of fuel in storage decayed into an unusable state.", game.fudcy);
      }
    fuel_report();
}

static void
engine_power(void)
{
   write_desc("At this distance from the sun, your solar collectors can fulfill");
   write_desc("%d%% of the fuel requirements of the engines.  How many pounds", 
     56 - (game.seg+1)*8);
  write_desc("of nuclear fuel do you want to use on this segment?");

   int restart_level = game_cur_line; 
   int lbs = -1;  /* should be from 0 to game.futot */

   while(1)
     {
       game_cur_line = restart_level;
       write_prompt("Enter a number from 0 to %d: ", game.futot);
       scanw("%d", &lbs); 
       if(lbs >= 0 && lbs <= game.futot) break;
       write_instructions("Try again...");
     }
    write_instructions("");
    game.fuseg = lbs;
}

static void
breeder_usage(void)
{
    int operable = game.fuseg/20;
    int seedable = game.futot/5;
    int max_cells = game.breed > operable ? operable : game.breed;
    if(max_cells > seedable) max_cells = seedable;
    write_desc("How many breeder reactor cells do you want to operate?");
    int restart_level = game_cur_line; 
    int bu = -1; /* should be from 0 to min( game.breed, game.fuseg/20, futot/5 ) */
    /* if > breed  "You don't have that many cells." */
    /* if > fuseg/20 The spent fuel from your engines is only enough to operate {int(game.fuseg/20)}\n    breeder reactor cells.  Again please...') */
    /* if > futot/5  'You have only enough fuel to seed {int(game.futot/5)} breeder cells.\n    Please adust your number accordingly.') */
   while(1)
     {
       game_cur_line = restart_level;
       write_prompt("Enter a number from 0 to %d: ", max_cells);
       scanw("%d", &bu); 
       if(bu >= 0 && bu <= max_cells) break;
       write_instructions("Try again...");
     }
    write_instructions("");
    game.ubreed = bu;
}

static void
engine_malfunction(double reduction)
{
   write_desc("Engine malfunction (%f) !!!",reduction);
   /* TODO! */
}

/* calculate what happens next, after user input
 */
static void
calculate_results(void)
{
    /* eff is the engine efficiency */
    double eff = 54 - (game.seg+1)*8+game.fuseg/40;
    if(eff > 104) eff = 104; 
    double engine_fail = percentage; 
    if(engine_fail < 0.1)              /* 10% chance of engine problem */
    {
        double reduction = 3*engine_fail;
        engine_malfunction(reduction);
        eff *= (1-reduction);
    }
    game.rate = eff * 513.89;              /* mph */
    game.distance += trip[game.seg].distance;  /* millions of miles */
    game.time = (int)(trip[game.seg].distance * 41667 / game.rate);  /* days */
    game.totime += game.time;                  /* total trip time */
    game.fubr = (int)(16+18*percentage);
    game.futot += game.fubr*game.ubreed;     /* new fuel from breeder */
    double fuel_decay = percentage;
    game.fudcy = fuel_decay < 0.2 ? (int)(fuel_decay*game.futot) : 0;
    game.futot -= game.fudcy;
}

/* play one game round */
static void
one_segment(void)
{
    clear_game_tobot (0);
    print_conditions();  
    /* trade_fuel() */
    press_any_key(2);
    write_desc("After trading:");
    fuel_report();
    engine_power();
    game.futot -= game.fuseg;
    breeder_usage();
    game.futot -= 5*game.ubreed;
    calculate_results();
    ++game.seg;
    /* cls(8); */
    /* timed_banner(3, '* * Travelling * *', 0.5) */
    /* getch(); */
}

int
main (int argc, char *argv[])
{
  srand (time (NULL));
  initscr ();
  if (!has_colors ())
    kill_program ("Your terminal has no colors!");
  setup_palette ();
  bkgd (DESC_COLOR);
  erase ();
  /* set up the dimensions of our game window and draw a backdrop... */
  {
    int x, y;
    getmaxyx (stdscr, y, x);
    if (y < GM_HGT || x < GM_WID)
      kill_program ("Your terminal must be at least " stringify (GM_WID) "x"
                    stringify (GM_HGT) "!");
    voffs = (y - GM_HGT + 1) / 2, hoffs = (x - GM_WID + 1) / 2;
    make_starfield (x, y);
    clear_game_tobot (0);
  }

  /* give basic intro for the game */
  do_intro ();

  /* now let's play... */
  while(game.seg < sizeof(trip)/sizeof(struct gm_segment))
    one_segment();

  /* game over... */
  press_any_key(-1);
  erase ();
  endwin ();

  return 0;
}
