class Vector():
    def __init__(self, sepalLength, sepalWidth, petalLength, petalWidth, species):
        self.sepalLength = float(sepalLength)
        self.sepalWidth = float(sepalWidth)
        self.petalLength = float(petalLength)
        self.petalWidth = float(petalWidth)
        self.species = species
        self.centroid = -1
    def __str__(self) -> str:
        return f"Sepal Length: {self.sepalLength}, Sepal Width: {self.sepalWidth}, Petal Length: {self.petalLength}, Petal Width: {self.petalWidth}, Species: {self.species}"
    
    def getClass(self):
        return self.species
    