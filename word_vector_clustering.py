from __future__ import division
from sklearn.cluster import MiniBatchKMeans 
from numbers import Number
from pandas import DataFrame
import sys, codecs, numpy, json

class autovivify_list(dict):
    '''Pickleable class to replicate the functionality of collections.defaultdict'''
    def __missing__(self, key):
        value = self[key] = []
        return value
    
    def __add__(self, x):
        '''Override addition for numeric types when self is empty'''
        if not self and isinstance(x, Number):
            return x
        raise ValueError
        
    def __sub__(self, x):
        '''Also provide subtraction method'''
        if not self and isinstance(x, Number):
            return -1 * x
        raise ValueError

def build_word_vector_matrix(vectors):
    '''Iterate over the GloVe array read from sys.argv[1] and return its vectors and labels as arrays'''
    numpy_arrays = []
    labels_array = []
    for key in vectors.keys():   
        labels_array.append(key)
        numpy_arrays.append( numpy.array(vectors[key]))

    return numpy.array( numpy_arrays ), labels_array            

def find_word_clusters(labels_array, cluster_labels):
    '''Read in the labels array and clusters label and return the set of words in each cluster'''
    cluster_to_words = autovivify_list() 
    for c, i in enumerate(cluster_labels):
        cluster_to_words[ str(i) ].append( labels_array[c] )
    return cluster_to_words

def recluster(vectors):
    clusters_to_make  = int( len(vectors) * reduction_factor) 

    df, labels_array  = build_word_vector_matrix(vectors)
    kmeans_model      = MiniBatchKMeans(init='k-means++', n_clusters=clusters_to_make)
    kmeans_model.fit(df)

    cluster_labels    = kmeans_model.labels_
    cluster_inertia   = kmeans_model.inertia_   
    cluster_to_words  = find_word_clusters(labels_array, cluster_labels)

if __name__ == "__main__":

    input_vector_file = sys.argv[1]
    reduction_factor  = float(sys.argv[2])

    with open(input_vector_file) as data_file:    
        vectors = json.load(data_file)

    while len(vectors) > 2:
        clusters_to_make  = int( len(vectors) * reduction_factor) 

        df, labels_array  = build_word_vector_matrix(vectors)
        kmeans_model      = MiniBatchKMeans(init='k-means++', n_clusters=clusters_to_make)
        kmeans_model.fit(df)

        cluster_labels    = kmeans_model.labels_
        cluster_inertia   = kmeans_model.inertia_   
        cluster_to_words  = find_word_clusters(labels_array, cluster_labels)

        for c in cluster_to_words:
            if len(cluster_to_words[c]) > 1 and len(cluster_to_words[c]) < 20:
                print cluster_to_words[c]
                for word in cluster_to_words[c]:
                    del vectors[word]


