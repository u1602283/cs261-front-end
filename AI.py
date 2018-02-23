from DatRet import DatRet
class AI:
	NUM_CATEGORIES = 34 # The number of categories, could do length of dictionary
	NUM_ANOMALIES = 2 # The number of top categories to search for anomalies
	MULTIPLIER = 0.9 # Affects weighting, lower number will prioritise newer queries
	ENTRIES = 20 # The number of entries to read from the file/max entries
	
	code_cat = { # Assigns a category to each stock code
		"AAL":"Mining",
		"ABF":"Food Producers",
		"ADM":"Nonlife Insurance",
		"AHT":"Support Services",
		"ANTO":"Mining",
		"AV":"Life Insurance",
		"AZN":"Pharmaceuticals & Biotechnology",
		"BA":"Aerospace & Defense",
		"BARC":"Banks",
		"BATS":"Tobacco",
		"BDEV":"Household Goods & Home Construction",
		"BKG":"Household Goods & Home Construction",
		"BLND":"Real Estate Investment Trusts",
		"BLT":"Mining",
		"BNZL":"Support Services",
		"BP":"Oil & Gas Producers",
		"BRBY":"Personal Goods",
		"BTA":"Fixed Line Telecommunications",
		"CCH":"Beverages",
		"CCL":"Travel & Leisure",
		"CNA":"Gas, Water & Multiutilities",
		"CPG":"Travel & Leisure",
		"CRDA":"Chemicals",
		"CRH":"Construction & Materials",
		"DCC":"Support Services",
		"DGE":"Beverages",
		"DLG":"Nonlife Insurance",
		"EVR":"Industrial Metals & Mining",
		"EXPN":"Support Services",
		"EZJ":"Travel & Leisure",
		"FERG":"Support Services",
		"FRES":"Mining",
		"GFS":"Support Services",
		"GKN":"Automobiles & Parts",
		"GLEN":"Mining",
		"GSK":"Pharmaceuticals & Biotechnology",
		"HL":"Financial Services",
		"HLMA":"Electronic & Electrical Equipment",
		"HMSO":"Real Estate Investment Trusts",
		"HSBA":"Banks",
		"IAG":"Travel & Leisure",
		"IHG":"Travel & Leisure",
		"III":"Financial Services",
		"IMB":"Tobacco",
		"INF":"Media",
		"ITRK":"Support Services",
		"ITV":"Media",
		"JE":"General Retailers",
		"JMAT":"Chemicals",
		"KGF":"General Retailers",
		"LAND":"Real Estate Investment Trusts",
		"LGEN":"Life Insurance",
		"LLOY":"Banks",
		"LSE":"Financial Services",
		"MCRO":"Software & Computer Services",
		"MDC":"Health Care Equipment & Services",
		"MKS":"General Retailers",
		"MNDI":"Forestry & Paper",
		"MRW":"Food & Drug Retailers",
		"NG":"Gas, Water & Multiutilities",
		"NMC":"Health Care Equipment & Services",
		"NXT":"General Retailers",
		"OML":"Life Insurance",
		"PPB":"Travel & Leisure",
		"PRU":"Life Insurance",
		"PSN":"Household Goods & Home Construction",
		"PSON":"Media",
		"RB":"Household Goods & Home Construction",
		"RBS":"Banks",
		"RDSA":"Oil & Gas Producers",
		"REL":"Media",
		"RIO":"Mining",
		"RR":"Aerospace & Defense",
		"RRS":"Mining",
		"RSA":"Nonlife Insurance",
		"RTO":"Support Services",
		"SBRY":"Food & Drug Retailers",
		"SDR":"Financial Services",
		"SGE":"Software & Computer Services",
		"SGRO":"Real Estate Investment Trusts",
		"SHP":"Pharmaceuticals & Biotechnology",
		"SKG":"General Industrials",
		"SKY":"Media",
		"SLA":"Financial Services",
		"SMDS":"General Industrials",
		"SMIN":"General Industrials",
		"SMT":"Equity Investment Instruments",
		"SN":"Health Care Equipment & Services",
		"SSE":"Electricity",
		"STAN":"Banks",
		"STJ":"Life Insurance",
		"SVT":"Gas, Water & Multiutilities",
		"TSCO":"Food & Drug Retailers",
		"TUI":"Travel & Leisure",
		"TW":"Household Goods & Home Construction",
		"ULVR":"Personal Goods",
		"UU":"Gas, Water & Multiutilities",
		"VOD":"Mobile Telecommunications",
		"WPP":"Media",
		"WTB":"Retail hospitality"
	}
	
	code_name = { # Translates code to name
		"III":"3i",
		"ADM":"Admiral Group",
		"AAL":"Anglo American plc",
		"ANTO":"Antofagasta",
		"AHT":"Ashtead Group",
		"ABF":"Associated British Foods",
		"AZN":"AstraZeneca",
		"AV":"Aviva",
		"BA":"BAE Systems",
		"BARC":"Barclays",
		"BDEV":"Barratt Developments",
		"BKG":"Berkeley Group Holdings",
		"BLT":"BHP",
		"BP":"BP",
		"BATS":"British American Tobacco",
		"BLND":"British Land",
		"BTA":"BT Group",
		"BNZL":"Bunzl",
		"BRBY":"Burberry",
		"CCL":"Carnival Corporation & plc",
		"CNA":"Centrica",
		"CCH":"Coca-Cola HBC AG",
		"CPG":"Compass Group",
		"CRH":"CRH plc",
		"CRDA":"Croda International",
		"DCC":"DCC plc",
		"DGE":"Diageo",
		"DLG":"Direct Line Group",
		"EZJ":"easyJet",
		"EVR":"Evraz",
		"EXPN":"Experian",
		"FERG":"Ferguson plc",
		"FRES":"Fresnillo plc",
		"GFS":"G4S",
		"GKN":"GKN",
		"GSK":"GlaxoSmithKline",
		"GLEN":"Glencore",
		"HLMA":"Halma",
		"HMSO":"Hammerson",
		"HL":"Hargreaves Lansdown",
		"HSBA":"HSBC",
		"IMB":"Imperial Brands",
		"INF":"Informa",
		"IHG":"InterContinental Hotels Group",
		"IAG":"International Airlines Group",
		"ITRK":"Intertek",
		"ITV":"ITV plc",
		"JMAT":"Johnson Matthey",
		"JE":"Just Eat",
		"KGF":"Kingfisher plc",
		"LAND":"Land Securities",
		"LGEN":"Legal & General",
		"LLOY":"Lloyds Banking Group",
		"LSE":"London Stock Exchange Group",
		"MKS":"Marks & Spencer",
		"MDC":"Mediclinic International",
		"MCRO":"Micro Focus",
		"MNDI":"Mondi",
		"MRW":"Morrisons",
		"NG":"National Grid plc",
		"NXT":"Next plc",
		"NMC":"NMC Health",
		"OML":"Old Mutual",
		"PPB":"Paddy Power Betfair",
		"PSON":"Pearson PLC",
		"PSN":"Persimmon plc",
		"PRU":"Prudential plc",
		"RRS":"Randgold Resources",
		"RB":"Reckitt Benckiser",
		"REL":"RELX Group",
		"RTO":"Rentokil Initial",
		"RIO":"Rio Tinto Group",
		"RR":"Rolls-Royce Holdings",
		"RBS":"The Royal Bank of Scotland Group",
		"RDSA":"Royal Dutch Shell",
		"RSA":"RSA Insurance Group",
		"SGE":"Sage Group",
		"SBRY":"Sainsbury's",
		"SDR":"Schroders",
		"SMT":"Scottish Mortgage Investment Trust",
		"SGRO":"Segro",
		"SVT":"Severn Trent",
		"SHP":"Shire plc",
		"SKY":"Sky plc",
		"SN":"Smith & Nephew",
		"SMDS":"Smith, DS",
		"SMIN":"Smiths Group",
		"SKG":"Smurfit Kappa",
		"SSE":"SSE plc",
		"STAN":"Standard Chartered",
		"SLA":"Standard Life Aberdeen",
		"STJ":"St James's Place plc",
		"TW":"Taylor Wimpey",
		"TSCO":"Tesco",
		"TUI":"TUI Group",
		"ULVR":"Unilever",
		"UU":"United Utilities",
		"VOD":"Vodafone Group",
		"WTB":"Whitbread",
		"WPP":"WPP plc"
	}
	
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
			return ""
		
		# Set to store weights
		scores = {}
			
		# Total up scores
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
		
	def detectAnomalies(self):
		dr = DatRet()
		result = []
#		for line in suggestCategories(NUM_ANOMALIES):
#			if anomalous:
#				result.append(line)
		return result
		
	# Writes the list to a file
	def writeToFile(self):
		with open("history", "w") as historyFile:
			for line in self.historyList:
				historyFile.write(line + "\n")