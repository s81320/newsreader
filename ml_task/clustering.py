import os

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans

import re

from textblob_de import TextBlobDE 

import glob
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

import math


def preprocessing_02 (text):
    #print(text)
    a = text.lower() # lower cases only
    b = re.sub("(\\W|\\d)"," ",a) #remove non-ascii and digits
    blob = TextBlobDE(b)
    return(blob.words.lemmatize()) # lemmatize for german



def read_articles_transform_to_df (path_to_text_files='../tagesspiegel/*.txt'):

	file_list=glob.glob(path_to_text_files)
	#file_list = glob.glob("../tagesspiegel/*.txt")
	#print(file_list)

	n = len(file_list)
	print(n , "files to work with.")

	#list_of_articles = []
	X = pd.DataFrame(columns=['file','text'])
	#print('df', X)

	for i in range(n):
		with open (file_list[i]) as file:
			text=file.read()
			X=X.append({'file':file_list[i] , 'text':text}, ignore_index=True)
	print(X.shape)
	return(X)

def enthropy(pv):

	# should check, that all values are positive and sum to (about) 1
	return(-sum([pv[i]*math.log(pv[i]) for i in range(len(pv))]))

def evaluate_cluster(km_object, modus):
	n, bins, patches = plt.hist(km_object.labels_, km_object.n_clusters, facecolor='blue', alpha=0.5)
	if modus==0:
		plt.title('sizes of clusters')
		plt.ylabel('nr. of articles')
		plt.show()
		return_value=1
	elif modus==1:
		rel_fq = [round(ni/sum(n),3) for ni in n] 
#		print('elements in bins: ' , n)
#		print('relative size of bins: ', rel_fq)
#		print('enthropy: ', enthropy(rel_fq))
		return_value = {'n': n , 'frequencies': rel_fq , 'enthropy': enthropy(rel_fq)}
	elif modus==2:
		return_value = km_object.inertia_
	else:
		return_value='modus 0,1 or 2, please.'
	return(return_value)

X = read_articles_transform_to_df('../tagesspiegel_01/*clean.json')

list_of_articles = X['text']

cv = TfidfVectorizer(max_df=0.8 , min_df =2)
print('cv: ' , dir(cv))
km =  KMeans(init='k-means++', n_clusters=5, n_init=10)

text_cluster = Pipeline([('vect', cv), ('cluster', km) ])

text_cluster.fit(list_of_articles[0:100])
#text_cluster.fit(list_of_articles)

#labels_as_column = pd.DataFrame(km.labels_)
#print(type(labels_as_column), labels_as_column.shape)

X['cluster'] = pd.DataFrame(km.labels_) # contains labels
#print(X)

print('inertia: ' , km.inertia_)
centers = np.array(km.cluster_centers_)
print(centers.shape)

evaluate_cluster(km,modus=1)

# make it a new column in DataFrame X
