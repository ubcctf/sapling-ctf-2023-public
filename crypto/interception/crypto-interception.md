# Companion guide: Interception

Aside on guides
---

For some of the cryptography challenges in Sapling CTF we'll be providing you with some helpful background information and tips for how to solve the challenges. 

Since this is the first challenge, you'll be getting some more assistance than usual, later challenges won't be nearly as handhold-y! The main goal of this first challenge is to help you install the tools you'll need for later challenges. 

A big part of CTF challenges is being able to research, learn, and understand systems and attacks that you haven't seen before, so get ready for that later!

How does modern encryption work?
---

What do you do when you want to make a message secret? The most common solutions use something that's called a _block cipher_.

What is a block cipher? It's a function that takes 16 bytes and a key, and encrypts it. The standard block cipher, AES, is extremely extremely good at doing this. It's been analyzed and tested to hell and back and no one has been able to break it. How it works is a bit complicated so you don't need to worry about it.

As a quick example. With the key "catscatscatscats"
- The encryption of "mymessageiscool!" is 7560e6979e56348cfe27616e0ca8567b
- The encryption of "mymessageiscool?" is 59acdc0dbe8c2432c673bb05c2034c62
- See how the results are completely different even though the inputs are very similar? That's a security feature of AES!

**AES is secure in that if I gave you just "7560e6979e56348cfe27616e0ca8567b", you would have no idea what my original message was without the key.** But if you had the key, you can recover the original message just by running the decryption algorithm.

In `interception` you're given a few messages that were encrypted using AES. Which I just said would be impossible to recover without the key. 

I wonder what that slip of paper is for...

Tips
---

You could decrypt the messages using a tool manually, but you'll want to programatically be able to do AES operations for the later challenges: Check out [this](https://learn.microsoft.com/en-us/windows/python/web-frameworks) and [this](https://pycryptodome.readthedocs.io/en/latest/src/installation.html#compiling-in-linux-ubuntu) for information on installing `python` on Windows `WSL` and a cryptography library.

Once you have the tools installed, you'll have to write a program to actually do the decryption. This will involve a few steps
- Having all the messages you want to decrypt
  - This could be as simple as just copy pasting in the messages, or something more complex involving reading the file
- Converting from hexadecimal to a byte array
  - [https://docs.python.org/3/library/stdtypes.html#bytearray-objects](https://docs.python.org/3/library/stdtypes.html#bytearray-objects)
  - This is because most cryptography functions operate on bytes, not hex strings
- Calling the AES decryption function
  - [https://pycryptodome.readthedocs.io/en/latest/src/cipher/aes.html](https://pycryptodome.readthedocs.io/en/latest/src/cipher/aes.html)
  - You'll notice that for the AES functions it'll ask you for a "mode". Don't worry about it for now and put in `AES.MODE_ECB`