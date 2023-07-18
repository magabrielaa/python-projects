"""
Analyzing Election Tweets

Gabriela Ayala 

Analyze module

Functions to analyze tweets. 
"""

import unicodedata
import sys

from basic_algorithms import find_top_k, find_min_count, find_salient

##################### DO NOT MODIFY THIS CODE #####################

def keep_chr(ch):
    '''
    Find all characters that are classifed as punctuation in Unicode
    (except #, @, &) and combine them into a single string.
    '''
    return unicodedata.category(ch).startswith('P') and \
        (ch not in ("#", "@", "&"))

PUNCTUATION = " ".join([chr(i) for i in range(sys.maxunicode)
                        if keep_chr(chr(i))])

# When processing tweets, ignore these words
STOP_WORDS = ["a", "an", "the", "this", "that", "of", "for", "or",
              "and", "on", "to", "be", "if", "we", "you", "in", "is",
              "at", "it", "rt", "mt", "with"]

# When processing tweets, words w/ a prefix that appears in this list
# should be ignored.
STOP_PREFIXES = ("@", "#", "http", "&amp")


#####################  MODIFY THIS CODE #####################


############## Part 2 ##############

# Task 2.1
    
def find_entities_subkeys(tweets, entity_desc):
    """
    Creates a list of the subkey of interest values from 
    the entities list and  converts text to lower case only 
    if the variable is not case sensitive.

    Inputs:
        tweets: a list of tweets
        entity_desc: a triple such as ("hashtags", "text", True),
          ("user_mentions", "screen_name", False), etc.
        k: integer

    Returns: list of subkey values.
    """
    key_of_interest, subkey_of_interest, boolean = entity_desc
    subkey_val_lst = []

    for tweet in tweets:
        key_lst = tweet["entities"][key_of_interest]
           
        for dictionary in key_lst:
            # If the boolean is False (the variable is not case-sensitive), 
            # the text is changed to lower case.
            if not boolean:
                subkey_value = dictionary[subkey_of_interest].lower()
            # If the boolean is True (the variable is case-sensitive),
            # the text remains the same.
            else:
                subkey_value = dictionary[subkey_of_interest]
            subkey_val_lst.append(subkey_value)
    
    return subkey_val_lst

def find_top_k_entities(tweets, entity_desc, k):
    """
    Find the k most frequently occuring entitites.

    Inputs:
        tweets: a list of tweets
        entity_desc: a triple such as ("hashtags", "text", True),
          ("user_mentions", "screen_name", False), etc.
        k: integer

    Returns: list of entities
    """
    key_of_interest, subkey_of_interest, boolean = entity_desc
    subkey_val_lst = find_entities_subkeys(tweets, entity_desc)

    top_entities = find_top_k(subkey_val_lst, k)

    return top_entities

# Task 2.2
def find_min_count_entities(tweets, entity_desc, min_count):
    """
    Find the entitites that occur at least min_count times.

    Inputs:
        tweets: a list of tweets
        entity_desc: a triple such as ("hashtags", "text", True),
          ("user_mentions", "screen_name", False), etc.
        min_count: integer

    Returns: set of entities
    """
    key_of_interest, subkey_of_interest, boolean = entity_desc
    subkey_val_lst = find_entities_subkeys(tweets, entity_desc)

    min_count_of_entities = find_min_count(subkey_val_lst, min_count)

    return min_count_of_entities
    

############## Part 3 ##############

# Pre-processing step and representing n-grams

def pre_process(tweets, case_sensitive, remove_stop_words):
    """
    Pre-processes the text of a list of tweets.

    Inputs:
        tweets: a list of tweets
        case_sensitive: boolean
        remove_stop_words: boolean

    Returns: list of processed text
    """

    cleaned_tweets = []
    
    for tweet in tweets:
        abridged_text = tweet["abridged_text"]
        # Turn abridged text into a list of words.
        words = abridged_text.split()
        
        processed_tweet = []
        for word in words:
            # Remove leading and trailing punctuation from each 
            # word.
            word = word.strip(PUNCTUATION)
            # Remove words where stripping punctuation leads to empty 
            # string.
            if word == "":
                continue
            # For tasks that are not case sensitive, convert word to
            # lower case.
            if not case_sensitive:
                word = word.lower()
            # Eliminate stop words for tasks that require it.
            if remove_stop_words:
                if word in STOP_WORDS:
                    continue
            # Remove words that begin with URLs, hashtags and mentions. 
            if word.startswith(STOP_PREFIXES):
                continue

            processed_tweet.append(word)
        cleaned_tweets.append(processed_tweet)

    return cleaned_tweets

def create_n_grams(tweets, n):
    """
    Create n-grams from a list of processed tweets.

    Inputs:
        tweets: a list of tweets
        n = the number of n_grams 

    Returns: list of lists of n_gram tuples
    """
    tweets_ngrams = []

    for tweet in tweets:
        tweet_ngrams = []
        for i in range(len(tweet) - (n - 1)):
            n_grams = tuple(tweet[i:i + n])
            tweet_ngrams.append(n_grams)
        tweets_ngrams.append(tweet_ngrams)

    return tweets_ngrams

def tweets_n_grams(tweets, case_sensitive, remove_stop_words, n):
    """
    Generate n_grams for a list of tweets.

    Inputs:
        tweets: a list of tweets
        case_sensitive: boolean
        remove_stop_words: boolean
        n = integer

    Returns: list of lists of tweets' n_grams
    """
    
    cleaned_tweets = pre_process(tweets, case_sensitive,
                                    remove_stop_words)
    tweets_n_grams = create_n_grams(cleaned_tweets, n)

    return tweets_n_grams


# Task 3.1
def find_top_k_ngrams(tweets, n, case_sensitive, k):
    '''
    Find k most frequently occurring n_grams.

    Inputs:
        tweets: a list of tweets
        n: integer
        case_sensitive: boolean
        k: integer

    Returns: list of top k n_grams
    '''

    tweets_ngrams = tweets_n_grams(tweets,case_sensitive, True, n)

    # Allocate space for a concatenated list of all the n_grams in
    # a list of tweets.
    concatenated_tw_ngrams = []
    for tweet_ngrams in tweets_ngrams:
        for n_gram in tweet_ngrams:
            concatenated_tw_ngrams.append(n_gram)

    # Find the top k occuring ngrams in a list of tweets.
    top_k_grams = find_top_k(concatenated_tw_ngrams, k)

    return top_k_grams


# Task 3.2
def find_min_count_ngrams(tweets, n, case_sensitive, min_count):
    '''
    Find n-grams that occur at least min_count times.

    Inputs:
        tweets: a list of tweets
        n: integer
        case_sensitive: boolean
        min_count: integer

    Returns: set of n-grams
    '''
    tweets_ngrams = tweets_n_grams(tweets,case_sensitive, True, n)

    # Allocate space for a concatenated list of all the n_grams in
    # a list of tweets.
    concatenated_tw_ngrams = []
    for tweet_ngrams in tweets_ngrams:
        for n_gram in tweet_ngrams:
            concatenated_tw_ngrams.append(n_gram)

    # Find n_grams that appear a minimum amount of times in a list 
    # of tweets.
    min_count_ngrams = find_min_count(concatenated_tw_ngrams, min_count)

    return min_count_ngrams


# Task 3.3
def find_salient_ngrams(tweets, n, case_sensitive, threshold):
    '''
    Find the salient n_grams for each tweet.

    Inputs:
        tweets: a list of tweets
        n: integer
        case_sensitive: boolean
        threshold: float

    Returns: list of sets of strings
    '''
    tweets_ngrams = tweets_n_grams(tweets,case_sensitive, False, n)

    # Find salient n_grams for each tweet in a list of tweets.
    salient_ngrams = find_salient(tweets_ngrams, threshold)

    return salient_ngrams



