import code, os

flag = 'maple{gc_0r_m3m_dump?}'

del flag
os.setuid(1000)

code.interact()