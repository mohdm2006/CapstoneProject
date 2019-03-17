# import math
# from nltk.corpus import stopwords
# from nltk.stem import SnowballStemmer
# import re
# stopWords = set(stopwords.words('english'))
#
# class VSM:
#
# 	def __init__( self, docs ):
# 		"""
#
# 		:return:
# 		"""
# 		self.myDocs = docs
# 		self.termList = [ ]
# 		self.docLists = [ ]
# 		self.docLength = {}
# 		# stemmer = SnowballStemmer(language = 'english')
#
# 		for i in range( 0, len( self.myDocs ) ):
# 			tokens = re.findall(r"[\w']+",self.myDocs[i])
# 			token = ""
# 			for j in range( 0, len( tokens ) ):
# 				token = tokens[ j ]
# 				token = token.lower()
# 				if token not in stopWords:
# 					if token not in self.termList:
# 						doclist = []
# 						self.termList.append( token )
# 						doc = Doc( i, 1 )
# 						doclist.append( doc )
# 						self.docLists.append( doclist )
# 					else:
# 						index = self.termList.index( token )
# 						doclist = self.docLists[ index ]
# 						k = 0
# 						match = False
# 						for aDoc in doclist:
# 							if aDoc.docId == i:
# 								aDoc.tw+= 1
# 								match = True
# 								break
# 							k += 1
# 						if not match:
# 							aDoc = Doc( i, 1 )
# 							doclist.append( aDoc )
#
# 		N = len( self.myDocs )
# 		for i in range(0,N):
# 			self.docLength[i] = 0
# 		for i in range( 0, len( self.termList ) ):
# 			doclist = self.docLists[ i ]
# 			df = len( doclist )
# 			for j in range( 0, len( doclist ) ):
# 				aDoc = doclist[ j ]
# 				if aDoc.tw < 0:
# 					aDoc.tw *= -1
# 				x = 1 + math.log(aDoc.tw)
# 				y = math.log(N / (df * 1.0))
# 				tfidf = x * y
# 				self.docLength[ aDoc.docId ] += math.pow( tfidf, 2 )
# 				aDoc.tw = tfidf
# 				doclist[ j ] = aDoc
#
# 		for i in range( 0, N ):
# 			self.docLength[ i ] = math.sqrt( self.docLength[ i ] )
#
# 	def rankSearch(self, query):
# 		"""
#
# 		:param query:
# 		:return:
# 		"""
# 		docs = {}
#
# 		try:
# 			query = query.lower()
# 			query = re.findall(r"[\w']+",query)
# 			for term in query:
# 				# if term not in self.termList:
# 				# 	return None
# 				if term in stopWords:
# 					continue
# 				index = self.termList.index(term)
# 				# if index < 0:
# 				# 	continue
# 				doclist = self.docLists[index]
# 				w_t = math.log(len(self.myDocs) * 1.0 / len(doclist))
# 				for j in range(0, len(doclist)):
# 					aDoc = doclist[j]
# 					score = w_t * aDoc.tw
# 					if aDoc.docId not in docs.keys():
# 						docs[aDoc.docId] = score
# 					else:
# 						score += docs[aDoc.docId]
# 						docs[aDoc.docId] = score
# 			return docs
# 		except:
# 			return None
#
# 	def __str__( self ):
# 		"""
#
# 		:return:
# 		"""
# 		s = ""
# 		for i in range( 0, len( self.termList ) ):
# 			s+= self.termList[i]
# 			docList = self.docLists[ i ]
# 			for j in range( 0, len( docList ) ):
# 				s += " " + str(docList[ j ])
# 			s += "\n"
# 		return s
#
#
# class Doc:
# 	def __init__( self, did, weight ):
# 		self.docId = did
# 		self.tw = weight
#
# 	def __str__(self):
# 		s = str(self.docId) + ": " + str(self.tw)
# 		return s
#
