# data cleaning for articles from tagesspiegel

import json
import os
import re

# get folder path and name

# open all json (?) files in folder

my_path = os.getcwd()
head, tail = os.path.split(my_path)
# assume you are in directory data-cleaning 
#assert tail=="data_cleaning"

# create path to .json files to be cleaned
#path_to_files = os.path.join(head,'tagesspiegel-2020-07-14-only-json')

def clean_up(path_to_folder, date_for_imputing):

	# initialize statistic for data cleaning
	impute_date_count = []
	remove_ad_count = []
	unwanted_files = []

	# r=root, d=directories, f=files
	for _, _, f in os.walk(path_to_folder):
		for file in f:
			if file.endswith(".json"):
				#print(file)
				filename=os.path.join(path_to_folder, file)
				#filename = '../data-acquisition/00530.json'
				with open(filename , 'r') as myfile:
					data=myfile.read()

				# parse file into dict
				article = json.loads(data)
				#print(article)
				# text is now in article['text']

				if article['url'].startswith("https://plus.tagesspiegel.de"):
					unwanted_files += [[filename, 'content from plus.tagesspiegel.de (url)']]
				else:
					if article['type'] != 'article':
						unwanted_files += [[filename, 'too short']]
					else:
					# characterseck length of text. If shorter than 500 characters we don't include the article
						if len(article['text']) < 500: # this counts the letters (and white spaces, not the words)
							unwanted_files += [[filename, 'wrong type: ' + article['type']]]
						else:
							#print('in main else')
							# remove advertisment text in brackets
							regex = re.compile('\[[ / \w \s .,;:\-_„"]*]')	
							# count ad text to be removed
							remove_ad_count += [[file, len(regex.findall(string=article['text']))]]

							# remove ad text
							text_clean = regex.sub(repl='', string=article['text'])
							article['text'] = text_clean
							# check for date of publication, impute if missing
							if article['publish-date'] in ('None',None,''):
								article['publish-date']=date_for_imputing
								impute_date_count += [file]
							# check for empty authors, impute with name of newspaper
							# this catches [  ] as empty but not [[]]
							if not len(article['authors']):							
								article['authors']=[article['paper']]

							# remove closing (tsp) or (tsp,dpa) or similar for press releases
							regex = re.compile("\([\w , / ]*\)\.?$") # we look for ( alpha numeric or , or / or \ 0 times or more ) followed by '.'' or no '.'
							article['text']=regex.sub(repl='', string=article['text'])	

							# create new filename
							split_string = filename.split('.json',1) # split at the dot, split only once and into two parts
							filename_clean = split_string[0]+'-clean.json' # file for storing a clean article in json
							# write clean text article to file
							json_txt = json.dumps(article, indent=4) # dumps , before used dump . What's the difference??
							try:
								with open(filename_clean , 'w', encoding='utf-8') as file:
									file.write(json_txt)
									#print('written file')
							except IOError as e:
								print("Couldn't open or write to file (%s)." % e)

	cleaning_report = dict()
	#print("remove ad text : " , remove_ad_count)
	cleaning_report['files inspected'] = len(list(os.walk(path_to_folder)))-1

	cleaning_report['files with ads'] = len([k for k in range(len(remove_ad_count)) if remove_ad_count[k][1]!=0])

	remove_ad_ctd = sum(remove_ad_count[i][1] for i in range(len(remove_ad_count)))
	cleaning_report['ads removed']=remove_ad_ctd
	#print("remove files : " , unwanted_files)
	cleaning_report['files not clean'] = len(unwanted_files)
	cleaning_report['files bot clean reasons'] = [unwanted_files[k][1] for k in range(len(unwanted_files))]
	cleaning_report['dates imputed']= len(impute_date_count)
	
	return(cleaning_report)

if __name__ == "__main__":
	report = clean_up("../tagesspiegel-2020-09-05","2020-09-09")
	print(report)