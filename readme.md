# create a newsreader with an ML feature

We follow a pipeline. There are (at the moment) 4 steps we go through. Each step is seperate and independent of the others:

 * data acquisition: we scrape from German newspapers and online publications
  * data cleaning: remove ads, impute missing dates of publication, remove tags for press releases from the article text, if the text is too short it does not qualify and will be left out from downstream tasks, ...
   * ML task: We cluster articles in 5 groups. 
   * HTML presentation: We start a Flask web server and dynamically present the scraped and clustered articles. Readers can choose a clusters and from a specified cluster choose an article. The article text can be read to the reader (the reader becomes a listener)

We have a Jupyter Notebook (workflow.ipynb) guiding us throgh the steps.

## data acquisition

So far I get data from a german and a US newspaper. I get the links with beautiful soup and download the articles with newspaper3k. I dump them as JSON for the meta data and as plain text for the articles text. There is no database. Reference is through filenames: 00001.json.

at the moment I am not downloading images. However, I kept links to the top image and all images in meta data.

I have scraped www.tagesspiegel.de for the last month collecting more than 1K articles. It would be nice to have (at least one) other source(s), like www.sueddeutsche.de or www.dw.com/de (Deutsche Welle).

## data cleaning ...

The data cleaning returns a dictionaly with information on: 
 * How many files have been inspected
 * How many ads have been removed from how many files.
 * How often the date has been imputed
 * how many scraped articles did not meet our quality criteria

Overview of the quality of the selected data:

* Articles are at least 500 words long
* multimedia collections are not considered articles
* infotainment is not considered articles

## ML task: clustering with Kmeans

I cluster all scraped articles with KMeans. I use sklearn Pipelines. We can cluster using the whole text of the article (many words, more informatio, longer processing time) or the title (few words, litte information, short processing time).

Before clustering we send the chosen text type (titles or texts) throu an vectorizer based on term frequency and inverse document frequency.

We should optimize hyperparamters like number of clusters.

##  presentation as html

There will be a html page (dynamically generated) that presents the user with a list of clusters. The user may select a cluster.

The newsreader then presents a list of titles that belong to articles in the selected cluster. The user may select a title.

The newsreader then presents the text of the selected title (belonging to the selected cluster) as speech.