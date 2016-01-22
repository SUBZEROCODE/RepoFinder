from sys import argv,exit ##Imported to manage the command line arguments.
from collections import OrderedDict #Ordered dictionary

#Global declarations
debug = True ##Boolean for testing purposes.

packageDependancyDict = {} ##Global dict declaration of initial package -> dependancy relationships

itemdependancies = [] #Holds the dependancies of a given package
itemandDependanciesDict = OrderedDict() ##Dictionary of all items with key= packagename and values = dependancies

##Set up while checking the number of arguments sent to the terminal.
def setup():

	##Function to start testing.
	#testing()

	##If no arguments,tell user to input some.
	if (len(argv) <= 1):
		print("Please input a set of package dependancies")

	##If enough arguments then pass the number of packages to search for.
	elif(len(argv) >= 2):
		dependancySearcher(len(argv) - 2)

##Function to look for the dependancies of the given packages.
def dependancySearcher(numberPackageDependancies):

	##Global variable declarations
	global itemdependancies,overalldependancies,debug

	##Local variables
	packageDependancies = ""
	dictItemDependancies = {}
	interimdependancies = []

	##debugger(numberPackageDependancies)

	##Print number of arguments.
	#debugger(len(argv))

	##Read in all the packages and dependancies from the file specified through the terminal.
	packageDependancies = readFile(argv[1])

	#print(packageDependancies)

	#Handle errors with the packages.txt file.
	if (packageDependancies == None):
		print("Please input a set of package dependancies into file: %s" % argv[1])
		pass

	
	else:
		#Remove spaces
		packageDependancies= filter(lambda x: not x.isspace(), packageDependancies)

		##Populate the dict of package dependancy pairs.
		populatePackageDependancyDict(packageDependancies)

		##For loop which runs for the numberOfPackageDependancies.
		performSearch(numberPackageDependancies)
		
		#print(itemandDependanciesDict)

		##Result of the overall dependancy search is worked out.
		##Using the dictionary of compiled keys(packages) and values(dependancies)
		dependancyResultCalculator(itemandDependanciesDict)


##Populates a dictionary of (package,dependancy) pairs.
def populatePackageDependancyDict(packageDependancies):

	global packageDependancyDict

	##For loop for the length of the number of packages and dependancies returned.
	for i in range(0,len(packageDependancies)):

		##Split by -> to seperate key(package) = values(string of dependancies)
		interimdependancies = packageDependancies[i].strip().split("->")
		#debugger(itemDependancies)

		if(interimdependancies[0] == ''):
			print("Line %s(in file without spaces): missing package name - so is invalid" % (i+1))
			exit()

		else:
			##Create dictionary of packages and associated values
			packageDependancyDict[interimdependancies[0].replace(" ","")] = interimdependancies[1]
 
		#print(packageDependancyDict)

##Recursively search into each package based on their dependancies.
def performSearch(numberPackageDependancies):

	global itemdependancies

	#Local
	recursiveListCounter = []

	##For loop which runs for the numberOfPackageDependancies.
	for i in range(0,numberPackageDependancies):
		
		#debugger("i: %s \n" % i)
		#print(argv[i+1])

		##Recursively searching into each of the package dependancy avenues.
		recursiveItemSearch(argv[i+2],packageDependancyDict,recursiveListCounter)
		#debugger(itemdependancies)

		itemdependancies.sort()
		##Use global dependancies for that package to populate a dictionary.
		itemandDependanciesDict[argv[i+2]] = ' '.join(itemdependancies)
		#Set item dependancies to be empty.
		itemdependancies = []
		recursiveListCounter = []

#Recursively search for a packages dependancies.
def recursiveItemSearch(packageName,dictItemDependancies,recursiveListCounter):

	#print("Item:" + packageName )
	##Global variables
	global itemdependancies
	##Local variables
	dependancies = []
	recursiveStop = ""

	recursiveStop = packageName
	
	#Handle if there are no dependancies for a given package.
	if(dictItemDependancies.get(packageName) == None):
		#("Leaf node : %s" % packageName)
		pass

	#elif (packageName in itemandDependanciesDict):
		#print("repeat")

	#If there are at least 1 dependancy to satisfy then run the code.
	elif len(dictItemDependancies.get(packageName)) >= 1:
		#print("%s ->%s"  % (packageName, dictItemDependancies.get(packageName)))

		##Split by a space to find the dependancies and add to a list.
		dependancies = dictItemDependancies.get(packageName).strip().split(" ")

		##For each dependancy found add all dependancies to itemlist 
		##before re-running the recursive routine.
		for i in range(0,len(dependancies)):

					##Handle problems with looping.

					if(dependancies[i] == recursiveStop):
						itemdependancies.append("[Dependant on itself]")
						return 0

					elif(dependancies[i] in recursiveListCounter):
						break

					else:
						recursiveListCounter.append(recursiveStop)
						recursiveListCounter.append(dependancies[i])
						itemdependancies.append(dependancies[i])

		recursiveItemSearch(dependancies[i],dictItemDependancies,recursiveListCounter)

def readFile(filename): #Needs to be set to the filename of the packages text file.

	while True:
		try:
			with open(filename, "r") as file:
				return file.readlines()
	    	
	    	except IOError as e:
	    		print "I/O error({0}): {1}".format(e.errno, e.strerror)
	    		break


##Takes the result as a dictionary and processes it
##Printing keys associated with their values in the form of strings.
def dependancyResultCalculator(result):

	for key in result:

		if(result[key] == []):
			print("%s -> "  % (key) )

		else:
	 		print("%s -> %s" % (key,result[key]))

def testing():
	global debug

	if(debug == True):
		print("******************************")
		print("******DebugMode Enabled*******")
		print("******************************")

def debugger(message):

	if(debug == True):
		print("Result of testing :" + str(message))
		print("\n")

setup()