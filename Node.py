class Node:
    def __init__(self, attribute=None, value=None, label=None):
        self.attribute = attribute #Attribute that got split on as an index
        self.value = value #value that it was split on > or <=
        self.label = label #species if leaf
        self.children = {}#
    
    def __str__(self) -> str:
        if self.attribute == None:
            return "Leaf: " + self.label
        elif self.attribute != None:
            return "Splitting Attribute: " + str(self.attribute) + " on value: " + str(self.value) + " with label: " + str(self.label)