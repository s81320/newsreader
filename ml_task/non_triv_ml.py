import re

from textblob_de import TextBlobDE 

import glob
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

import math

import json


def preprocess(text):
    #print(text)
    a = text.lower() # lower cases only
    b = re.sub("(\\W|\\d)"," ",a) #remove non-ascii and digits
    blob = TextBlobDE(b)
    return(blob.words.lemmatize()) # lemmatize for german


def read_articles_transform_to_df (path_to_text_files='articles_02/*clean.json', debug=False):

	file_list=glob.glob(path_to_text_files)
	#file_list = glob.glob("../tagesspiegel/*.txt")
	#print(file_list)

	n = len(file_list)
	print(n , "files to work with.")
	if debug==True:
		n_restrict = 50
		print('debug mode, working with a subset of ' + str(n_restrict) + ' files.')
		n = n_restrict
        
	#list_of_articles = []
	X = pd.DataFrame(columns=['file','file_name','title','text','description','date','image'])

	for i in range(n):
		if debug:
			#print('*** '+str(i)+' ***' + file_list[i])
			pass
		with open (file_list[i]) as file:
			article = json.loads(file.read())
		X=X.append({'file':file_list[i] , 'file_name':article['text-link'], 'text':article['text'], 'title':article['title'], 'description':article['description'], 'date':article['publish-date'], 'image':article['image']}, ignore_index=True)
	return(X)

def enthropy(pv):
	# should check, that all values are positive and sum to (about) 1
	return(-sum([pv[i]*math.log(pv[i]) for i in range(len(pv))]))

def evaluate_cluster(km_object):
	n, bins, patches = plt.hist(km_object.labels_, km_object.n_clusters, facecolor='blue', alpha=0.5)
	plt.title('sizes of clusters')
	plt.ylabel('nr. of articles')
	plt.show()

	rel_fq = [round(ni/sum(n),3) for ni in n] 
#		print('elements in bins: ' , n)
#		print('relative size of bins: ', rel_fq)
#		print('enthropy: ', enthropy(rel_fq))

	return({'n': n , 'frequencies': rel_fq , 'enthropy': enthropy(rel_fq), 'inertia':km_object.inertia_})

if __name__ == "__main__":
	print('import me (non_triv_ml), call my functions.')