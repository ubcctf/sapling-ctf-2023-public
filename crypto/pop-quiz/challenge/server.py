#!/usr/bin/env python3
from Crypto.Util.number import getPrime
from secrets import flag
import math

messages = [
    "Let's start with some modular arithmetic, one of the core concepts behind cryptography.",
    "Not so bad, right? Let's try again with some larger numbers.",
    "Now, let's practice some exponentiation.",
    "Since the result of exponentiation grows very fast, we usually consider numbers modulo some value.",
    "If you implemented exponentiation with repeated multiplication, you'll need to find a different way this time!",
    "Two more questions left! Previously, we calculated the value of (x ^ y modulo p). Now, let's flip it around:",
    "The problem of finding the exponent in (x ^ y == result modulo p) is known as the Discrete Logarithm Problem. It's a lot harder to solve than simply finding the value of (x ^ y modulo p)!"
]

def challenge1():
    x = getPrime(16)
    modulo = getPrime(4)
    print(f"1. What is the value of {x} modulo {modulo}?")
    user_input = int(input(">>> ").strip())
    assert user_input == x % modulo

def challenge2():
    x = getPrime(128)
    modulo = getPrime(64)
    print(f"2. What is the value of {x} modulo {modulo}?")
    user_input = int(input(">>> ").strip())
    assert user_input == x % modulo

def challenge3():
    x = getPrime(10)
    y = getPrime(4)
    print(f"3. Find the value of {x} ^ {y}. Note: the caret [^] refers to exponentiation.")
    user_input = int(input(">>> ").strip())
    assert x ** y == user_input

def challenge4():
    modulo = getPrime(16)
    x = getPrime(16)
    y = getPrime(16)
    print(f"4. Find the value of {x} ^ {y} modulo {modulo}")
    user_input = int(input(">>> ").strip())
    assert pow(x, y, modulo) == user_input

def challenge5():
    modulo = getPrime(64)
    x = getPrime(32)
    y = getPrime(32)
    print(f"5. Find the value of {x} ^ {y} modulo {modulo}")
    user_input = int(input(">>> ").strip())
    assert pow(x, y, modulo) == user_input

def challenge6():
    modulo = getPrime(6)
    x = getPrime(6)
    while math.gcd(x, modulo) != 1:
        x = getPrime(6)

    y = getPrime(6)
    while math.gcd(y, modulo) != 1:
        y = getPrime(6)

    result = pow(x, y, modulo)

    print(f"6. What value of y satisfies: {x} ^ y == {result} modulo {modulo}? (You can enter any such y value)")
    user_input = int(input(">>> ").strip())
    assert pow(x, user_input, modulo) == result



def challenge7():
    modulo = getPrime(32)
    x = getPrime(32)
    while math.gcd(x, modulo) != 1:
        x = getPrime(32)
        
    y = getPrime(32)
    while math.gcd(y, modulo) != 1:
        y = getPrime(32)

    result = pow(x, y, modulo)
    print(f"7. What value of y satisfies: {x} ^ y == {result} modulo {modulo}? (You can enter any such y value)")
    user_input = int(input(">>> ").strip())
    assert pow(x, user_input, modulo) == result

challenges = [challenge1, challenge2, challenge3, challenge4, challenge5, challenge6, challenge7]
NUM_CHALLENGES = len(challenges)

START_MESSAGE = f"""
Welcome to the pop quiz! Progress through these {NUM_CHALLENGES} challenges for a special treat.

Here are some useful resources that may help you along the way:
- khanacademy.org/computing/computer-science/cryptography/modarithmetic/a/what-is-modular-arithmetic
- brilliant.org/wiki/modular-arithmetic/
- artofproblemsolving.com/wiki/index.php/Modular_arithmetic/Introduction

We'd also recommend Python for working with the large numbers coming up!
"""
if __name__ == "__main__":
    print(START_MESSAGE)
    for i in range(NUM_CHALLENGES):
        print(messages[i])
        # Repeat the challenge until the user responds correctly
        while True:
            try:
                challenges[i]()
                print()
                break
            except ValueError:
                print("Please input an integer")
                print()
            except AssertionError:
                print("Incorrect answer")
                print()
            except Exception:
                print("Something unexpected occured, please try again and let the organizers know")
                exit()

            print()

    print("Congratulations! Here's your flag:", flag)