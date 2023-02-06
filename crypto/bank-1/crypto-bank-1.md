# Companion guide: Bank-1


Recall in `interception` I said that AES is a block cipher that always takes 16 bytes of input, what happens if we don't have exactly 16 bytes? What if we have more?

## The first block cipher mode: ECB

Block cipher modes are what allows you to do variable length encryption. Let's consider the most simple block cipher mode

Here's how you encrypt a variable number of bytes with ECB
1. Split it into a bunch of 16 byte messages and encrypt them all
2. Append it all together, and send it off

Simple right? What could possibly go wrong...

But what happens if we don't have an exact multiple of 16 bytes in our message? Well then we can add on some bytes at the end in a special format that we can easily recognize, these bytes are called "padding".

This is called Electronic Code Book, or ECB mode for short. It has a few glaring weaknesses, which you'll have to discover to solve the challenge!

## Tips

Within symmetric cryptography there are three major categories of exploits, one of which is a _chosen plaintext attack_. In a chosen plaintext attack you have control over what messages are encrypted. The idea behind chosen plaintext attacks is to send specific messages to somehow "leak" information that you're not supposed to have.

So in this problem, look at the source code and think about what information we don't have and then we want to leak. 

The answer is pretty straightforward: we want the pin of the admin user. 

We have no ability to access it directly but we see that this admin pin will be included in requests for money. So we know that we can encrypt messages that include the admin pin and in those messages we control the `recipient_id`.

What can we do with a message that gets encrypted? Recall that we have no way of decrypting it because we don't have the key. So what can we do with the ciphertexts? 

In summary those are the pieces of this problem: we have an encryption mode which encrypts each block in the same way, we have a pin that we would like to leak, we have the ability to somewhat affect the messages that get encrypted, and we get told what those ciphertexts are. Our goal is to recognize information leaked in the resulting ciphertexts.

Good luck!
