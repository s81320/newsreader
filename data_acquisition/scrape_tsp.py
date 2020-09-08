import requests
import urllib.request
from datetime import date
import pandas as pd

from bs4 import BeautifulSoup

from newspaper import Article
import time
import sys , os
import json


def get_links ():
	'''get links from tagesspiegel.de and write them to links-tsp-<date_today>.txt'''
	url= 'http://www.tagesspiegel.de'
	response = requests.get(url)
	print(response)
	soup = BeautifulSoup(response.text , "html.parser")

	all_a = soup.findAll('a')

	link_list = []
	for one_a in all_a:
		if ( one_a['href'][-5:]== '.html' ):
			if(one_a['href'][0:4]=='http') :
				link_list.append(one_a['href'])  
			else:
				link_list.append('https://www.tagesspiegel.de' + one_a['href'])

	link_list = list(set(link_list))

	file_name = 'data_acquisition/links-tsp-' + str(date.today()) + '.txt'
	with open(file_name , "w") as file:
		for link in link_list:
			file.write(link + '\n')

	return('wrote ' + str(len(link_list)) + ' links to ' + file_name)

def create_set_link_ids(file_links):
	file_ids = set()

	# ids from the links we already collected

	with open( file_links , "r") as link_file:
		all_lines = link_file.readlines()
		for line in all_lines:
			#print(line[-14:-1])
			file_ids.update([line[-14:-1]]) # put the string in [] or else it will be split into characters

	return(file_ids)


def select_new_links(scraped_file , bestands_file = "data_acquisition/links-tsp-bestand.txt"):

	ids_bestand = create_set_link_ids(bestands_file)
	ids_scraped = create_set_link_ids(scraped_file)

	ids_new = set(ids_scraped).difference(set(ids_bestand))

	split_string = scraped_file.split('.',1) # split at the dot, split only once and into two parts
	new_file = split_string[0]+'-new.'+split_string[1] # file for new links

	with open(new_file , "w") as write_file , open(scraped_file , "r") as read_file:
		all_lines = read_file.readlines()
		for line in all_lines:
			#print(line)
			if(line[-14:-1] in ids_new):
				write_file.write(line)

def get_content(path_to_link_file , file_number , path_to_output_folder):
	assert type(file_number) == int, "second argument to get_content should be an integer."
	#with open("../data-acquisition/links-tsp-2020-07-14-new.txt" , "r") as link_file :
	with open(path_to_link_file, "r") as link_file :
		all_lines = link_file.readlines()
		for link in all_lines:
			link = link.replace('\n', '')
			article = Article(link)
			article.download()
			time.sleep(2)
			article.parse()
			
			## generate a filename
			file_number+=1
			filename = f'{file_number:05}'
			# should check, if file exists ...

			keep = article.meta_data['og']
			keep['authors'] = article.authors
			keep['text-link'] = filename
			keep['publish-date'] = str(article.publish_date)
			keep['paper'] = 'tagesspiegel'
			keep['id'] = link[-13:-5]
			keep['text'] = article.text

			json_txt = json.dumps(keep, indent=4)
			filename=os.path.join(path_to_output_folder, filename + ".json")
			with open(filename, 'w', encoding='utf-8') as file:
				file.write(json_txt)		
	return(file_number)

if __name__ == "__main__":
	print('import me (scrape_tsp), call my functions.')


