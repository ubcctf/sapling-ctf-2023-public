import sys, os

#a dict that always returns None
class nulldict(dict):
    def get(self, key, default):
        return None
    def __getitem__(self, __key):
        return None

os.setuid(1000)

#clear sys.modules to prep for setting sys.modules to always return None
for k in sys.modules.copy().keys():
    sys.modules.pop(k)

del sys.modules

sys.modules = nulldict()

del sys, os

#not the actual flag! connect to the remote endpoint to leak the real one.
flag = 'maple{FAKEFLAG}'

#you only get one line this time!
exec(input('>>> '), {}, {})