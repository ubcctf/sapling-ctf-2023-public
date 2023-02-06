import gc, functools

for s in functools.reduce(list.__add__, [i for i in gc.get_objects() if 'maple' in str(i) and isinstance(i, list)]):
    if isinstance(s, str) and s.startswith('maple'):
        print(s)