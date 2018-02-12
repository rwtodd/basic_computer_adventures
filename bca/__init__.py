# init file  --  put infrastructure that all
# the games will use in here...

def centered(txt: str) -> str:
    """center text assuming 70-columns"""
    front_space = ' '*( (70 - len(txt))//2 )
    return front_space + txt

class CheckedInput:
    def __init__(self, prompt, ntype):
        self.prompt = prompt
        self.ntype = ntype
        self.checks = []
        self.pre_proc = None
    def ensure_nonneg(self, msg="Expected a positive number, or zero."):
        self.ensure_morethan(-1, msg)
    def ensure_lessthan(self, n, msg):
        self.checks.append( (lambda x: x < n, msg) )
    def ensure_morethan(self, n, msg):
        self.checks.append( (lambda x: x > n, msg)  )
    def choices(self, lst, msg):
        self.checks.append( ( lambda x: x in lst , msg)  )
    def ensure(self, check, msg):
        self.checks.append( (check, msg) )
    def pre_process(self,f):
        self.pre_proc = f
    def keep_letters(self, n):
        self.pre_proc = lambda s: s.strip().upper()[:n]
    def run(self):
        while True:
            resp = input(self.prompt)
            try:
               n = self.ntype(resp)
               if self.pre_proc:
                   n = self.pre_proc(n)
               ok = True
               for check, msg in self.checks:
                   if not check(n):
                       if callable(msg): msg = msg(n)
                       print(msg) 
                       ok = False
                       break
               if ok:             # passed all the checks!
                   return n 
            except ValueError:
               if   self.ntype == int: print('An integer is expected here.') 
               elif self.ntype == float: print('A number is expected here.')
               else: print("That wasn't the type of value expected here.")

def cls(n = 80) -> None:
    """clear the screen via printing lots of newlines"""
    print('\n'*n,end='')

def pause(msg='Press <return> to continue....'):
    input(msg)

def plural(n: int, thing: str, add='s', alternate=None) -> str:
    if n == 1:  return f'1 {thing}'
    if alternate: return f'{n} {alternate}'
    return f'{n} {thing}{add}'

def said_y(prompt: str) -> bool:
    """Ask a y/n question and return True if they said yes"""
    ci = CheckedInput(prompt, str)
    ci.keep_letters(1)
    ci.choices("YN", "Please enter 'y' or 'n'.")
    return ci.run() == 'Y'

