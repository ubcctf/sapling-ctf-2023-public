#!/usr/bin/env python3

from Crypto.Cipher import AES 
import os 
from random import randint
from secrets import FLAG

# ======= AES and ECB stuff =======
key = os.urandom(16) # This is 16 bytes of cryptographically random data, there's no way you can bruteforce or guess this
cipher = AES.new(key, AES.MODE_ECB)

# pads the message to a multiple of 16 bytes
def pad(msg):
    bytes_of_padding = (16 - len(msg)) % 16
    pad_bytes = bytes([bytes_of_padding]) # creates a single byte that has the numerical value of the number of bytes of padding you want
                                          # this padding scheme is called PKCS, don't worry about it, just know it pads the message to 16 bytes
    return msg + pad_bytes * bytes_of_padding

# strip the padding off
# don't worry about this function
def strip_padding(block):
    last = block[-1]
    if last < 16 and all([last == b for b in block[-1 * last:]]):
        # we have a padded msg, strip it off
        return block[:-1*last]
    else:
        # no padding
        return block

# splits the message into 16 byte chunks
# msg must be a multiple of 16 bytes long
def blockify(msg):
    blocks = []
    for i in range(0,len(msg),16):
        blocks.append(msg[i:i+16])
    return blocks

def encrypt_debug(ptxt):
    print(f"[+] Encrypting {ptxt}")

    msg = pad(ptxt)
    print(f"[+] Padded the message out to {msg}")

    blocks = blockify(msg)
    print(f"[+] Splitting into blocks for ECB")
    for i,block in enumerate(blocks):
        print(f"[+] Block #{i+1}: {block}")

def encrypt(ptxt):
    msg = pad(ptxt)
    blocks = blockify(msg)
    enc_blocks = [cipher.encrypt(block) for block in blocks]
    result = b"".join(enc_blocks)
    return result

def decrypt(ctxt):
    ctxt_blocks = blockify(ctxt)
    ptxt_blocks = [cipher.decrypt(block) for block in ctxt_blocks]
    ptxt_blocks[-1] = strip_padding(ptxt_blocks[-1])
    result = b"".join(ptxt_blocks)
    return result

ADMIN_ID = 0
USER1_ID = 1
USER2_ID = 2

ADMIN_PIN = randint(100000, 999999)

users = {
    ADMIN_ID: [ADMIN_PIN, 100_000_000],
    USER1_ID: [1111, 1000],
    USER2_ID: [2222, 1000]
}

def debug_transaction(sender_id, recipient_id, sender_pin, amount):
    # Authors note: This is just to help with debugging
    if sender_pin == ADMIN_PIN:
        debug = f"{sender_id}|{recipient_id}|??????|{amount}".encode()
    else:
        debug = f"{sender_id}|{recipient_id}|{sender_pin}|{amount}".encode()
    
    encrypt_debug(debug)

def send_money(sender_id, recipient_id, sender_pin, amount):
    debug_transaction(sender_id, recipient_id, sender_pin, amount)
    
    transaction = f"{sender_id}|{recipient_id}|{sender_pin}|{amount}"
    receipt = encrypt(transaction.encode())
    print(f"Your receipt: {receipt.hex()}")

    transaction = decrypt(receipt)

    if (sender_id not in users) or (recipient_id not in users):
        print("Invalid sender or recipient id")
        return receipt

    if users[sender_id][0] != sender_pin:
        print(f"Invalid sender pin")
        return receipt

    if amount > users[sender_id][1]:
        print(f"Insufficient balance")
        return receipt
    
    if amount < 0:
        print(f"Can't send a negative amount")
        return receipt

    users[sender_id][1] -= amount
    users[recipient_id][1] += amount

    print(f"Transaction successful: sent {amount} from user {sender_id} to user {recipient_id}")
    return receipt

def request_money(recipient_id):
    return send_money(ADMIN_ID, recipient_id, ADMIN_PIN, 50)


def purchase_flag():
    if users[USER1_ID][1] < 100_000:
        print(f"Sorry, this flag is too expensive for you to afford (just like living in Vancouver)")
        return False

    print(f"Your flag is {FLAG}, thank you for your purchase!")
    return True
    

menu = """Welcome to the Electronic Code Bank or ECB for short!
Options:
  1. Send money
  2. Request some money
  3. Purchase flag
  4. Check savings"""



def main():
    remaining_requests = 100
    while remaining_requests > 0:
        print(menu)
        option = int(input("> "))
        if option == 1:
            sender_id = int(input("Input sender id: "))
            recipient_id = int(input("Input recipient id: "))
            sender_pin = int(input("Input sender PIN: "))
            amount = int(input("Input amount: "))
            
            send_money(sender_id, recipient_id, sender_pin, amount)

        elif option == 2:
            if remaining_requests > 0:
                recipient_id = int(input("Input recipient id: "))
                request_money(recipient_id)
            else:
                print("Sorry! You've used up all of your requests for money.")

        elif option == 3:
            purchase_flag()
        elif option == 4:
            for id in users.keys():
                print(f"User {id} has balance {users[id][1]}")
        else:
            print("Invalid option")

        remaining_requests -= 1
        print()

if __name__ == "__main__":
    main()