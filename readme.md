# create a newsreader with an ML feature

We follow a pipeline. There are (at the moment) 4 steps we go through. Each step is seperate and independent of the others. In the end there will be a jupyter notebook going through all steps.

## data acquisition

So far I get data from a german and a US newspaper. I get the links with beautiful soup and download the articles with newspaper3k. I dump them as JSON for the meta data and as plain text for the articles text. There is no database. Reference is through filenames: 00001.json for the meta data and 00001.txt for the main text.

at the moment I am not downloading images. However, I kept links to the top image and all images in meta data.

Since I cannot work with two langauges (and I get more articles from tagesspiegel than from the ny times), I will only work with the german newspaper. I should add another or better two more German newspapers.

## data cleaning ...

... might have to follow. Some articles I get are plain adverts. I have a 'type' (with the option 'article') in the meta data that could help here.

Not doing any data cleaning at the moment. Will do only if required by the ML task.

There should be an overview of the quality of the selected data:

* How long are the articles (are they indeed articles, i.e are they long enough to qualify as an article?)
* Are there missing values in title, date of publication, authors? Impute or throw out?

## ML task: clustering with Kmeans

I cluster all scraped articles with KMeans. I use sklearn Pipelines. The result is pretty bad, I guess. I get 2 clusters of almost equal size, at best. The remaining "clusters" are of size 1.

##  presentation as html

There will be a html page (dynamically generated) that presents the user with a list of clusters. The user may select a cluster.

The newsreader then presents a list of titles that belong to articles in the selected cluster. The user may select a title.

The newsreader then presents the text of the selected title (belonging to the selected cluster).