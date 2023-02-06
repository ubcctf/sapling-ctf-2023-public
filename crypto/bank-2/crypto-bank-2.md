# Companion guide: Bank-2

## A new block cipher mode

In the last bank challenge we saw that `ECB` mode is very vulnerable and messages can be trivially recovered, so in this challenge we'll look at the successor to `ECB`, Cipher Block Chaining, aka `CBC`.

You can learn more about CBC [here](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Cipher_block_chaining_(CBC))

## Tips

In this challenge you're given access to a function that will decrypt any ciphertext you give it, meaning this is _chosen ciphertext attack_.

What happens when you send a ciphertext? One of three things

1. The decrypted message is correctly formatted and you get a "Email recieved" message
2. The decrypted message is incorrectly formatted and ydou get a "Email is corrupted" message
3. The decryption fails and you get a stacktrace

So you can ask it to decrypt anything, but it'll never show you any decryption results, so what can you do?

It turns out that telling the attacker whether or not a given decrypted message is corrupted is enough information to *fully* recover any message.

This is a very famous attack and the ideas behind that attack will be very helpful in solving this challenge, so step one will be to research that attack. To make things harder, this challenge features a slightly modified version of typical AES-CBC, so you'll have to adapt that attack to work on this challenge

Good luck!