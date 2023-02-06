#see patch.py for more information
import subprocess, re


patches = {
    b'\xF4\x48\x89\xE5\x48\x83\xEC\x60': b'\x55',                        #push rbp
    b'\xF4\xF4\xF4\xBF....\xB8\x00\x00\x00\x00': b'\x48\x89\xC6',        #mov rsi, rdx
    b'\xF4\x0F\x1F\x80\x00\x00\x00\x00\xB8\x01\x00\x00\x00': b'\xC3',    #ret
}


with open('flagprinter', 'rb') as b:
    data = b.read()


patched = data
for search, patch in patches.items():
    addr = re.search(search, data).start()
    patched = patched[:addr] + patch + patched[addr+len(patch):]


with open('flagprinter-solve', 'wb') as s:
    s.write(patched)

print(subprocess.Popen(['./flagprinter-solve'], stdout=subprocess.PIPE).communicate()[0].decode(), end='')