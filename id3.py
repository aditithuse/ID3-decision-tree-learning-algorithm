from sklearn.metrics import confusion_matrix
import csv
import sys
import math
import copy

def calculateEntropyTerm(probability):
	if probability == 0:
		return 0
	else:
		return float(-probability*math.log(probability,2))

def mostCommonValue(targetIndex,examples):
	t=0
	f=0
	#print(targetIndex)
	for i in range(len(examples)):
		if examples[i][targetIndex] == 1:
			t+=1
		else:
			f+=1
	if t>=f:
		return 1
	elif f>t:
		return 0

class Node:
    def _init_(self):
    	# If it is a node or leaf
        self.element = 'root'
        self.value = 1
        self.attr = -1
        self.trueChild = None
        self.falseChild = None
        self.results = None
        self.index = -1
        self.attrlist = []

def gain(inputData, classIndex, featureIndex):
	totalInput = len(inputData)

	numberOfTrue = 0
	numberOfFalse = 0

	trueSet = []
	falseSet = []

	for loop in range(totalInput):
		if inputData[loop][featureIndex] == 1:
			numberOfTrue +=1
			trueSet.append(inputData[loop])
		if inputData[loop][featureIndex] == 0:
			numberOfFalse += 1
			falseSet.append(inputData[loop])
	
	classEntropy = calculateEntropy(inputData, classIndex)
	trueEntropy = (float(numberOfTrue) / float(totalInput)) * calculateEntropy(trueSet, classIndex)
	falseEntropy = (float(numberOfFalse) / float(totalInput)) * calculateEntropy(falseSet, classIndex)
	informationGain = classEntropy - trueEntropy - falseEntropy

	return informationGain

def calculateEntropy(inputData, classIndex):
	totalInput = len(inputData)
	
	if totalInput == 0:
		return 0

	numberOfTrue = 0
	numberOfFalse = 0
	
	for loop in range(totalInput):
		if inputData[loop][classIndex] == 1:
			numberOfTrue +=1
		elif inputData[loop][classIndex] == 0:
			numberOfFalse += 1
	
	trueEntropy = calculateEntropyTerm(float(numberOfTrue)/float(totalInput))
	falseEntropy = calculateEntropyTerm(float(numberOfFalse)/float(totalInput))

	return (trueEntropy + falseEntropy)

def bestAttr1(inputData, classIndex, features):
	informationGain = []
	for loop in range(len(features)):
		infogain = gain(inputData, classIndex, loop)
		informationGain.append(infogain)

	featureIndex = informationGain.index( max(informationGain) )
	faetureLabel = features[featureIndex]

	return faetureLabel, featureIndex

def id3(inputData, classIndex, features):
	#Create a Root node for the tree
	root = Node()

	allPositive = True
	allNegative = True

	for loop in range(len(inputData)):
		if inputData[loop][classIndex] == 0:
			allPositive=False
		elif inputData[loop][classIndex] == 1:
			allNegative = False
		
	#If all Examples are positive, Return the single-node tree Root, with label = +
	if allPositive:
		root.element ='leaf'
		root.value = 1
		return root
	
	#If all Examples are positive, Return the single-node tree Root, with label = -
	if allNegative:
		root.element ='leaf'
		root.value = 0
		return root

	#If Attributes is empty, Return the single-node tree Root, with label = most common value of Target attribute in Examples
	if not features:
		root.element ='leaf'
		root.value = mostCommonValue(classIndex, inputData)
		return root
	else:
		bestAttr, bestAttrIndex = bestAttr1(inputData, classIndex, features)
		root.attr = 'root'
		root.attr = bestAttr
		root.attrlist = copy.deepcopy(features)
		root.attrlist.remove(bestAttr)

	trueAttrEx = []
	falseAttrEx = []
	
	for i in range(len(inputData)):
		if inputData[i][bestAttrIndex] == 1:
			trueAttrEx.append(inputData[i])

	for i in range(len(inputData)):
		if inputData[i][bestAttrIndex] == 0:
			falseAttrEx.append(inputData[i])

	if not trueAttrEx:
		tempnode = Node()
		tempnode.element = 'leaf'
		tempnode.value = mostCommonValue(classIndex, inputData)
		root.trueChild = None
	else:
		root.element = 'root'
		root.trueChild = id3(trueAttrEx, classIndex, root.attrlist)

	if not falseAttrEx:
		tempnode = Node()
		tempnode.element = 'leaf'
		tempnode.value = mostCommonValue(classIndex, inputData)
		root.falseChild = None
	else:
		root.element = 'root'
		root.falseChild = id3(falseAttrEx, classIndex, root.attrlist)

	return root

def printTree(root, indent):
	if root == None:
		return

	if root.element == 'leaf':
		if root.value == 0:
			print (indent + "Value 0")
		elif root.value == 1:
			print (indent + "Value 1")
		return

	print (indent + root.attr )
	if not root.trueChild == None:
		print (indent + root.attr + " == 1")
		printTree(root.trueChild, indent + " ")
	if not root.falseChild == None:
		print (indent + root.attr + " == 0")
		printTree(root.falseChild, indent + " ")



def fetch(root, dataSet):
	if root == None:
		return -1

	global correct
	correct = 150

	if root.element == 'leaf':
		#print root.attr
		if root.value == 1:
			return 1
		elif root.value == 0:
			return 0
	
	attrIndex = features.index(root.attr)
	if dataSet[attrIndex] == 1:
		return fetch(root.trueChild, dataSet)
	if dataSet[attrIndex] == 0:
		return fetch(root.falseChild, dataSet)


def verify(treeRoot, dataSet):
	plabel = list()
	alabel = list()
	
	for loop in range(len(dataSet)):
		x= fetch(treeRoot, dataSet[loop])
		if x == 0 or x == 1:
			plabel.append(x)
			alabel.append(dataSet[loop][len(dataSet[loop]) - 1])

	for loop in range(len(plabel)):
		#print(plabel[loop]," ",alabel[loop])
		if plabel[loop] == alabel[loop]:
			global correct
			correct +=1
	
	accuracyPercentage = (float) (correct * 100 ) / len(dataSet)
	return plabel,alabel,correct,accuracyPercentage

def calculateMajority(root):
	global ntrue
	global nfalse
	if root.trueChild.trueChild == None or root.trueChild.falseChild == None or root.falseChild.trueChild == None or root.trueChild.falseChild == None:
		#print(nt,nf)
		return ntrue,nfalse

	if not root.trueChild == None:
		ntrue = ntrue+1
		#print("nt",nt)
		calculateMajority(root.trueChild)
	if not root.falseChild == None:
		nfalse = nfalse+1
		#print("nf",nf)
		calculateMajority(root.falseChild)

	return ntrue,nfalse

def majority(root):
	global ntrue
	global nfalse
	#nt,nf = calculateMajority(root)

	if root.trueChild.trueChild == None or root.trueChild.falseChild == None or root.falseChild.trueChild == None or root.trueChild.falseChild == None:
		return

	if not root.trueChild == None:
		
		truenumber,falsenumber = calculateMajority(root.trueChild)
		root.nt = truenumber
		root.nf = falsenumber
		majority(root.trueChild)
		#print(root.trueChild.attr,truenumber,falsenumber)
		ntrue=0

	if not root.falseChild == None:
		
		truenumber,falsenumber = calculateMajority(root.falseChild)
		root.nt = truenumber
		root.nf = falsenumber
		majority(root.falseChild)
		#print(root.falseChild.attr,truenumber,falsenumber)
		nfalse=0
		
def prune(root,accuracyPercentagev,inputData):

	counter = list()
	counterpos = 0
	counterneg = 0
	loop = 0
	temp=tempnode = root


	while root.trueChild != None and root.falseChild != None:
		
		if root.nt >= root.nf:
			counter.append("+1")
			counterpos +=1
			root = root.trueChild

		if root.nt < root.nf:
			counter.append("-1")
			counterneg +=1
			root = root.falseChild


	
	if(counterpos >= counterneg):
		while counter[loop] != '-1':
			print("positive")
			temp = temp.trueChild
			loop +=1
		print(loop)
		temp.trueChild  = None
		temp.value = 1


	elif(counterpos < counterneg):
		while counter[loop] != '+1':
			print("negative")
			temp = temp.falseChild
			loop +=1
		print(loop)
		temp.falseChild  = None
		temp.value = 0

	#print(counter)
	return tempnode


correct = 0
ntrue = 0
nfalse = 0
totalset = []
validationSet = []

trainSetfilename = "./HW3data/data_sets2/training_set.csv"
validationSetfilename = "./HW3data/data_sets2/validation_set.csv"
testingsetfilename = "./HW3data/data_sets2/test_set.csv"

with open(trainSetfilename, 'r') as f:
	reader = csv.reader(f)
	attributes = next(reader)  # skip the headers
	totalset.append(attributes)
	for row in reader:
		results = [int(i) for i in row]
		totalset.append(results)


classIndex = totalset[0].index('Class')
features = totalset[0][0:classIndex]
inputData = totalset[1:len(totalset)]

rootTree = id3(inputData, classIndex, features)

f.close()

printTree(rootTree, "")
#-----------------------------------Validation Data-------------------------
del totalset[:]

with open(validationSetfilename, 'r') as f:
	reader = csv.reader(f)
	attributes = next(reader)  # skip the headers
	totalset.append(attributes)
	for row in reader:
		results = [int(i) for i in row]
		totalset.append(results)

classIndex = totalset[0].index('Class')
features = totalset[0][0:classIndex]
validationData = totalset[1:len(totalset)]

plabel,alabel,correct1,accuracyPercentagev = verify(rootTree, validationData)

print "\n\nMistakes in Validation data:", (len(validationData) - correct1) ,"/",len(validationData)

print "Accuracy percentage in Validation data: ",accuracyPercentagev
cmTest = confusion_matrix(alabel, plabel)
print "Confusion Matrix for ","Validation data","\n",cmTest

f.close()
del plabel[:]
del alabel[:]

#---------------------------Testing Data---------------------------------
del totalset[:]

with open(testingsetfilename, 'r') as f:
	reader = csv.reader(f)
	attributes = next(reader)  # skip the headers
	totalset.append(attributes)
	for row in reader:
		results = [int(i) for i in row]
		totalset.append(results)

classIndex = totalset[0].index('Class')
features = totalset[0][0:classIndex]
testData = totalset[1:len(totalset)]

plabel,alabel,correct2,accuracyPercentage = verify(rootTree, testData)

print "\n\nMistakes in Test data:", (len(testData) - correct2) ,"/",len(testData)

print "Accuracy percentage in Testing Data: ",accuracyPercentage
cmTest = confusion_matrix(alabel, plabel)
print "Confusion Matrix for ","Testing Data","\n",cmTest

del plabel[:]
del alabel[:]

#----------------------Pruning Using Validation Data-----------------------
#print "prune start"

#majority(rootTree)
#root = prune(rootTree,accuracyPercentagev,inputData)

print("\n\nAfter Pruning")
plabel,alabel,correct3,accuracyPercentagev = verify(rootTree, validationData)

print("\n\nMistakes in validation Data",len(validationData) - correct,"/", len(validationData))
print("Accuracy percentage in Validation data: ",accuracyPercentagev)
cm = confusion_matrix(alabel, plabel)
print("Confusion Matrix for ","Validation data","\n",cm)
#prune(rootTree)
#prune(rootTree, validationData)

#print "prune end"


f.close()
