# create a newsreader with an ML feature

We follow a pipeline. There are 4 steps we go through. Each step is seperate and independent of the others:

 * data acquisition: we scrape from German newspaper tagesspiegel.de
  * data cleaning: remove ads, impute missing dates of publication, remove tags for press releases from the article text, remove articles with less than 500 words, ...
   * ML task: We cluster articles with Kmeans. We optimize over the number of clusters and two other parameters in the tfidf vectorizer. 
   * HTML presentation: We start a Flask web server and dynamically present the scraped and clustered articles. Readers can choose a clusters and from a specified cluster choose an article. The article text can be read to the reader (the reader becomes a listener)

We have a Jupyter Notebook (workflow.ipynb) guiding us throgh the steps.

## data acquisition

So far I get data from the Berlin based German newspaper tagesspiegel.de. I get the links with beautiful soup and download the articles with newspaper3k. I dump them as JSON. There is no database. Reference is through filenames: 00001.json.

I have scraped www.tagesspiegel.de for the last month collecting more than 1K articles. I only work with relatively new articles, partly because in the beginning I did not download and save the image urls - but i need them in the html presentation, the newsreader web interface for the end user / reader. Also: clustering (relatively) new news makes more sense to me.

I am not working with word embeddings. If I did, a large corpus of articles would be needed.

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

There should be a test, if articles pass all technical requirements to be displayed in the newsreader (like: all required variables exist).

## ML task: clustering with Kmeans

I cluster all scraped articles with KMeans. I use sklearn Pipelines. We can cluster using the whole text of the article (many words, more information, longer processing time) or the title (few words, litte information, short processing time).

We investigate some of our options:
Should we cluster articles wrt their titles or wrt their full length text?
Actually we could start with clustering wrt titles (fast, reduced information / few words) and use these clusters as initial clusters for the clustering wrt the full text (slower, more information / many words).

Before clustering we preprocess the text y removing (German) stoppwords and stemming and lemmatizing (German, again). We then send the chosen text type (titles or full texts) through an vectorizer based on term frequency and inverse document frequency. We optimize min_df and max_df.

When clustering we optimize over the number of clusters: 5,10 or 15.

##  presentation as html

We work with flask to set up an html server that we access through our browser. We can now click through our scraped and clusteres articles.