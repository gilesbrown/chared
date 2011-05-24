# Copyright (c) 2011 Vit Suchomel and Jan Pomikalek
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.

"""Character encoding detection library."""

import os
import sys
import cPickle as pickle

def list_models():
    "Returns a list of inbuilt models."
    models = []
    models_dir = os.path.join(
        os.path.dirname(sys.modules['chared'].__file__), 'models')
    for filename in os.listdir(models_dir):
        if filename.endswith('.edm'):
            models.append(filename.rsplit('.', 1)[0])
    return models

def get_model_path(model_id):
    """
    Returns the full path to the model with given id or None if no model with
    the ID exists.
    """
    models_dir = os.path.join(
        os.path.dirname(sys.modules['chared'].__file__), 'models')
    filepath = os.path.join(models_dir, model_id + '.edm')
    if os.path.isfile(filepath):
        return filepath
    else:
        return None

def save_model(model, path):
    "Saves the model to the specified path."
    with open(path, 'w') as fp:
        pickle.dump(model, fp)

def load_model(path):
    "Loads the model from the specified path."
    with open(path, 'r') as fp:
        model = pickle.load(fp)
        return model
    return None

def union(list1, list2):
    "Returns a list of all distinct elements which occur in list1 or in list2."
    return list(set(list1).union(list2))

def scalar_product(vec1, vec2):
    "Returns a scalar product of the two vectors."
    indices = union(vec1.keys(), vec2.keys())
    result = 0
    for i in indices:
        if vec1.has_key(i) and vec2.has_key(i):
            result += vec1[i] * vec2[i]
    return result

class EncodingDetector(object):
    def __init__(self):
        self._vectors = {}
        self._encodings_order = ()
        self._version = '1.0'

    def vectorize(self, string):
        """
        Transforms the input strings into a frequency vector of contained
        characters.
        """
        vector = {}
        for ch in string:
            vector[ch] = vector.get(ch, 0) + 1.0
        return vector

    def train(self, string, encoding):
        "Trains the detector. The input must be a string and its encoding."
        self._vectors[encoding] = self.vectorize(string)

    def set_encodings_order(self, encodings):
        """
        Defines the order (importance / frequency of use) of the encodings
        the classifier has been trained on. The input must be a list or a
        tuple of encodings. The first is the most important and the last is
        the least important.
        """
        if not isinstance(encodings, (tuple, list)):
            raise TypeError
        self._encodings_order = tuple(encodings)

    def get_encoding_order(self, encoding):
        """
        Returns the order of the encoding or sys.maxint if no order is
        defined for it.
        """
        if encoding in self._encodings_order:
            return self._encodings_order.index(encoding)
        return sys.maxint

    def classify(self, string):
        """
        Returns the predicted character encoding(s) for the input string as
        a list. The list may contain more than one element if there are
        multiple equally likely candidates. In this case, the candidates are
        returned in the order of importance (see set_encodings_order). Empty
        list may be returned if there are no valid candidates. 
        """

        input_vector = self.vectorize(string)

        classification = []
        for clas in self._vectors.keys():
            #get scalar product of the vectors
            vector = self._vectors[clas]
            product = scalar_product(input_vector, vector)
            clas_info = {'clas': clas, 'product': product,
                'order': self.get_encoding_order(clas)}
            #exclude utf8 in case data is not convertible to utf8
            if 'utf_8' == clas:
                try:
                    unicode(string, 'utf_8', 'strict')
                except ValueError:
                    clas_info['product'] = 0.0
            classification.append(clas_info)

        if not classification:
            return []

        #order result classes 
        # 1.) by vector products (higher product is better)
        # 2.) by the encoding order (lower index is better)
        classification.sort(lambda x, y:
            cmp(y['product'], x['product']) or cmp(x['order'], y['order']))

        #return a list of the top classes
        # the top classes have the same score and order as the first one
        first = classification[0]
        result = []
        for clas in classification:
            if first['product'] == clas['product']:
                result.append(clas['clas'])
        return result

    def reduce_vectors(self):
        """
        Remove the common parts of all vectors. Should be called after all
        training data has been loaded. Provided the training has been performed
        on the same data for all encodings, reducing vectors increases both
        efficiency and accuracy of the classification.
        """
        #get frequencies of (character, value) pairs
        char_value_count = {}
        for vect in self._vectors.values():
            for ch, value in vect.iteritems():
                char_value_count[(ch, value)] = char_value_count.get(
                    (ch, value), 0) + 1
        #remove common parts of vectors (the (character, value) pairs with the
        #frequency equal to the number of vectors)
        encodings_count = len(self._vectors)
        for (ch, value), count in char_value_count.iteritems():
            if count >= encodings_count:
                for vect in self._vectors.values():
                    if vect.has_key(ch):
                        del vect[ch]
