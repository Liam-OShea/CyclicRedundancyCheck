# File: CRC.py
# Author: Liam O'Shea B00613041
# a) Given a bit string, compute the CRC remainder and generate the bit string to be transmitted
# b) Given a bit string with CRC remainder appended, divide by G(X) to determine if message is error free
# c) Use these method in a test program which accepts G(X) and M(X), introduces random errors in P(X), and
#    demonstrate how receiver is able to detect the error.

import random

def cleanUpBits(order, bits):
    bits = bits[2:] # remove 0b
    while(len(bits) < order + 1):
        bits = "0" + bits
    return bits

def findMPrime(M, G):
    order = len(G) - 1
    # Add 0's to M(X) equal to order of G(X)
    for i in range(order):
        M = M + "0"
    return M

def findRemainder(M, G):
    size = len(G)
    order = size - 1

    keepDividing = True
    firstDivision = True
    dropIndex = len(G) # Index for bit to be brought down during long division
    result = ""
    numerator = ""
    zeros = ""

    # Create divisor of 0's for when most significant bit is 0
    for i in range(size):
        zeros += "0"

    # Main loop
    while keepDividing:

        # Get numerator from M'(X) if this is first divison
        if firstDivision:
            firstDivision = False
            numerator = M[:size]
        # Else get numerator from previous numerator and next digit from M'(X)
        else:
            numerator = numerator[1:] + M[dropIndex]
            dropIndex += 1

        # We will stop division process when we run out of new digits from M'(X)
        if dropIndex > len(M) - 1:
            keepDividing = False

        msb = numerator[0]
        if msb == "1":
            divisor = G
        else:
            divisor = zeros

        # Find result by using XOR operator between numerator and divisor.
        result = bin(int(numerator, 2) ^ int(divisor, 2))
        # Clean 0b from result and trim to correct number of bits.
        result = cleanUpBits(order, result)

        # Define numerator for next iteration as our result.
        numerator = result
    return result[1:]

def findPX(M, G):
    rem = findRemainder(findMPrime(M, G), G)
    px = M + rem
    return px

def isErrorFree(P, G):
    rem = findRemainder(P, G)
    return int(rem) != 0

# c) A program which accepts M(X) and G(X) from user, introduces random
# errors into P(X), and demonstrates receiver is able to detect error

def userProgram():
    M = input("Enter M(X): ")
    G = input("Enter G(X): ")
    P = findPX(M, G)
    Mp = findMPrime(M, G)
    print("Your M'(X) is: ", Mp)
    print("Your P(X) is:  ", P)
    R = findRemainder(P, G)
    print("Remainder of P(X)/G(X): " + R)
    print("Error Detected: ", isErrorFree(P, G))
    print("Introducing random errors to P(X)...")

    # Convert string to list so we can modify access characters with indices
    plist = list(P)
    # Flip up to 3 random bits within the string (Same index may be generated
    # multiple times).
    flipped = []
    for i in range(3):
        index = random.randint(0, len(plist) - 1)
        # Prevent reflipping
        if index not in flipped:
            flipped.append(index)
            if plist[index] == "0":
                plist[index] = "1"
            else:
                plist[index] = "0"

    P = ""
    P = P.join(plist)

    print("P(X) with Errors: ", P)
    print("Remainder of P(X)/G(X): ", findRemainder(P, G))
    print("Error Detected: ", isErrorFree(P, G))


userProgram()
