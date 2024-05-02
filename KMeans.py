import csv
import random
from Vector import Vector
import copy
import math

file = open('iris.data', 'r') #open iris dataset

csvReader = csv.reader(file) #read using csv reader

unParsedData = list(csvReader) #convert to list
# random.seed(500)
random.shuffle(unParsedData) #shuffle the list

dataSet = []
for i in range(len(unParsedData)): #convert the unparsed data to a list of my own vector class
    dataSet.append(Vector(unParsedData[i][0], unParsedData[i][1], unParsedData[i][2], unParsedData[i][3], unParsedData[i][4]))

trainingSet = []
for i in range(0, 120): #Split the data into train and test sets, since the list is now shuffled i can just pick from 0,120 
    trainingSet.append(Vector(unParsedData[i][0], unParsedData[i][1], unParsedData[i][2], unParsedData[i][3], unParsedData[i][4]))
    # print(trainingSet[i])

testingSet = []
for i in range(120, 150):
    testingSet.append(Vector(unParsedData[i][0], unParsedData[i][1], unParsedData[i][2], unParsedData[i][3], unParsedData[i][4]))



# FINDING THE MIN AND MAX FOR EACH FEATURE
minSepalLength = 9999999
maxSepalLength = -1
minSepalWidth = 9999999
maxSepalWidth = -1
minPetalLength = 9999999
maxPetalLength = -1
minPetalWidth = 9999999
maxPetalWidth = -1
for i in range(len(dataSet)):
    if dataSet[i].sepalLength < minSepalLength:
        minSepalLength = dataSet[i].sepalLength
    if dataSet[i].sepalLength > maxSepalLength:
        maxSepalLength = dataSet[i].sepalLength
    if dataSet[i].sepalWidth < minSepalWidth:
        minSepalWidth = dataSet[i].sepalWidth
    if dataSet[i].sepalWidth > maxSepalWidth:
        maxSepalWidth = dataSet[i].sepalWidth
    if dataSet[i].petalLength < minPetalLength:
        minPetalLength = dataSet[i].petalLength
    if dataSet[i].petalLength > maxPetalLength:
        maxPetalLength = dataSet[i].petalLength
    if dataSet[i].petalWidth < minPetalWidth:
        minPetalWidth = dataSet[i].petalWidth
    if dataSet[i].petalWidth > maxPetalWidth:
        maxPetalWidth = dataSet[i].petalWidth
        
#Now with this i can make better random centroids 

def kMeans(dataSet, n, k):
    bestCentroids = [] #init best centroid
    bestDistortion = 9999999 #init for distortion
    for z in range(n): #run n times
        centroids = [] #init random centroids
        for i in range(k): #Create 3 random centroids from the min to max of each feature uniformly distributed across the range
            centroids.append(Vector(random.uniform(minSepalLength, maxSepalLength), random.uniform(minSepalWidth, maxSepalWidth), random.uniform(minPetalLength, maxPetalLength), random.uniform(minPetalWidth, maxPetalWidth), ""))
        converged = False #Its not converged yet
        while converged == False: #while its not converged(stop moving)
            oldCentroids = centroids.copy() #Save the centroids
            distortion = 0
            for j in range(len(dataSet)): #For each point
                minDistance = 9999999 #distance init
                for l in range(3): #For each centroid
                    #Calc distance to centroid
                    distance = math.sqrt((dataSet[j].sepalLength - centroids[l].sepalLength)**2 + (dataSet[j].sepalWidth - centroids[l].sepalWidth)**2 + (dataSet[j].petalLength - centroids[l].petalLength)**2 + (dataSet[j].petalWidth - centroids[l].petalWidth)**2)
                    #if the distance is lower than the previous centroid
                    if distance < minDistance:
                        minDistance = distance #its the new one
                        dataSet[j].centroid = l #add it to the cluster
            for m in range(len(centroids)): #For each centroid
                totalSepalLength = 0 #Calc total for each feature
                totalSepalWidth = 0
                totalPetalLength = 0
                totalPetalWidth = 0
                count = 0 #and how many are in each cluster
                for p in range(len(dataSet)):
                    if dataSet[p].centroid == m: #If the point is in the cluster
                        totalSepalLength += dataSet[p].sepalLength  #total its features
                        totalSepalWidth += dataSet[p].sepalWidth 
                        totalPetalLength += dataSet[p].petalLength
                        totalPetalWidth += dataSet[p].petalWidth
                        count += 1
                if count > 0: #if its non empty
                    centroids[m].sepalLength = totalSepalLength / count #Calc the new centroid
                    centroids[m].sepalWidth = totalSepalWidth / count
                    centroids[m].petalLength = totalPetalLength / count
                    centroids[m].petalWidth = totalPetalWidth / count
            if oldCentroids == centroids: #If the centroids didnt move
                converged = True #converged
            
        for j in range(len(dataSet)): #Calculate the distortion
            distortion += (dataSet[j].sepalLength - centroids[dataSet[j].centroid].sepalLength)**2 + (dataSet[j].sepalWidth - centroids[dataSet[j].centroid].sepalWidth)**2 + (dataSet[j].petalLength - centroids[dataSet[j].centroid].petalLength)**2 + (dataSet[j].petalWidth - centroids[dataSet[j].centroid].petalWidth)**2
        # distortion = round(distortion, 2)
        #if the distortion is lower than the previous best
        if(distortion < bestDistortion):
            bestDistortion = distortion#its the new one
            bestCentroids = copy.deepcopy(centroids) #save the centroids
            # print("New Best Distortion: ", round(bestDistortion,2)) #print the new best distortion

    #Then, after the best centroids are found, recolor the points
    for i in range(len(dataSet)):
        minDistance = 9999999 #distance init
        for j in range(3):
            distance = math.sqrt((dataSet[i].sepalLength - bestCentroids[j].sepalLength)**2 + (dataSet[i].sepalWidth - bestCentroids[j].sepalWidth)**2 + (dataSet[i].petalLength - bestCentroids[j].petalLength)**2 + (dataSet[i].petalWidth - bestCentroids[j].petalWidth)**2)
            if distance < minDistance:
                minDistance = distance
                dataSet[i].centroid = j #recoloring
    
    #Then, now classify the centroids based off their dominant species        
    arr = []
    for i in range(3):
        setosaCount = 0 #counts for each
        versicolorCount = 0
        virginicaCount = 0
        for j in range(len(dataSet)):
            if dataSet[j].centroid == i: #if the point is in the cluster
                if dataSet[j].species == "Iris-setosa": #and its species matches
                    setosaCount += 1 #add to the count
                elif dataSet[j].species == "Iris-versicolor":
                    versicolorCount += 1
                elif dataSet[j].species == "Iris-virginica":
                    virginicaCount += 1
        # print("Cluster ", i, " has ", setosaCount, " Iris-setosa, ", versicolorCount, " Iris-versicolor, and ", virginicaCount, " Iris-virginica")
        arr.append((setosaCount, versicolorCount, virginicaCount)) #add the counts to the array
    for i in range(3): #for each centroid
        if arr[i][0] >= arr[i][1] and arr[i][0] >= arr[i][2]: #if the setosa count is the highest
            bestCentroids[i].species = "Iris-setosa" #classify it as setosa
        elif arr[i][1] >= arr[i][0] and arr[i][1] >= arr[i][2]: #if the versicolor count is the highest
            bestCentroids[i].species = "Iris-versicolor" #classify it as versicolor
        else: #if the virginica count is the highest
            bestCentroids[i].species = "Iris-virginica" #classify it as virginica
    
    # print("Best Centroids: ", bestCentroids[0] ,"\n", bestCentroids[1],"\n", bestCentroids[2]) #print the centroids
    return bestCentroids

def predict(testingSet, bestCentroids): #Predict the species of the testing set
    accuracy = 0
    totalPoints = len(testingSet)
    totalCorrect = 0
    virginicaCorrect = 0
    setosaCorrect = 0
    versicolorCorrect = 0
    totalVirginica = 0
    totalSetosa = 0
    totalVersicolor = 0
    for i in range(len(testingSet)): #count the total number of each species
        minDistance = 9999999
        if(testingSet[i].species == "Iris-virginica"):
                totalVirginica += 1
        elif(testingSet[i].species == "Iris-setosa"):
                totalSetosa += 1
        else:
                totalVersicolor += 1
        for j in range(len(bestCentroids)): #find the closest centroid
            
            distance = math.sqrt((testingSet[i].sepalLength - bestCentroids[j].sepalLength)**2 + (testingSet[i].sepalWidth - bestCentroids[j].sepalWidth)**2 + (testingSet[i].petalLength - bestCentroids[j].petalLength)**2 + (testingSet[i].petalWidth - bestCentroids[j].petalWidth)**2)
            if distance < minDistance:
                minDistance = distance
                testingSet[i].centroid = j #and assign it
                
    for i in range(len(testingSet)): #then for each test point
        if(testingSet[i].centroid == 0): #if its in the first cluster
            if(testingSet[i].species == bestCentroids[0].species): #and its species matches the centroid
                totalCorrect += 1 #add to the total correct
                if testingSet[i].species == "Iris-virginica": #and if its virginica
                    virginicaCorrect += 1
                elif testingSet[i].species == "Iris-setosa": #SO ON
                    setosaCorrect += 1
                elif testingSet[i].species == "Iris-versicolor":
                    versicolorCorrect += 1
            
        elif(testingSet[i].centroid == 1): #SAME AS ABOVE
            if(testingSet[i].species == bestCentroids[1].species):
                totalCorrect += 1
                if testingSet[i].species == "Iris-virginica":
                    virginicaCorrect += 1
                elif testingSet[i].species == "Iris-setosa":
                    setosaCorrect += 1
                elif testingSet[i].species == "Iris-versicolor":
                    versicolorCorrect += 1                    
                
        elif(testingSet[i].centroid == 2): #SAME AS ABOVE
            if(testingSet[i].species == bestCentroids[2].species):
                totalCorrect += 1
                if testingSet[i].species == "Iris-virginica":
                    virginicaCorrect += 1
                elif testingSet[i].species == "Iris-setosa":
                    setosaCorrect += 1
                elif testingSet[i].species == "Iris-versicolor":
                    versicolorCorrect += 1

    setosaAcc = round(setosaCorrect / totalSetosa * 100, 2)
    virginicaAcc = round(virginicaCorrect / totalVirginica * 100, 2)
    versicolorAcc = round(versicolorCorrect / totalVersicolor * 100, 2)
    print("Setosa Accuracy: ", setosaAcc,"%")
    print("Virginica Accuracy: ", virginicaAcc,"%")
    print("Versicolor Accuracy: ", versicolorAcc,"%")
    # accuracy = round(totalCorrect / totalPoints * 100, 2)
    # print("Overall Accuracy: ", accuracy,"%")
    # return accuracy
# bestCentroids = kMeans(trainingSet, 100)
# predict(testingSet, bestCentroids)
def main():
    while True:
        try:
            k = int(input("Enter the value of K: "))
            if k < 3:
                print("K must be at least 3")
            else:
                break
        except:
            print("Invalid input")
    while True:
        try:
            n = int(input("Enter the number of iterations: "))
            if n < 1:
                print("Number of iterations must be at least 1")
            else:
                break
        except:
            print("Invalid input")
    bestCentroids = kMeans(trainingSet, n, k)
    predict(testingSet, bestCentroids)
    
if __name__ == "__main__":
    main()
