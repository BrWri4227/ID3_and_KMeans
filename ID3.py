from math import log
import csv
import random
import sys
from Node import Node
file = open('iris.data', 'r') #open iris dataset

csvReader = csv.reader(file) #read using csv reader

unParsedData = list(csvReader) #convert to list
# random.seed(400)
random.shuffle(unParsedData) #shuffle the list

dataSet = []
for i in range(len(unParsedData)): #convert the unparsed data to a list of my own vector class
    dataSet.append([unParsedData[i][0], unParsedData[i][1], unParsedData[i][2], unParsedData[i][3], unParsedData[i][4]])

trainingSet = []
for i in range(0, 120): #Split the data into train and test sets, since the list is now shuffled i can just pick from 0,120 
    trainingSet.append([unParsedData[i][0], unParsedData[i][1], unParsedData[i][2], unParsedData[i][3], unParsedData[i][4]])
    # print(trainingSet[i])

testingSet = []
for i in range(120, 150):
    testingSet.append([unParsedData[i][0], unParsedData[i][1], unParsedData[i][2], unParsedData[i][3], unParsedData[i][4]])

#[sepal length, sepal width, petal length, petal width, class]
def calcEntropy(data):
    classes = {}
    for row in data:
        if row[-1] not in classes: #If the species [row[-1]] is not in the dictionary
            classes[row[-1]] = 0 #Add it to the dictionary
        classes[row[-1]] += 1 #Add one to the count of the species
    entropy = 0.0
    # print(classes)
    for count in classes.values(): #For each each of the species
        p = count / len(data) #Get the probability / 120
        entropy += (-p) * log(p, 2) #calculate entropy
    return entropy

def infoGain(data, index): #info gain for a given attribute
    baseEntropy = calcEntropy(data) #entropy of whole data
    attributeNums = {} #get all of the vaules of that attribute for all of the data
    if index == 4: #If the index is the species/class,
        print("Error: index is class, something has gone horribly wrong") #SOEMTHING WENT WRONG
        sys.exit(1)
    for row in data: #Then for each full row of data
        attributeNums[row[index]] = 0 #add ONLY the selected attribute it to the dict
    for row in data:
        attributeNums[row[index]] += 1 #Count how many pieces of data share that value
    # print(attributeNums,"!")
    newEntropy = 0.0 #init for new entropy

    for value in attributeNums: #for each unique value of the attribute
        subData = [] #split 
        for row in data: #
            if row[index] == value: #any of the pieces of data share a value
                subData.append(row) #split on it
        p = len(subData) / len(data) #calculate how many data poitns share compared to total
        newEntropy += p * calcEntropy(subData) #calculate the nwe
    
    return baseEntropy - newEntropy #calculate how much information is gained off splitting on attribute 'index' where 0 is sepal length, 1 is sepal width, 2 is petal length, 3 is petal width

def bestInfoGain(data, attributes): #function for calculating the best attribute to split on
    bestAttribute = None
    highestInfoGain = 0
    for i in attributes: #For each attribute in the list (because we could have split on any of them not just in order)
        infoGainValue = infoGain(data, i)  #we get the info gain
        # print(infoGainValue, " ", highestInfoGain)
        if(infoGainValue > highestInfoGain): #check if its the highest
            highestInfoGain = infoGainValue #if it is, set it as the highest
            bestAttribute = i
    return bestAttribute #return the index of the best attribute

def majorityClass(data): #function for getting the majority class 
    classes = {} #init
    for row in data: #for each piece of data
        if row[-1] not in classes: #if its not in the dict
            classes[row[-1]] = 0 #add it
        classes[row[-1]] += 1 #count it
    
    classes = sorted(classes.items(), key=lambda x: x[1], reverse=True) #sort it
    return classes[0][0] #whatever is in the first spot should be the highest and majority

def createTree(data, attributes):
    pureLabels = {} #Checking if the data is pure
    for row in data: #Populate the dict
        if row[-1] not in pureLabels: #if not in 
            pureLabels[row[-1]] = 0 #add it
        pureLabels[row[-1]] += 1 #count it
    if(len(pureLabels) == 1): #If thers only one species
        return Node(label=list(pureLabels.keys())[0]) #Its a leaf, return it
    if len(attributes) == 0: #If there is nothing left to split on
        pureLabels = sorted(pureLabels.items(), key=lambda x: x[1], reverse=True) #get the majority class, sort
        label = pureLabels[0][0] #get the first one
        return Node(label=label) #LEAF! return it
    
    bestAttributeIndex = -1 #init for best attribute
    bestAttributeIndex = bestInfoGain(data, attributes) # get the best attribute to split on
    root = Node(attribute=bestAttributeIndex) #First iteration, root is the best best attribute out of all of them
    attributes.remove(bestAttributeIndex) #no more splitting on that one
    attributeValues = {} # init for the values of the attribute
    for row in data: #populate the dict of the values of the BEST attribute
        attributeValues[row[bestAttributeIndex]] = 0 #if not it in
    for row in data:
        attributeValues[row[bestAttributeIndex]] += 1 #add it
    
    for value in attributeValues: #for each value of the best attribute
        subData = [] #split on it
        for row in data: #for each piece of data
            if row[bestAttributeIndex] == value: #if it its value for that attribute matches the value we are splitting on
                subData.append(row) #split it
        if len(subData) == 0: #if nothing to split!
            root.children[value] = Node(label=majorityClass(data)) #is a leaf!
        else:
            root.children[value] = createTree(subData, attributes[:]) #otherwise, recursively create the tree on the leftover data and leftover attribute(s)
    return root #return the root!

 
def classify(root, attributes, point):

    if root.label is not None: #if its a leaf (IT SHOULDN'T HAVE A LABEL UNLESS ITS A LEAF)
        return root.label #return the label
    else: #it must have at least one child
        value = point[root.attribute] #pull the value of the attribute we are splitting on
        if value not in root.children: #if there is no subtree for that value
            classList = [child.label for child in root.children.values() if child.label is not None] # Grab all the labels from this nodes children
            
            return majorityClass(classList) # and return the majority class
        else:
            return classify(root.children[value], attributes, point) #otherwise, search the subtrees for that value (until it hits a leaf)
        
attributes = [0, 1, 2, 3] #init list for the attributes, 0 is sepal length, 1 is sepal width, 2 is petal length, 3 is petal width
# print(calcEntropy(trainingSet))
# print(infoGain(trainingSet, 0))
tree = createTree(trainingSet, attributes) #create the tree passing the list of possible splitting attributes
testAttributeSet = [0, 1, 2, 3] #since 'attributes' is actually modified by createTree we have to redeclare it
accuracy = 0
totalPoints = len(testingSet)
totalCorrect = 0
virginicaCorrect = 0
setosaCorrect = 0
versicolorCorrect = 0
totalVirginica = 0
totalSetosa = 0
totalVersicolor = 0

for i in range(len(testingSet)):
    if(testingSet[i][4] == "Iris-setosa"):
        totalSetosa += 1
    elif(testingSet[i][4] == "Iris-versicolor"):
        totalVersicolor += 1
    elif(testingSet[i][4] == "Iris-virginica"):
        totalVirginica += 1
    if(classify(tree, testAttributeSet, testingSet[i]) == testingSet[i][4]):
        totalCorrect += 1
        if(testingSet[i][4] == "Iris-setosa"):
            setosaCorrect += 1
        elif(testingSet[i][4] == "Iris-versicolor"):
            versicolorCorrect += 1
        elif(testingSet[i][4] == "Iris-virginica"):
            virginicaCorrect += 1
setosaAcc = round(setosaCorrect / totalSetosa * 100, 2)
virginicaAcc = round(virginicaCorrect / totalVirginica * 100, 2)
versicolorAcc = round(versicolorCorrect / totalVersicolor * 100, 2)
print("Setosa Accuracy: ", setosaAcc,"%")
print("Virginica Accuracy: ", virginicaAcc,"%")
print("Versicolor Accuracy: ", versicolorAcc,"%")
# print(totalCorrect, " out of ", totalPoints, " correct")
# accuracy = round(totalCorrect / totalPoints * 100, 2)
# print("Overall Accuracy: ", accuracy,"%")
        