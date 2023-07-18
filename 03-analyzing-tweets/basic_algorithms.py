"""
CS 121: Analyzing Election Tweets

Gabriela Ayala

Basic algorithms module

Algorithms for efficiently counting and sorting distinct 'entities',
or unique values, are widely used in data analysis.
"""

import math
from util import sort_count_pairs

# Task 1.1

def count_tokens(tokens):
    '''
    Counts each distinct token (entity) in a list of tokens.

    Inputs:
        tokens: list of tokens (must be immutable)

    Returns: dictionary that maps tokens to counts
    '''

    dictionary = {}

    for val in tokens:
        if val in dictionary:
            dictionary[val] += 1
        else:
            dictionary[val] = 1

    return dictionary


# Task 1.2
def find_top_k(tokens, k):
    '''
    Find the k most frequently occuring tokens.

    Inputs:
        tokens: list of tokens (must be immutable)
        k: a non-negative integer

    Returns: list of the top k tokens ordered by count.
    '''

    #Error checking (DO NOT MODIFY)
    if k < 0:
        raise ValueError("In find_top_k, k must be a non-negative integer")

    freq = count_tokens(tokens)
    token_count_lst = []

    for token, count in freq.items():
        token_count_lst.append((token, count))
    
    token_count_lst = sort_count_pairs(token_count_lst)

    token_lst = []
    for i, (token, count) in enumerate(token_count_lst):
        token_lst.append(token)

    top_k_lst = token_lst[:k]

    return top_k_lst


# Task 1.3
def find_min_count(tokens, min_count):
    '''
    Find the tokens that occur *at least* min_count times.

    Inputs:
        tokens: a list of tokens  (must be immutable)
        min_count: a non-negative integer

    Returns: set of tokens
    '''

    #Error checking (DO NOT MODIFY)
    if min_count < 0:
        raise ValueError("min_count must be a non-negative integer")

    freq = count_tokens(tokens)
    set_min_count = set()

    for token, count in freq.items():
        if count >= min_count:
            set_min_count.add(token)

    return set_min_count


# Task 1.4

def find_max_count(document):
    '''
    Find the maximum number of times that any token
    appears in a document.

    Inputs:
        document: a list of tokens  (must be immutable)

    Returns (int): the maximum number of times any token
    appears in the document.
    '''

    freq = count_tokens(document)
    max_count_tokens = max(freq.values())
    
    return max_count_tokens

def count_term_in_document (term, document):
    '''
    Compute the frequency of a term in a document.

    Inputs:
        document: a list of tokens  (must be immutable)
        term (str): the term

    Returns (int): the frequency of the given term in the
    document.
    '''
    
    count_term_in_doc = 0

    for value in document:
        if value == term:
            count_term_in_doc += 1

    return count_term_in_doc

def augmented_term_frequency(term, document):
    '''
    Calculates the augment term frequency (tf) for a given
    term in a given document.

    Inputs:
        document: a list of tokens  (must be immutable)
        term (str): the term

    Returns (float): the augmented term frequency (tf).
    '''

    count_term_in_doc = count_term_in_document (term, document)
    max_count_in_doc = find_max_count(document)
    
    augmented_term_freq = 0.5 + 0.5 * (count_term_in_doc/max_count_in_doc)

    return augmented_term_freq

def inverse_document_frequency(docs, term):
    '''
    Computes the inverse document frequency (idf) for a 
    given term in a document collection.

    Inputs:
        docs: list of list of tokens, the document 
        collection.

    Returns (int): the maximum number of times any token
    appears in the document.
    '''

    # Allocate space to count the number of documents in 
    # the document collection.
    document_count = 0
    for idx, _ in enumerate(docs):
        document_count += 1
    
    # Allocate space to count the number of documents where
    # the term appears.
    number_docs_with_term = 0

    for document in docs:
        count_term_in_doc = count_term_in_document(term, document)
        if count_term_in_doc > 0:
            number_docs_with_term += 1

    inverse_doc_freq = math.log(document_count/number_docs_with_term)

    return inverse_doc_freq


def find_salient(docs, threshold):
    '''
    Compute the salient words for each document.  A word is salient if
    its tf-idf score is strictly above a given threshold.

    Inputs:
      docs: list of list of tokens
      threshold: float

    Returns: list of sets of salient words
    '''
    lst_salient = []

    for document in docs:
        salient_words = set()
        
        for term in document:
            tf = augmented_term_frequency(term, document)
            idf = inverse_document_frequency(docs, term)
            tf_idf_score = tf * idf
            
            if tf_idf_score > threshold:
                salient_words.add(term)
        lst_salient.append(salient_words)
    
    return lst_salient

    