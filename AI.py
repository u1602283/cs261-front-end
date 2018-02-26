from DatRet import DatRet
from datetime import date, timedelta
import Dict

class AI:
	NUM_CATEGORIES = 34 # The number of categories, could do length of dictionary
	NUM_ANOMALIES = 2 # The number of top categories to search for anomalies
	MULTIPLIER = 0.9 # Affects weighting, lower number will prioritise newer queries
	ENTRIES = 20 # The number of entries to read from the file/max entries
	ANOMALY_THREASHOLD = 0.05

	historyList = []

	# Initialise
	def __init__(self):
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
			category = self.code_cat[line]
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
		{a: 3
        b: 4}

		# Set to store weights
		scores = {}

		# Total up scores
        # Separate method?
		weight = 1
		for line in self.historyList:
			category = self.code_cat[line]
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
		if newQuery in self.code_cat: # Check code exists
			self.historyList = [newQuery] + self.historyList
			self.historyList = self.historyList[:self.ENTRIES]
			return 1
		else:
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
		for code in self.code_cat:
			if self.code_cat[code] == category:
				result.append(code)
		return result

	def detectAnomalies(self):
		dr = DatRet()
		result = []

		for line in self.suggestCategories(self.NUM_ANOMALIES):
			print(line)
			for code in self.getCodes(line):
				print(code)
				yesterday = date.today() - timedelta(1)
				day = yesterday.strftime('%Y-%m-%d')
				print(day)
				print('print(dr.diff(symbol="code", start=day))')
				data = dr.diff(symbol=code, start=day)
				print(data)
				if abs(data[1]) > self.ANOMALY_THREASHOLD:
					print(code + " is anomalous")
					result.append(line)
		return result

	# Writes the list to a file
	def writeToFile(self):
		with open("history", "w") as historyFile:
			for line in self.historyList:
				historyFile.write(line + "\n")
