# Companion guide: Access-2

Looking at the new source we see that the exploit we used in last challenge won't work. We now theoretically would need the entire secret data in order to generate the key. However the rest of the code is almost exactly the same.

So now we're unable to generate the same key, but is there another way we can get the key? What if we try to guess what the key is?

`key` is four bytes, so we could test every possible 4 byte value, plug it into a decryption function, and see if we get a message back. But we would have to test 2^31 or 2147483648 guesses on average before we would get it correct. That's way too many!

What exactly is `key` used for? `key` is used to generate `key_one` and `key_two`, which are each used encrypting the message.

So maybe we can try to guess `key_one` and `key_two`?

We could, but how would we be able to check if our answer was right? Unlike before, we can't just decrypt using one of the keys, because we need both to get back the original message. That leaves us back where we started.

But theoretically, if there was some way we could somehow know if our guesses were correct, then this would work wouldn't it?

If only there was a way...

Good luck!


PS: Some general CTF advice, if two challenges in a series have almost the same source code, `diff` them and assume that any differences are important to the new challenge and it's solution.
