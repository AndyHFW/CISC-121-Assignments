# This program stores student grades for CISC 525
# in the format of a binary search tree.
# The original dataset is read from a webpage.
# The program allows for adding students, finding
# average marks, counting students who failed the final
# and looking up a student's marks.
# BST = Binary Search Tree

# Assignment 4 for CISC 121, Summer 2017
# Author: Andy Wang

import urllib.request

'''
Reads instructions from a web page using the
urlopen function in the urllib.request module.
Places each line of instructions in list cmdList.
Continues reading until an empty bytes variable is read.
Splits each line into a list, then uses the add() function
to add each list into the BST based on student number
Returns BST
'''
def readHtml(tree):
    html=b'temp'
    cmdList=[]
    response = urllib.request.urlopen("http://www.cs.queensu.ca/home/cords2/marks.txt")
    while html!=b'':
        html = response.readline()
        data = html.decode('utf-8').split()
        cmdList.append(data)
    cmdList.remove([])                      #removes the "decoded" empty bytes variable
    for i in range(len(cmdList)):
        tempList=cmdList[i][0].split(",")
        for j in range(len(tempList)):
            if float(tempList[j])%1>0:
                tempList[j]=float(tempList[j])
            else:
                tempList[j]=int(tempList[j])
        tree=add(tree,tempList)
    return tree


'''
Prints an indented display of the tree -- useful for debugging.
The output will look kind of like a sideways version of a drawing
of the tree.
Function taken from the sample BST code for CISC 121.
'''
def display(tree, indent=0):
    if tree == None: # empty
        pass
    else:
        # right tree first (so it's on the right when you tilt your
        # head to the left to look at the display)
        display(tree['right'],indent+1)
        print("    " * indent + str(tree['data'][0]))
        # now the left tree
        display(tree['left'],indent+1)

'''
Prints contents of the BST -- useful for debugging.
Function taken from the sample BST code for CISC 121
'''
def printValues(tree):
    if tree == None:
        return
    printValues(tree['left'])
    print(tree['data'])
    printValues(tree['right'])

'''
Adds a value to a BST and returns a pointer to the modified BST
Modified function from the sample BST code for CISC 121.
'''
def add(tree, value):
    if tree == None:
        return {'data':value, 'left':None, 'right':None}
    elif value[0] < tree['data'][0]:
        tree['left'] = add(tree['left'],value)
        return tree
    elif value[0] > tree['data'][0]:
        tree['right'] = add(tree['right'],value)
        return tree
    else: # value == tree['data']
        return tree # ignore duplicate

'''
Centralizes error printing.
Prints an error message based on the error code (numError)
'''
def errorReport(numError):
    if numError==0:
        print("Invalid input, please try again. \n")
    elif numError==1:
        print("Invalid input (input cannot contain letters). \n")
    elif numError==2:
        print("Invalid input (student number must be 4 digits). \n")
    elif numError==3:
        print("Invalid input (choose evaluation between 1-7). \n")
    elif numError==25 or numError==15 or numError==20 or numError==35 or numError==65:
        print("Invalid input (grade must be between 0 and ",numError,"). \n",sep="")

'''
Checks for a valid int or string input.
Returns True if input is valid, False if not.
Also prints an error message if input is invalid.
'''
def checkInput(stringInput):
    try:
        float(stringInput)
        return True
    except ValueError:
        errorReport(1)
        return False

'''
Adds to a new student's mark profile.
Parameter evalNum is used to validate input.
The inputted grade is added to the list newStudent.
newStudent is returned as the student's updated profile.
'''
def addMark(evalNum,newStudent):
    validInput=False
    markWeight={1:25, 2:25, 3:15, 4:20, 5:20, 6:35, 7:65}
    while validInput==False:
        print("Please input a mark for assignment ",evalNum," (/",markWeight[evalNum],"): ",sep="",end="")
        tempInput=input()
        if checkInput(tempInput)==True:
            if float(tempInput)>markWeight[evalNum] or float(tempInput)<0:
                errorReport(markWeight[evalNum])
            else:
                if float(tempInput)%1>0:
                    newStudent.append(float(tempInput))
                else:
                    newStudent.append(int(tempInput))
                validInput=True
                return newStudent

'''
Adds a new student to the BST.
The list newStudent is used to temporarily store
the student's profile.
Inputs are read for the student # and marks for the
seven evaluations.
Returns BST with the new student added.
'''
def addStudent(myTree):
    newStudent=[]
    tempInput=""
    validInput=False
    print("Adding a new student:")
    while validInput==False:        #adding student number
        tempInput=input("Please input student number (4 digits): ")
        if checkInput(tempInput)==True:
            if len(tempInput)!=4:
                errorReport(2)
            else:
                newStudent.append(int(tempInput))
                validInput=True
                
    newStudent=addMark(1,newStudent)
    newStudent=addMark(2,newStudent)
    newStudent=addMark(3,newStudent)
    newStudent=addMark(4,newStudent)
    newStudent=addMark(5,newStudent)
    newStudent=addMark(6,newStudent)
    newStudent=addMark(7,newStudent)    
    #print(newStudent)
    return add(myTree,newStudent)

'''
Sums the marks for a given evaluation.
Parameters are the BST and evalNum (evaluation in question).
Returns the sum of the marks.
Eventually used to calculate the average mark.
'''
def findSum(myTree,evalNum):
    if myTree==None:
        return 0
    return myTree["data"][evalNum]+findSum(myTree["left"],evalNum)+findSum(myTree["right"],evalNum)

'''
Counts the number of students in the BST.
Parameter is the BST.
Returns the number of students.
Eventually used to calculate the average mark.
'''
def countStudents(myTree):
    if myTree==None:
        return 0
    return 1+countStudents(myTree["left"])+countStudents(myTree["right"])

'''
Counts the number of students who scored
<50% on the final exam.
Returns the number of students with <50%.
'''
def countExam(myTree):
    if myTree==None:
        return 0
    if myTree["data"][7]<(65/2):
        return 1+countExam(myTree["left"])+countExam(myTree["right"])
    else:
        return countExam(myTree["left"])+countExam(myTree["right"])

'''
Finds the marks for a specific student.
Parameters are the BST and the student #.
Returns student data or None if the student does not exist.
'''
def findMarks(myTree,studentNo):
    if myTree==None:
        return None
    elif myTree["data"][0]==studentNo:
        return myTree["data"]
    elif myTree["data"][0]>studentNo:
        return findMarks(myTree["left"],studentNo)
    else:
        return findMarks(myTree["right"],studentNo)

'''
Top level function.
Prints instructions and determines commands.
Has error-handling functionality for invalid inputs.
'''
def main():
    myTree = None  #create an empty tree
    myTree=readHtml(myTree)
    stringInput=""
    evalInput=""
    studentInput=""
    evalDict={1:"Assignment 1",2:"Assignment 2",3:"Assignment 3",4:"Assignment 4",5:"Assignment 5",6:"Midterm",7:"Final Exam"}
    
    print("This program is written to organize student marks for CISC 525. \n")
    while stringInput.lower()!="exit":
        stringInput=""
        stringInput=input("Please select a command "
              "(type exit to end the program): \n"
              "(1) Add a new student \n"
              "(2) Find average marks for an evaluation \n"
              "(3) Count students who failed the final exam (<50%) \n"
              "(4) Look up the marks for a specific student \n")
        if stringInput=="1":            #command 1: add new student to the database/BST
            myTree=addStudent(myTree)
        elif stringInput=="2":          #command 2: find average marks for an evaluation
            evalInput=""
            while evalInput!=-1:
                print("Please select an evaluation ",
                  "(type back to return to command selection): \n",
                  "(1)",evalDict[1], "\n",
                  "(2)",evalDict[2], "\n",
                  "(3)",evalDict[3], "\n",
                  "(4)",evalDict[4], "\n",
                  "(5)",evalDict[5], "\n",
                  "(6)",evalDict[6], "\n",
                  "(7)",evalDict[7], "\n",end="")
                evalInput=input()
                try:
                    if int(evalInput)>0 and int(evalInput)<8:
                        print("The course average for",evalDict[int(evalInput)],"was", round(findSum(myTree,int(evalInput))/countStudents(myTree),1),"\n")
                        evalInput=-1
                    else:
                        errorReport(3)
                except ValueError:
                    if evalInput=="back":
                        evalInput=-1
                    else:
                        errorReport(1)
        elif stringInput=="3":          #command 3: counts students with <50% on the final
            print("There were",countExam(myTree),"students who scored below 50% on the final exam.\n")
        elif stringInput=="4":          #command 4: searches for a student's grades
            studentInput=""
            while studentInput!=-1:
                studentInput=input("Grade search - please enter a student number (4 digits)\n"
                                   "(type back to return to command selection): \n")
                try:
                    if int(studentInput)>999 and int(studentInput)<10000:
                        markList=findMarks(myTree,int(studentInput))
                        if markList==None:
                            print("Student does not exist. Please try again")
                        else:
                            print("Marks for student #",markList[0],": \n",
                                  evalDict[1],": ", markList[1],"/25 (",round(markList[1]/25*100,1),"%)","\n",
                                  evalDict[2],": ", markList[2],"/25 (",round(markList[2]/25*100,1),"%)","\n",
                                  evalDict[3],": ", markList[3],"/15 (",round(markList[3]/15*100,1),"%)","\n",
                                  evalDict[4],": ", markList[4],"/20 (",round(markList[4]/20*100,1),"%)","\n",
                                  evalDict[5],": ", markList[5],"/20 (",round(markList[5]/20*100,1),"%)","\n",
                                  evalDict[6],": ", markList[6],"/35 (",round(markList[6]/35*100,1),"%)","\n",
                                  evalDict[7],": ", markList[7],"/65 (",round(markList[7]/65*100,1),"%)","\n",sep="")
                            studentInput=-1
                    else:
                        errorReport(2)
                except ValueError:
                    if studentInput=="back":
                        studentInput=-1
                    else:
                        errorReport(1)
        elif stringInput.lower()!="exit":
            errorReport(0)
    #display(myTree, 0)
    #printValues(myTree)
    
    
main()
