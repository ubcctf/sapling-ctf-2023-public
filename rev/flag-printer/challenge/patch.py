# this file generates an intentionally broken binary with selected instructions replaced by hlts, which should be pretty obvious both statically and dynamically
# (valgrind complains about illegal opcode, and otherwise segfaults at hlt under a debugger)
# the idea of this challenge is to break decompilation so that relying on it won't get you far
# people have 2 paths they can approach this:
#  - either figure out what the function on assembly level (or stitch together decompilations) by ignoring the missing instructions, and reimplement
#  - or figure out what the broken instructions are supposed to do by understanding the context around it (argument setting, stack frame setup, etc), and patch
# for those going the first route (which i assume most would), even though no disassemblers are willing to disassemble code after hlt (IDA seems to be hit the hardest with it completely considering the function as a byte array instead),
# i would assume eventually people would be able to figure out that they can manually disassemble after the hlt'd instructions, which would actually give them quite a bit of good decompilation,
# but is where the stripped, statically linked code with indirect references comes into play
# since most people probably won't utilize any function identification libraries with which they can trivially obtain the library functions' names (which is itself a high level overview of the function)
# whereas if they go the patch route, they will have to have a pretty good understanding of how x86 ABI work, along with debugging skills since it's likely that people won't get the patches right the first time
# which should make this a level playing field hopefully

import re

patches = {
    b'\x55\x48\x89\xE5\x48\x83\xEC\x60': 1,                       #main() callee prologue - if someone has stared at x86 asm before they'd realize push rbp is missing since its in basically every function
    b'\x48\x89\xC6\xBF....\xB8\x00\x00\x00\x00': 3,               #calling convention (argument registers for printf() in main) - mov rdi, rax is gone but should be really obvious that's the format string argument to printf
    b'\xC3\x0F\x1F\x80\x00\x00\x00\x00\xB8\x01\x00\x00\x00': 1,   #l64a's ret instruction as a trivial patch deterrent (doesnt affect decompilation)
}


with open('flagprinter', 'r+b') as b:
    data = b.read()

    #write backup as usual
    with open('flagprinter.bak', 'wb') as bak:
        bak.write(data)


    #apply all patches
    patched = data
    for search, size in patches.items():
        addr = re.search(search, data).start()
        patched = patched[:addr] + b'\xF4'*size + patched[addr+size:]

    #reset and overwrite
    b.seek(0)
    b.write(patched)