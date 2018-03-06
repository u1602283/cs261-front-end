from DatRet import DatRet
from datetime import date, timedelta
import Dict

class AI:
	
	historyList = []
	TOTAL_CATEGORIES = 34 # The number of categories, could do length of dictionary
	
	# Initialise
	def __init__(
			self,
			NUM_CATEGORIES = 2, # The number of top categories to search for anomalies
			MULTIPLIER = 0.9, # Affects weighting, lower number will prioritise newer queries
			ENTRIES = 20, # The number of entries to read from the file/max entries
			ANOMALY_THREASHOLD = 0.05 # Threashold to identify as anomaly
			):
		self.NUM_CATEGORIES = NUM_CATEGORIES
		self.MULTIPLIER = MULTIPLIER
		self.ENTRIES = ENTRIES
		self.ANOMALY_THREASHOLD = ANOMALY_THREASHOLD
		try:
			with open("history", "r") as historyFile:
				self.historyList = historyFile.read().splitlines() # TODO Should find a way to read a given amount of lines and stop if not enough as opposed to reading whole file
				self.historyList[:self.ENTRIES]
		except FileNotFoundError:
			print("File not found")
			self.historyList = []
			
	# Returns a string of the highest weighted category
	def suggestCategory(self):
		# If the list is empty
		if len(self.historyList) == 0:
			return ""
			
		# Dictionary to store weights
		scores = {}
		
		# Total up scores
		weight = 1
		for line in self.historyList:
			category = Dict.code_cat[line]
			if not line in scores:
				scores[category] = 0
			scores[category] += weight
			weight = weight * self.MULTIPLIER
			
		# Get the index of highest score
		result = max(scores, key=scores.get)
		return result
		
	# Returns a string of the highest weighted category
	def suggestCategories(self, amount):
		# If the list is empty
		if len(self.historyList) == 0:
			return []
			
		# Set to store weights
		scores = {}
		
		# Total up scores
		# Separate method?
		weight = 1
		for line in self.historyList:
			category = Dict.code_cat[line]
			if not line in scores:
				scores[category] = 0
			scores[category] += weight
			weight = weight * self.MULTIPLIER
			
		# Get highest scores
		result = []
		for i in range(int(amount)):
			top = max(scores, key=scores.get)
			if scores[top] == 0:
				break
			result.append(top)
			scores[top] = 0
		return result
		
	# Adds a query to the search history, returns 1 on success, 0 on failure
	def addQuery(self, newQuery):
		newQuery = newQuery.upper()
		if newQuery in Dict.code_cat: # Check code exists
			self.historyList = [newQuery] + self.historyList
			self.historyList = self.historyList[:self.ENTRIES]
			print("Added " + newQuery + ": " + Dict.code_name[newQuery])
			return 1
		else:
			print(newQuery + " is not a valid company code")
			return 0
			
	# Clear the history
	def clearHistory(self):
		self.historyList = []
		
	# Return a list containing the history
	def getList(self):
		return self.historyList
		
	# Return a list containing codes within given category
	def getCodes(self, category):
		result = []
		for code in Dict.code_cat:
			if Dict.code_cat[code] == category:
				result.append(code)
		return result
		
	# Return a sorted list of anomalous company codes
	def detectAnomalies(self, DICT = False):
		dr = DatRet()
		resultList = []
		resultDict = {}
		
		for line in self.suggestCategories(self.NUM_CATEGORIES):
			print(line)
			for code in self.getCodes(line):
				print(code)
				day = date.today().strftime('%Y-%m-%d')
				print(day)
				print('print(dr.diff(symbol="code", start=day))')
				data = dr.diff(symbol=code, start=day)
				print(data)
				if abs(data[1])/100 > self.ANOMALY_THREASHOLD:
					print(code + " is anomalous")
					resultList.append([code, data[1]])
					resultDict["code"] = code
					resultDict["diff"] = data[1]
				print()
		resultList.sort(key = lambda x: abs(x[1]), reverse = True)
		print(resultList)
		print(resultDict)
		if DICT == True:
			return resultDict
		else:
			return resultList
		
	# Writes the list to a file
	def writeToFile(self):
		print("Writing to file..")
		with open("history", "w") as historyFile:
			for line in self.historyList:
				print("Writing line: " + line)
				historyFile.write(line + "\n")
#ai = AI(ANOMALY_THREASHOLD = 0.01)
#ai.addQuery("AAK")
#ai.addQuery("AAL")
#ai.addQuery("AAl")
#ai.detectAnomalies(DICT = True)
#ai.detectAnomalies()
