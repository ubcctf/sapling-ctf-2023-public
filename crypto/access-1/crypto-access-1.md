# Companion guide: Access-1

`bank-1` and `bank-2` feature chosen plaintext and ciphertext attacks, so this challenge will be looking at another category of symmetric exploit: The offline attack.

In this style of attack you're given a message that you know to be encrypted in a vulnerable way, so without having to communicate with any server or anything at all you can completely decrypt the message. This is the worst kind of cryptographic break because it means that whatever you did to encrypt your messages was completely broken!

## Tips

What do you need in order to decrypt the message?

`make_key` generates a key and then `encrypt` encrypts our message using two calls to `AES.encrypt()`. So since AES is secure, we need the key. But how can we get the key?

Look carefully at `make_key()`. What would we be missing if we wanted to generate the same key that's on the server? Evidently that would be `DATA`, since that's made up of random bytes. However we see that we do have all the other information that we would need to run the same `make_key()` and get the same key.

So if we wanted to generate the same key, it appears that we need `DATA`. But do we? The key question to ask is; do we need _all_ of the secret data? What parts of the secret data are actually used?

Good luck!

Hint: the percent sign is called a modulo operator, you should look up what it means if you don't know already