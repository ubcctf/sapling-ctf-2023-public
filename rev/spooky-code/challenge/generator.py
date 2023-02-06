import random

flag = b'maple{sP0oKy_s3lf_m0d1fy1ng_c0de_4pp34r1ng_0ut_0f_n0wh3r3}'


"""
#start generator code for each character (total length exactly 0x20 for aligning vmovups)
cmp BYTE PTR [rdi], 0x6d    #flag checker
jne fail                    #if fail just return
inc rdi                     #else increment to the next character in string
vmovups ymm1, [rax]         #copy generator code
add rax, 0x20               #point to ret to replace
mov ebx, [rax]              #copy next flag character masked by the current character (4 bytes in total to test, since the character itself can be 0x0 even if it's not the end yet)
test ebx, ebx               #check if all 4 bytes are zero (signifying the end)
je next+4                   #skip to finalizing code if end is found
vmovups [rax], ymm1         #write generator code
xor [rax+2], bl             #reveal next flag character
jmp next                    #dont return
fail:
ret
next:
"""
output = [hex(i) for i in bytes.fromhex('803F6D751A48FFC7C5FC10084883C0208B1885DB740EC5FC1108305802EB01C3')]


#random bytes + the flag character masked inside
for i, c in enumerate(flag[1:]):    #generator includes the character "m" already
    output.append(hex(c ^ flag[i]))
    output += [hex(i) for i in random.randbytes(31)]

"""
#last chunk to signify everything passed
mov rdi, rdx   #move correct string into rdi (first arg for puts)
push rbx       #push 0 onto stack (and also align stack)
call rsi       #call puts (second arg when calling shellcode) *might crash if not 16 byte aligned due to movaps
pop rax        #set rax to 0 and reset frame
leave          #avoid continue running main
ret            #terminate
"""
#+4 null bytes to signify end
output += ['0x00']*4 + [hex(i) for i in bytes.fromhex('4889D753FFD658C9C3')]


print('char data[] = {' + ", ".join(output) + "};")
print('size:', len(output))  #for checking if mmap size is enough
