# This program plays the Crown and Anchor game, a game in which
# players bet money on a spinning wheel with various symbols.
# The game continues until only one player remains.

# For CISC 121, Summer 2017
# Author: Andy Wang

from random import randint

'''
Spins the wheel by randomly selecting three symbols
The possible symbols are hearts, spades, diamonds, clubs, crowns, and anchors
    0 = hearts
    1 = spades
    2 = diamonds
    3 = clubs
    4 = crowns
    5 = anchors
Keeps track of number of each symbol using spinTracker
'''
def spinWheel(spinTracker):
    numSymbol=["hearts","spades","diamonds","clubs","crowns","anchors"]
    spin=[numSymbol[randint(0, 5)], numSymbol[randint(0, 5)], numSymbol[randint(0, 5)]]     #generates spin
    #spin=[numSymbol[5],numSymbol[5],numSymbol[5]]                                          ##optional code to test for 3 x anchors dialogue
    for i in range(len(spinTracker)):                                                       #resets spinTracker values to 0
        spinTracker[numSymbol[i]]=0
    for j in range(len(spin)):                                                              #checks matches between spin and spinTracker keys, increments values
        if spin[j] in spinTracker:
            spinTracker[spin[j]]=spinTracker[spin[j]]+1         
    return spin, spinTracker                                                                #returns list and updated dictionary

'''
Reads a positive integer from the user. Prints an error message if
the input is negative or is not an integer. Return value is the
integer entered by the user
'''
def readPlayers():
    print("Welcome to the Crown and Anchor game!")
    while True:
        stringInput=input("How many people are playing?\n")
        try:
            n=int(stringInput)
            if n<2:
                print("There must be at least two players, please try again.\n")
            else:
                return n
        except ValueError:
            print("Invalid input, please try again.\n")

'''
Clears betTracker
'''
def clearBets(betTracker):
    for i in range(len(betTracker)):
        betTracker[i].clear()

'''
Shows bets made in the current round by player
'''
def showBets(player):
    for i in betTracker[player]:
        print(i.capitalize(),": $",betTracker[player][i],sep="")

'''
Begins by asking player what symbol they wish to bet on. Will loop if an invalid input is given.
Includes function "bets" to check bets made in current round.
Will automatically end once a player has run out of money or if player types "end"
Proceeds to ask for bet amount, checking if the bet is an integer and valid
and also if player has already made a bet on the symbol.
Can return to symbol selection by typing "cancel"
Adds bets to betTracker list
'''
def readBets(player,playerFunds,betTracker):
    endBet=False
    while endBet==False:                                    #continues until player decides to end betting
        if playerFunds[player]<1:                           #optional code to automatically end betting when out of money
            print("You have no more money to bet. Betting has ended.\n")
            break
        print("What symbol would you like to bet on (hearts, spades, diamonds, clubs, crowns, anchors)?\nTo show bets, type bets.\nTo end betting, type end.")      #read input to determine symbol
        symbolInput=input()
        symbolInput=symbolInput.lower()
        if symbolInput=="bets":                             #shows bets made by player
            showBets(player)
        elif symbolInput=="end":                            #ends betting for player
            print("Betting has ended.\n")
            endBet=True
        elif symbolInput!="hearts" and symbolInput!="spades" and symbolInput!="diamonds" and symbolInput!="clubs" and symbolInput!="crowns" and symbolInput!="anchors":     #symbol entered is not valid
            print("Invalid symbol, please try again.")
        else:
            validBet=False
            while validBet==False:                          #checks if a valid bet has been made
                print("You have $",playerFunds[player]," remaining.",sep="")
                if symbolInput not in betTracker[player]:   #adds symbol into dictionary if not already present
                    betTracker[player][symbolInput]=0
                if betTracker[player][symbolInput]!=0:      #handles additional bets on a symbol
                    print("You already have a $",betTracker[player][symbolInput]," bet on ",symbolInput,". How much more would you like to bet?\nYou may bet in $1, $2, $5, or $10 increments.",sep="")
                else:
                    print("How much would you like to bet on ",symbolInput,"?\nYou may bet in $1, $2, $5, or $10 increments.",sep="")
                print("To cancel, type cancel")
                betValue=input()
                try:
                    if betValue=="cancel":                  #allows player to return to symbol selection, removes symbol from dictionary if no bets exist
                        if betTracker[player][symbolInput]==0:
                            del betTracker[player][symbolInput]
                        validBet=True
                    else:
                        betValue=int(betValue)
                        if betValue<1 or (betValue!=1 and betValue!=2 and betValue!=5 and betValue!=10):    #prevents negative bets or invalid numbers
                            print("Not a valid bet, please try again.\n")
                        elif playerFunds[player]-betValue<0:                                                #checks that player has enough money
                            print("Not enough funds. You have $",playerFunds[player]," remaining",sep="")
                        else:
                            playerFunds[player]=playerFunds[player]-betValue                                #removes money from player's funds
                            betTracker[player][symbolInput]=betTracker[player][symbolInput]+betValue        #adds bet to tracker
                            print("Player ",player+1," has made a bet of $",betValue," on ",symbolInput,".\nYou have $",playerFunds[player]," remaining.",sep="")
                            validBet=True
                except ValueError:                          #handles invalid inputs
                    print("Not a valid number, please try again.\n")
    return betTracker,playerFunds
        
'''
Handles turns by calling readBets for players still in the game
'''
def makeBets(numPlayers, playerFunds, betTracker):
    for i in range(numPlayers):
        if playerFunds[i]=="Eliminated":
            print("Player",i+1,"is out of money.")
        else:
            print("Player",i+1,"is betting:")
            betTracker=readBets(i,playerFunds,betTracker)
    return betTracker

'''
Checks bets and distributes/announces winnings.
Players with no money at the end are eliminated.
Returns the numbers of players remaining.
'''
def checkBets(playersLeft,spinTracker,playerFunds,betTracker):
    numSymbol=["hearts","spades","diamonds","clubs","crowns","anchors"]
    print("The wheel has been spun!\nThe result is:",spinResult)
    for i in range(numPlayers):
        for j in range(len(numSymbol)):
            if spinTracker[numSymbol[j]]>0 and numSymbol[j] in betTracker[i]:
                if spinTracker[numSymbol[j]]==1:                                #if the symbol appears once, the bet is doubled
                    print("Player ",i+1," has won $",betTracker[i][numSymbol[j]]," on ",numSymbol[j],"!",sep="")
                    playerFunds[i]=playerFunds[i]+2*betTracker[i][numSymbol[j]]
                elif spinTracker[numSymbol[j]]==2:                              #if the symbol appears twice, the bet is tripled
                    print("Player ",i+1," has won $",2*betTracker[i][numSymbol[j]]," on ",numSymbol[j],"!",sep="")
                    playerFunds[i]=playerFunds[i]+3*betTracker[i][numSymbol[j]]
                elif spinTracker[numSymbol[j]]==3:                              #if the symbol appears three times, the bet is quadrupled
                    print("Player ",i+1," has won $",3*betTracker[i][numSymbol[j]]," on ",numSymbol[j],"!",sep="")
                    playerFunds[i]=playerFunds[i]+4*betTracker[i][numSymbol[j]]
                if numSymbol[j]=="anchors" and spinTracker["anchors"]==3:       #special output for winning on triple anchors
                    print("CISC 121 - Winner on Anchors!!!!")
    return playerFunds

'''
Shows each players' funds between turns.
'''
def showFunds(numPlayers,playerFunds):
    print("Money remaining:")
    for i in range(numPlayers):
        if playerFunds[i]=="Eliminated":
            print("Player ",i+1,": ",playerFunds[i],sep="")
        else:
            print("Player ",i+1,": $",playerFunds[i],sep="")
    print("")

'''
Outputs victory and closing messages when the game is over (0 or 1 players remaining).
'''
def endGame(playersLeft,playerFunds):
    if playersLeft==0:
        print("Congratulations! No one won!")
        print("Thank you for playing Crowns and Anchors!")
    elif playersLeft==1:
        for i in range(numPlayers):
            if playerFunds[i]!="Eliminated":
                print("Congratulations! Player ",i+1," is the winner with $",playerFunds[i]," remaining!",sep="")
        print("Thank you for playing Crowns and Anchors!")
    
def main():
    numPlayers=readPlayers()                                                        #number of players at game start
    playersLeft=numPlayers                                                          #number of players remaining
    playerFunds=[]                                                                  #list of integers describing each players' funds
    betTracker=[]                                                                   #list of dictionaries recording bets by each player
    numSymbol=["hearts","spades","diamonds","clubs","crowns","anchors"]             #list used to match symbols to numbers as described above spinWheel 
    spinTracker={"hearts":0,"spades":0,"diamonds":0,"clubs":0,"crowns":0,"anchors":0}       #dictionary used to record the spin

    for i in range(int(numPlayers)):
        playerFunds.append(10)              #assigns $10 to each player
        betTracker.append({})               #adds a blank dictionary to the betTracker list for each player

    while playersLeft>1:
        spinResult=spinWheel(spinTracker)[0]    #spin the wheel
        spinTracker=spinResult[1]
        betTracker=clearBets(betTracker)        #clear bets from the previous round
        betTracker=makeBets(numPlayers, playerFunds, betTracker)                              #make bets
        playerFunds=betTracker[1]
        betTracker=betTracker[0]
        playersFunds=checkBets(playersLeft,spinTracker,playerFunds,betTracker)      #check results
        for i in range(numPlayers):                                                 #checks each players' funds and eliminates those with $0
            if playerFunds[i]==0:
                playersLeft=playersLeft-1
                playerFunds[i]="Eliminated"
                print("Player",i+1,"has been eliminated")
        print("")
        showFunds(numPlayers,playerFunds)                             #show players' funds
        endGame(playersLeft,playerFunds)                               #outputs end game messages when 0 or 1 players left

main()



    






