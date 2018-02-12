# Orient Express Mystery


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


