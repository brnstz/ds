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

By analyzing common words in the lyrics of songs, we can find clusters of music that are orthogonal 
to genre, but may still fit the listener's mood or overall musical taste.


### Dataset Description ###

The Million Song Dataset (MSD) is a set of metadata and audio analysis for one million popular
music tracks, provided by The Echo Nest for public research.

In addition, there is lyric data provided by musicXmatch with word counts for
270,000 tracks (a subset of the million). The words are stemmed and only the top 5,000
words are counted.

* http://labrosa.ee.columbia.edu/millionsong/
* http://labrosa.ee.columbia.edu/millionsong/musixmatch
* http://labrosa.ee.columbia.edu/millionsong/faq (click "field list")

### Initial exploriation ###

Data visualization of word counts aggregated across all tracks: http://brnstz.com/music/words.html

### Statistical Methods ###

Since the goal is to find unknown clusters of tracks, K-Means was the most appropriate
statistical method to use. If the lyric data was full text, I would have considered
natural language algorithms such as LDA (Latent Dirichlet allocation).

### Feature Selection ###

To focus on creating a non-traditional recommendation service, I decided to use only the
lyric data as independent variables. The additional data from the MSD helped me
retrieve the actual songs to evaluate the clusters.

### Obtaining and Transforming the Dataset ###

I had to obtain and process two primary datasets, the overall MSD and the lyric data. 

The yric data is provided as a .csv file indexed by trackid with word ids 
mapped to counts. This is a sparse representation, which doesn't account for 
unused words in a track. I transformed this into full csv using [expand_5000.py](expand_5000.py).

The MSD is 300 GB of HDF5 files, available as a public dataset from Amazon.
This can be mounted on an Amazon EC2 instance and read with the h5py lib.

I wrote functions to extract and aggregate this data after clustering, and output in 
JSON files in [cluster.py](cluster.py).

* http://aws.amazon.com/datasets/6468931156960467
* http://www.h5py.org/

### Challenges ###



### Business applications ###

### Implementation plan ###
