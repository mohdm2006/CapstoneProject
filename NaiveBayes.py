import pandas as pd
from sklearn import naive_bayes
from sklearn import tree
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle

# -------------------------- uplaoding the data set and doing the tf_idf ------------------------ :
data = pd.read_csv('FinalDataset.csv')
data.dropna(inplace = True)
data["text"]= data["text"].str.split(",", n=1, expand=True)
trainDF = pd.DataFrame()
trainDF['text'] = data["text"]
trainDF['label'] = data["category"]
shuffling = shuffle(trainDF)
vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5, min_df=3, stop_words='english', use_idf=True,
								 token_pattern=u"\w{4,}", lowercase=True)
# the training text
x = vectorizer.fit_transform(shuffling['text'])
# label training
y = shuffling['label']
x_train, x_test, y_train, y_test = train_test_split(x,y , test_size=0.30)



# ---------------------- Naivebyes Algorithm ------------------------ :
def performNaive():
	x_train, x_test, y_train, y_test = train_test_split(x,y , test_size=0.30)
	NBClasssifier = naive_bayes.MultinomialNB()
	NBClasssifier.fit(x_train, y_train)
	accuracy = accuracy_score(y_test, NBClasssifier.predict(x_test)) * 100
	conf = confusion_matrix(y_test, NBClasssifier.predict(x_test))
	report = classification_report(y_test, NBClasssifier.predict(x_test))
	print(report)
	print(accuracy)
	return NBClasssifier, [x_train,y_test,vectorizer]

# -------------------- predicting a tweets for naive bayes ---------------- :
def predictingATweet(ATweets):
	NP, trainData = performNaive()
	# x_train = trainData[0]
	# y_test = trainData[1]
	vectorizer = trainData[2]
	doc = vectorizer.transform([ATweets])
	prediction = NP.predict(doc)
	print(prediction)
	# p = NP.predict_proba()

# --------------------- KNN algorithm ------------------------------------- :

def KNeighborsAlgorithm():
	KNN_List = [ ]
	print( "------------- Testing K-Neighbors Classifier With Different K Values -----------------" )
	for i in [ 1, 2, 3, 4, 5]:
		print( "Testing KNN with k= " + str( i ) + ":" )
		KNN = KNeighborsClassifier( n_neighbors = i )
		KNN.fit( x_train, y_train )
		KNN_List.append( KNN )
		conf = confusion_matrix( y_test, KNN.predict( x_test ) )
		accuracy = accuracy_score( y_test, KNN.predict( x_test ) ) * 100
		print('Accuracy = %.3f' % accuracy + "%" )
		print("Confusion Matrix for KNN with k= " + str( i ) + ":" )
		for l in range( 0, len( conf ) ):
			s = [' {0} '.format( elem ) for elem in conf[ l ] ]
			print('{:>12}  {:>12}'.format( KNN.classes_[ l ], str( s ) ) )
		print( "Classification report for KNN with k= " + str( i ) + ":" )
		print('knn', classification_report( y_test, KNN.predict( x_test ) ) )
	return KNN_List

# ---------------------------- Decsion Tree ------------------------ :
def DecsionTree():
	DT = tree.DecisionTreeClassifier()
	DT.fit(x,y)
	accuracy = accuracy_score(y_test, DT.predict(x_test)) * 100
	# print('DT accuracy',accuracy)
	report = classification_report(y_test, DT.predict(x_test))
	#print('DT report', report)
	# print(vectorizer.vocabulary_)
	# doc = vectorizer.transform(["@miabrownex @snapchatsupport odd felx but ok x"])
	# print('The prediction :',DT.predict(doc))
	return DT

# ------------------ Results of the algorithms ----------------------- :
print(vectorizer.vocabulary_)