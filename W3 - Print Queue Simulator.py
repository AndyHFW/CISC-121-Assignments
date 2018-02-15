# This program is a print queue simulator.
# The program reads instructions off of a web page
# pertaining to addition, removal, and printing of documents
# as well as showing contents of the print queue

# Assignment 2 for CISC 121, Summer 2017
# Author: Andy Wang

import urllib.request

'''
Reads instructions from a web page using the
urlopen function in the urllib.request module.
Places each line of instructions in list cmdList.
Continues reading until an empty bytes variable is read.
Returns cmdList
'''
def readHtml():
    html=b'temp'
    cmdList=[]
    response = urllib.request.urlopen("http://research.cs.queensu.ca/home/cords2/printsim.txt")
    while html!=b'':
        html = response.readline()
        data = html.decode('utf-8').split()
        cmdList.append(data)
    cmdList.remove([])                      #removes the "decoded" empty bytes variable
    return cmdList

'''
Calculates time reequired to process a document
based on format, colour/bw, and pages.
Parameter docInfo is the info for the relevant document.
Returns -1 if file format is invalid (not pdf, docx, pptx, or jpg)
Otherwise, returns estimated time
'''
def calcTime(docInfo):
    time=0
    if docInfo["type"]=="pdf":
        if docInfo["colour"]=="bw":
            time=time+4*int(docInfo["pages"])
        else:
            time=time+30*int(docInfo["pages"])
    elif docInfo["type"]=="pptx" or docInfo["type"]=="docx":
        if docInfo["colour"]=="bw":
            time=time+6*int(docInfo["pages"])
        else:
            time=time+20*int(docInfo["pages"])
    elif docInfo["type"]=="jpg":
        if docInfo["colour"]=="bw":
            time=time+10*int(docInfo["pages"])
        else:
            time=time+60*int(docInfo["pages"])
    else:
        return -1                           #returns -1 for an invalid file format
    return time    

'''
Used to determine where to place a new document in queue.
Parameters include the current queue and estimated time
for the new document.
Returns "head" if the document should be placed at the front.
Otherwise, returns n, being the position in queue
'''
def findPlace(currentQ,newTime):
    n=0
    ptr=currentQ
    while ptr["data"]["time"]<=newTime and ptr["next"]!=None:
        ptr=ptr["next"]
        n=n+1
    if n==0 and ptr["data"]["time"]>newTime:
        return "head"
    elif ptr["data"]["time"]>newTime:       #in case the current ptr location contains a slower document
        n=n-1
    return n

'''
Function used to add a new document to queue.
Parameters include info about the new document and the current queue.
Ignores document if file format is invalid.
Adds document based on position found using findPlace().
Special cases exist for the first document or a cleared/empty queue.
Returns updated currentQ.
'''
def submit(docInfo,currentQ):
    docData={"data":{"id":docInfo[1],"type":docInfo[2],"pages":docInfo[3],"colour":docInfo[4]}}
    docTime=calcTime(docData["data"])
    docData["data"]["time"]=docTime
    if docTime==-1:                         #ignore document if file format is invalid
        pass                                
    else:
        print("Adding job",docData["data"]["id"],"to the queue. It will require",docTime,"seconds to process.")
        ptr=currentQ
        if currentQ==None:                  #special case for cleared queue
            currentQ={}
            currentQ["data"]=docData["data"]
            currentQ["next"]=None
        elif "data" not in currentQ:        #special case for first document
            docData["next"]=None
            currentQ=docData
        else:
            position=findPlace(currentQ,docTime)
            if position=="head":
                docData["next"]=ptr
                currentQ=docData
            else:
                counter=0
                while counter<position:     #counts to n based on findPlace()
                    ptr=ptr["next"]
                    counter=counter+1
                docData["next"]=ptr["next"]
                ptr["next"]=docData
    return currentQ

'''
Shows the current print queue.
Parameter is the current queue
Prints the number of items in the queue and estimated total time.
Optional lines to show all document data or job IDs
'''
def queue(currentQ):             #prints a linked list
    if currentQ==None:
        print("The queue is empty")
    else:
        ptr=currentQ
        printTime=0
        inQueue=0
        while ptr["next"]!=None:
            print(ptr["data"])              #optional line - shows all info for queue items
            #print(ptr["data"]["id"])       #optional line - shows specific queue items
            inQueue=inQueue+1
            printTime=printTime+int(ptr["data"]["time"])
            ptr=ptr["next"]
        print(ptr["data"])                  #optional line - shows all info for queue
        #print(ptr["data"]["id"])           #optional line - shows specific queue item
        printTime=printTime+int(ptr["data"]["time"])
        inQueue=inQueue+1
        print("There are",inQueue,"items in queue. Estimated total print time is",printTime,"seconds.")

'''
Function used to "print" first document in queue.
Parameter is the current queue.
Prints and removes the first document.
Returns updated queue.
'''
def printDoc(currentQ):
    if currentQ==None:
        print("There are no documents in queue")
    else:
        print("Printing job",currentQ["data"]["id"])
        currentQ=currentQ["next"]
    return currentQ

'''
Function used to removea specific document from the queue.
Parameters include ID for document to be removed and current queue.
Specific case when document to be removed is at the head.
Returns updated queue.
'''
def removeDoc(cmdInfo,currentQ):
    ptr=currentQ
    prevLoc={}
    print("Removing job",cmdInfo[1])
    if cmdInfo[1]==ptr["data"]["id"] and prevLoc=={}:
        currentQ=currentQ["next"]
    elif cmdInfo[1]!=ptr["data"]["id"] and prevLoc=={}:
        prevLoc=currentQ
        ptr=ptr["next"]
        while ptr["next"]!=None:
            if cmdInfo[1]==ptr["data"]["id"]:
                prevLoc["next"]=ptr["next"]
                break
            ptr=ptr["next"]
            prevLoc=prevLoc["next"]
    return currentQ

'''
Top level function.
Determines command and calls appropriate function.
Optional line allows pausing between each command
'''
def main():
    cmdList=readHtml()
    currentQ={"next":None}
    for i in range(len(cmdList)):
        command=cmdList[i][0]
        if command=="submit":
            currentQ=submit(cmdList[i],currentQ)
        elif command=="queue":
            queue(currentQ)
        elif command=="print":
            currentQ=printDoc(currentQ)
        elif command=="remove":
            currentQ=removeDoc(cmdList[i],currentQ)
        #input("Press enter to continue to the next command")
        print("")
    
main()
