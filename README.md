## Data Science final project ##

* Brian Seitz
* General Assembly NYC
* April 30, 2014 

### Demo ###

* http://cluster.brnstz.com/

### Problem ###

Music recommendation services can be skewed to recommend songs in a similar
genre or time period. Some listeners may want recommendations that span
different genres.

### Hypothesis ###

By analyzing common words in the lyrics of songs, we can find clusters of music
that are orthogonal to genre, but may still fit the listener's mood or overall
musical taste.

### Dataset Description ###

The Million Song Dataset (MSD) is a set of metadata and audio analysis for one
million popular music tracks, provided by The Echo Nest for public research.

In addition, there is lyric data provided by musicXmatch with word counts for
270,000 tracks (a subset of the million). The words are stemmed and only the
top 5,000 words are counted.

* http://labrosa.ee.columbia.edu/millionsong/
* http://labrosa.ee.columbia.edu/millionsong/musixmatch
* http://labrosa.ee.columbia.edu/millionsong/faq (click "field list")

### Initial exploriation ###

Data visualization of word counts aggregated across all tracks: http://brnstz.com/music/words.html

### Statistical Methods ###

Since the goal is to find unknown clusters of tracks, k-means was the most
appropriate statistical method to use. If the lyric data was full text, I would
have considered natural language algorithms such as LDA (Latent Dirichlet
allocation).

### Feature Selection ###

To focus on creating a non-traditional recommendation service, I decided to use
only the lyric data as independent variables, with common English stop words
removed. The additional data from the MSD helped me retrieve the actual songs
to evaluate the clusters. 

### Obtaining and Transforming the Dataset ###

I had to obtain and process two primary datasets, the overall MSD and the lyric data. 

The lyric data is provided as a .csv file indexed by trackid with word ids
mapped to counts. This is a sparse representation, which doesn't account for
unused words in a track. I transformed this into full csv using
[expand_5000.py](expand_5000.py) so it would be compatible as a k-means input.

The MSD is 300 GB of HDF5 files, available as a public dataset from Amazon.
This can be mounted on an Amazon EC2 instance and read with the h5py lib.

I wrote functions to extract and aggregate this data after clustering, and
output in JSON files in [cluster.py](cluster.py).

* http://aws.amazon.com/datasets/6468931156960467
* http://www.h5py.org/

### Visualization and Analysis ###

I built a UI at http://cluster.brnstz.com/ which lists the clusters ordered by
median distance from the centroid. Each song has a "Listen!" link which tries
to find the song on Spotify and allows the user to listen. Word count charts
for the top words is also listed for each cluster.

The UI source code is in [web.go](web.go).

### Challenges ###

By far, the biggest challenge was scaling the algorithm with 5,000 columns. I
spent most of my time pre-processing the data and optimizing the access to HDF5
files. Ultimately, I limited the analysis to 100,000 songs to fit processing on
a single machine.

The second biggest challenge was lack of evaluation data. Since I was trying to
make recommendations that are orthogonal to traditional tags and genre, I
didn't want to evaluate on the existing MSD metadata. Instead, I evaluated the
track clustering manually with my UI. More on this in the next section.

### Business application / Implementation plan ###

A production implementation would follow the same basic structure that we have,
except it would be distributed and have user feedback.

The backend processing would be a scaled and distributed version of a
clustering algorithm.  It would process new tracks / metadata / ratings
periodically and update a live database cluster.

The user UI would read from the database and provide track recommendations
based on prior user history.

The most valuable asset would be a true userbase. This userbase could evaluate
the recommendations made by the algorithm, determine how effective they are,
and provide data points to improve the algorithm. 

This lyrical approach could be an asset to any music service that wants to
improve its recommendations.

### Interesting clusters ###
* Cluster 0: Very similar, low repeat of words.
* Cluster 1: Spanish songs, "come" is the resolved stemmed version of "como".
* Cluster 3: Love is overtaken by know/never/one. Mostly heavy metal songs. Obscure words, very little repetition.
* Cluster 5: Sad love songs, ponderous. More "know" than "love". Good examples: Placebo, Rufus.
* Cluster 9: Break up songs, resentful.
* Cluster 11: One, never, go, out. World-weary conspiracy songs. First 4...
* Cluster 12: Break up songs, moving on. "go"
* Cluster 13: Desire songs. Up and want.
* Cluster 16: Desire songs, needful.
* Cluster 19: German
* Cluster 22: Italian
* Cluster 23: Romantic, feel. Liz Phair and Boyz II Men.
* Cluster 30: Upbeat poppy love songs.
* Cluster 32: Hip-hop.
