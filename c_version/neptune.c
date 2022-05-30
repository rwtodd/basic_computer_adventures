#include<stdarg.h>
#include<time.h>
#include<errno.h>
#include<stdlib.h>
#include<stdio.h>
#include<string.h>
#include<ncurses.h>

#define GM_WID 67
#define GM_HGT 23

#define stringify1(x) #x
#define stringify(x) stringify1(x)
#define percentage ((rand() % 100)/100.0)

static char buffer[GM_WID + 1]; /* oh no, it's not ... thread safe! re-write it in Rust LOL */
static const char spc[] = " ";  /* just define it once here */
static int voffs = 0, hoffs = 0;        /* center the game 'window' */
static int game_cur_line = 0;   /* current last line in game buffer */

/* in a few places we might kill the program... centralize that */
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
format_days (int days)
{
  static char fdbuff[50];
  int years = days / 365, jday = days % 365;
  float months = jday / 30.5;
  if (years > 0)
    snprintf (fdbuff, 50, "%d year%s %0.2f months",
              years, years == 1 ? "," : "s,", months);
  else
    snprintf (fdbuff, 50, "%0.2f months", months);
  return fdbuff;
}

/* some macros to help set colors the way ncurses wants us to */
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

/* draw a heading centered (usually at the top) */
static void
write_heading (int line, const char *const msg)
{
  size_t mslen = strlen (msg) + 10;
  int spacing = (GM_WID - mslen + 1) / 2;
  char fmtstring[23];           /* "%999s~~([ %s ])~~%999s" */
  sprintf (fmtstring, "%%%ds~~([ %%s ])~~%%%ds", spacing,
           (int) (GM_WID - spacing - mslen));
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

/* write a description line, and keep track of which line to write on next */
static void
write_desc (const char *const msg, ...)
{
  va_list args;
  va_start (args, msg);
  vsnprintf (buffer, sizeof (buffer), msg, args);
  va_end (args);
  attrset (DESC_COLOR);
  mvprintw (voffs + game_cur_line++, hoffs, "%-" stringify (GM_WID) "s",
            buffer);
}

/* write a prompt for a user response... usually followed by getch() or scanw() */
static void
write_prompt (const char *const msg, ...)
{
  va_list args;
  va_start (args, msg);
  vsnprintf (buffer, sizeof (buffer), msg, args);
  va_end (args);
  attrset (PROMPT_COLOR);

  /* a little wasteful writing over the line twice, but it's an easy way to clear
   * the line of any garbage...
   */
  mvprintw (voffs + game_cur_line, hoffs, "%" stringify (GM_WID) "s", spc);
  mvprintw (voffs + game_cur_line++, hoffs, "%s", buffer);

  /* go ahead an set up for the user to type */
  attrset (USER_COLOR);
}

/* put an instructional message at the bottom right */
static void
write_instructions (const char *const msg)
{
  attrset (PROMPT_COLOR);
  mvprintw (voffs + GM_HGT - 1, hoffs, "%" stringify (GM_WID) "s", msg);
}

/* from stackOverflow....
 * msleep(): Sleep for the requested number of milliseconds.
 */
static int
msleep (long msec)
{
  struct timespec ts;
  int res;

  if (msec < 0)
    {
      errno = EINVAL;
      return -1;
    }

  ts.tv_sec = msec / 1000;
  ts.tv_nsec = (msec % 1000) * 1000000;

  do
    {
      res = nanosleep (&ts, &ts);
    }
  while (res && errno == EINTR);

  return res;
}

/* run a banner down the screen, at timed intervals */
static void
timed_banner (int count, const char *const msg, int msecs)
{
  size_t mslen = strlen (msg) + 10;
  int spacing = (GM_WID - mslen + 1) / 2;
  char fmtstring[23];           /* "%999s~~([ %s ])~~%999s" */
  sprintf (fmtstring, "%%%ds*-*( %%s )*-*%%%ds", spacing,
           (int) (GM_WID - spacing - mslen));
  attrset (DESC_COLOR);
  clear_game_tobot (0);
  for (int idx = 0; idx < count; ++idx)
    {
      mvprintw (voffs + idx * 2, hoffs, fmtstring, spc, msg, spc);
      refresh ();
      msleep (msecs);
    }
}

/* several times in the game you have to press a key to
 * continue... we'll get to that now
 */
static void
press_any_key (int clear_level)
{
  write_instructions ("Press any key... ");
  move (voffs + GM_HGT - 1, hoffs + GM_WID - 1);
  refresh ();
  getch ();
  if (clear_level > 0)
    clear_game_tobot (clear_level);
  else
    write_instructions (" ");
}

/* put three screens of intro text in front of the user... */
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

/* ask a yes or no question until the user picks an option */
static int
y_or_n (const char *const prompt)
{
  int answer;
  int restart_level = game_cur_line;
  while (1)
    {
      game_cur_line = restart_level;
      write_prompt ("%s (Y/N)? ", prompt);
      answer = getch ();
      if (answer == 'y' || answer == 'Y' || answer == 'n' || answer == 'N')
        break;
      write_instructions ("Try again... Enter y or n");
    }
  return (answer == 'y' || answer == 'Y');
}

/* repeatedly ask for a number in a range [min,max] 
 * until the user provides one. 
 */
static int
get_user_number (const char *const prompt, int min, int max)
{
  int restart_level = game_cur_line;
  int answer = min - 1;
  while (1)
    {
      game_cur_line = restart_level;
      write_prompt ("%s (%d to %d)? ", prompt, min, max);
      scanw ("%d", &answer);
      if (answer >= min && answer <= max)
        break;
      write_instructions ("Try again...");
    }
  write_instructions ("");
  return answer;
}


/* **********************************************************************
 * G A M E   L O G I C
 * **********************************************************************
 */
static struct gm_segment
{
  const char *location;
  int distance;
} trip[] = {
  {"Earth", 391}, {"Callisto", 403}, {"Titan", 446},
  {"Alpha 1", 447}, {"Ariel", 507}, {"Theta 2", 507},
  {"Neptune", 0}
};

static struct gm_state
{
  double rate;                  /* rate of speed (last seg) */
  int totime;                   /* total cumulative time  */
  int breed;                    /* breeder-reactor cells */
  int futot;                    /* fuel cells */

  int time;                     /* time spent (last seg) */
  int ubreed;                   /* used breeder cells (last seg) */
  int fubr;                     /* fuel used per breeder cell (last seg) */
  int fudcy;                    /* how much fuel decays (last seg) */

  int fuseg;                    /* amount of fuel to use this segment */
  int seg;                      /* segment of the trip */
  int distance;                 /* distance travelled */
} game = {
  .breed = 120,.futot = 3000
};

/* In a few places we like to report on fuel */
static void
fuel_report (void)
{
  ++game_cur_line;
  write_desc ("Pounds of of nuclear fuel ready for use: %d", game.futot);
  write_desc ("Operational breeder reactor cells: %d", game.breed);
  ++game_cur_line;
}

/* describe a new location */
static void
print_conditions (void)
{
  write_heading (0, trip[game.seg].location);
  write_desc ("Current conditions are as follows:");
  write_desc ("  Location: %s", trip[game.seg].location);
  write_desc ("  Distance to Neptune: %d million miles.",
              2701 - game.distance);
  if (game.seg > 0)
    {
      write_desc ("  Distance from Earth: %d million miles.", game.distance);
      ++game_cur_line;
      write_desc ("Over the last segment, your average speed was %d mph",
                  (int) game.rate);
      write_desc ("and you covered %d million miles in %d days.",
                  trip[game.seg - 1].distance, game.time);
      ++game_cur_line;
      write_desc ("Time est for this total distance: %s",
                  format_days (0.81 * game.distance));
      write_desc ("Your actual cumulative time was: %s",
                  format_days (game.totime));
      ++game_cur_line;
      write_desc ("You used %d cells which produced %d pounds of fuel each.",
                  game.ubreed, game.fubr);
      if (game.fudcy > 0)
        write_desc
          ("%d pounds of fuel in storage decayed into an unusable state.",
           game.fudcy);
    }
  fuel_report ();
}

/* find out how much fuel to burn */
static void
engine_power (void)
{
  write_desc
    ("At this distance from the sun, your solar collectors can fulfill");
  write_desc
    ("%d%% of the fuel requirements of the engines.  How many pounds",
     56 - (game.seg + 1) * 8);
  write_desc ("of nuclear fuel do you want to use on this segment?");

  int restart_level = game_cur_line;
  game.fuseg = get_user_number ("Fuel to use", 0, game.futot);
}

/* find out how many breeders to operate */
static void
breeder_usage (void)
{
  int operable = game.fuseg / 20;
  int seedable = game.futot / 5;
  int max_cells = game.breed > operable ? operable : game.breed;
  if (max_cells > seedable)
    max_cells = seedable;
  ++game_cur_line;
  write_desc ("There are %d breeder cells here.", game.breed);
  write_desc
    ("The spent fuel from the engines can operate up to %d cells, and",
     operable);
  write_desc ("  you have enough fuel to seed up to %d cells.", seedable);
  write_desc ("How many breeder reactor cells do you want to operate?");
  int restart_level = game_cur_line;
  game.ubreed = get_user_number ("Cells to operate", 0, max_cells);
}

/* inform the user of engine trouble! */
static void
engine_malfunction (double reduction)
{
  timed_banner (10, "* * ENGINE MALFUNCTION!!! * *", 150);
  clear_game_tobot (6);

  write_desc ("You will have to operate your engines at a %d%% reduction.",
              (int) (reduction * 100));
  write_desc ("in speed until you reach %s.", trip[game.seg + 1].location);
  press_any_key (0);
}

/* calculate what happens next, after user input
 */
static void
calculate_results (void)
{
  /* eff is the engine efficiency */
  double eff = 54 - (game.seg + 1) * 8 + game.fuseg / 40;
  if (eff > 104)
    eff = 104;
  double engine_fail = percentage;
  if (engine_fail < 0.1)        /* 10% chance of engine problem */
    {
      double reduction = 3 * engine_fail;
      engine_malfunction (reduction);
      eff *= (1 - reduction);
    }
  game.rate = eff * 513.89;     /* mph */
  game.distance += trip[game.seg].distance;     /* millions of miles */
  game.time = (int) (trip[game.seg].distance * 41667 / game.rate);      /* days */
  game.totime += game.time;     /* total trip time */
  game.fubr = (int) (16 + 18 * percentage);
  game.futot += game.fubr * game.ubreed;        /* new fuel from breeder */
  double fuel_decay = percentage;
  game.fudcy = fuel_decay < 0.2 ? (int) (fuel_decay * game.futot) : 0;
  game.futot -= game.fudcy;
}

/* trade fuel for breeder cells, or vice-versa */
static void
trade_fuel ()
{
  int trade = 150 + (int) (80 * percentage);
  if (!game.seg)
    write_desc
      ("Before leaving, you can trade fuel for breeder reactor cells at");
  else
    write_desc ("Here at %s, breeder cells and nuclear fuel trade at",
                trip[game.seg].location);
  write_desc ("the rate of %d pounds of fuel per cell.", trade);
  fuel_report ();
  if (game.futot - trade > 1500)
    {
      if (y_or_n ("Would you like to procure more breeder cells"))
        {
          write_desc
            ("You must leave at least 1500 pounds of fuell to run the engines.");
          int ncells = get_user_number ("How many cells do you want",
                                        0,
                                        (1501 - game.futot) / -trade);
          game.futot -= ncells * trade, game.breed += ncells;
          return;               /* done trading! */
        }
    }
  else
    write_desc ("You have too little fuel to trade.");

  if (game.breed > 50)
    {
      if (y_or_n ("Would you like to trade breeder cells for fuel"))
        {
          write_desc
            ("You must leave at least 50 cells to operate the reactor.");
          int ncells = get_user_number ("How many cells to trade",
                                        0,
                                        game.breed - 50);
          game.breed -= ncells, game.futot += ncells * trade;
        }
    }
  else
    write_desc ("You don't have enough fuel cells to trade.");
}

/* play one game round */
static void
one_segment (void)
{
  clear_game_tobot (0);
  print_conditions ();
  press_any_key (2);
  trade_fuel ();
  press_any_key (2);
  write_desc ("After trading:");
  fuel_report ();
  engine_power ();
  game.futot -= game.fuseg;
  breeder_usage ();
  game.futot -= 5 * game.ubreed;
  calculate_results ();
  ++game.seg;

  timed_banner (10, " * * Travelling * * ", 200);
}

/* print final stats... */
static void
endgame (void)
{
  clear_game_tobot (0);
  write_heading (0, "* * N E P T U N E ! * *");
  write_desc ("You finally reached Neptune in %s.",
              format_days (game.totime));
  write_desc
    ("Had your engines run at 100%% efficiency the entire way, you would");
  write_desc
    ("have averaged 51,389 mph and completed the trip in exactly 6 years.");
  game_cur_line++;
  if (game.totime <= 2220)
    write_heading (game_cur_line, "Congratulations!  Outstanding job!");
  else
    {
      static const char *const scale[] = {
        "excellent (room for slight improvement).",
        "quite good (but could be better).",
        "marginal (could do much better).",
        "abysmal (need lots more practice)."
      };

      int tm = game.totime - 2190;
      write_desc ("Your trip took longer than this by %s", format_days (tm));
      game_cur_line++;
      int years_over = tm / 365;
      if (years_over > 3)
        years_over = 3;
      write_desc ("Your performance was %s", scale[years_over]);
    }
  game_cur_line++;
  if (game.breed < 105)
    {
      write_desc
        ("I guess you realize that the return trip will be extremely");
      write_desc ("chancy with only %d breeder reactor cells operational.",
                  game.breed);
    }
  else
    {
      write_desc ("Fortunately you have %d operational breeder reactor cells",
                  game.breed);
      write_desc ("for your return trip.  Very good.");
    }
  game_cur_line++;
  int back_to_2 = (int) (42250.0 / (8.0 + game.futot / 40.0));
  if (back_to_2 < 405)
    back_to_2 = 405;
  write_desc ("With your remaining %d pounds of fuel and %d breeder",
              game.futot, game.breed);
  write_desc ("cells, to get back to Theta 2 will take %s.",
              format_days (back_to_2));
  game_cur_line++;
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

  while (1)
    {
      /* now let's play... */
      while (game.seg < sizeof (trip) / sizeof (struct gm_segment) - 1)
        one_segment ();
      endgame ();
      if (!y_or_n ("Play again"))
        break;

      /* reset for next game */
      memset (&game, 0, sizeof (struct gm_state));
      game.breed = 120, game.futot = 3000;
    }

  /* no more games... */
  erase ();
  endwin ();

  return 0;
}

/* vim: sw=2 sts=2 expandtab cindent cinoptions={1s formatoptions=jcroql
 */
