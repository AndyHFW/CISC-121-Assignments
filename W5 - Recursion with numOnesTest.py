# This program for a recursion assignment.
# The program includes various functions that manipulate integers and strings.
# Use of loops and built-in functions other than len() is prohibited.

# Assignment 3 for CISC 121, Summer 2017
# Author: Andy Wang

'''
Counts the number of digits in an integer using recursion.
Parameter intInput is the integer of interest.
Returns 1 if |intInput|<10 or recursively counts additional digits.
Used in the breakApart() function.
'''
def numDigits(intInput):
    if intInput < 10 and intInput > -10:
        return 1
    return 1 + numDigits(intInput/10)

'''
Prints the digits of an integer individually.
Does not return any value.
'''
def breakApart(intInput):
    powTen=10**(numDigits(intInput)-1)
    if intInput!=0:
        print(intInput//powTen)
        breakApart(intInput%powTen)

'''
Counts the number of vowels in a string.
Parameter strInput is the string of interest.
Adds 1 if the first character is a vowel.
Ultimately returns the total number of digits
or 0 if the string is empty.
'''
def numVowels(strInput):
    if strInput=="":
        return 0
    else:
        newStr=strInput[1:]
        if (strInput[0]=="a" or strInput[0]=="e" or strInput[0]=="i" or
            strInput[0]=="o" or strInput[0]=="u"):
            return 1 + numVowels(newStr)
        else:
            return numVowels(newStr)

'''
Multiplies the numbers between n and m inclusive where n<=m.
Parameters n and m are integers.
Calculates product by recursively splitting numbers into two groups.
Returns the final product or None if n>m.
'''
def multiply(n,m):
    #print(n,m)
    if n>m:
        return None
    if n==m:
        return m
    return multiply(n,(n+m)//2)*multiply((n+m)//2+1,m)
'''
Counts the number of ones in the binary representation of an integer.

'''
def numOnes(intInput):
    if intInput==0:
        return 0
    else:
        if intInput%2==1:
            return 1 + numOnes(intInput//2)
        else:
            return numOnes(intInput//2)

'''
def numOnesTest(intput):
    strInput=format(intput,'b')
    counter=0
    for i in range(len(strInput)):
        if strInput[i]=="1":
            counter=counter+1
    return counter
'''

def tester():
  breakApart(54321)
  print()
  breakApart(987)
  print()
  breakApart(4)
  print()
  print(numVowels("mnsty"))
  print(numVowels(""))
  print(numVowels("annn"))
  print(numVowels("nnnnna"))
  print(numVowels("canoe"))
  print(multiply(4, 7))
  print(multiply(2, 10))
  print(multiply(8, 2))
  print(numOnes(128))
  print(numOnes(127))

tester()




