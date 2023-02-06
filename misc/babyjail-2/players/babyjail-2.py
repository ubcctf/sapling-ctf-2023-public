import code, os

#not the actual flag! connect to the remote endpoint to leak the real one.
flag = 'maple{FAKEFLAG}'

del flag
os.setuid(1000)

code.interact()