import pandas as pd
import numpy as np
import nltk
import os
import re
import string

def settingenv():
    ''' download nltk packages '''
    if not nltk.data.find('corpora/stopwords'):
        nltk.download('stopwords')
    # I wasn't able to download the word_tokenize, don't know pat
    nltk.download('word_tokenize')
    if not nltk.data.find('tokenizers/punkt'):
        nltk.download('punkt')

def tweets(path = "tweets.csv"):
    '''import tweets csv into a pandas dataframe'''
    tweets = pd.read_csv("tweets.csv")
    return tweets

def sampling(tweets_df, a = 1, b = 20):
    '''
    slice a sample from the original tweets
    tweets: tweets data frame
    a, b: range of sampling
    returns a corpus data frame.
    '''
    sample = tweets_df.loc[a:b,]
    corpus = sample.loc[:,['text']]
    corpus['text_index'] = corpus.index
    corpus.text = corpus.text.astype(str)

    return corpus

def tokenize(insent):
    '''
    input sentence, returns a list of words
    '''
    from nltk.tokenize import word_tokenize
    #tokenlist = word_tokenize(insent)
    tokenlist = insent.split()
    return tokenlist

def stemming(inlist):
    '''
    input a list, returns a list of stemmed words
    '''
    outlist = []
    stemmer = nltk.SnowballStemmer('english')
    for word in inlist:
        outlist.append(stemmer.stem(word))
    return outlist

def remove_stopwords(inlist):
    '''
    input list of words, returns list of words w/o stopwords
    e.g.: the, a, here, we
    '''
    from nltk.corpus import stopwords
    stop_words = set(stopwords.words("english"))
    outlist = []
    for word in inlist:
        if word not in stop_words:
            outlist.append(word)
    return outlist

def remove_punkt(inlist, exemption = ['@', '#']):
    '''
    input list of words, returns list of words w/o punctuation
    by default, @ and # are not removed since they are important features of tweets
    '''
    import string
    #outlist = [word for word in inlist if not re.fullmatch('[' + string.punctuation + ']+', word)]
    punktlist = string.punctuation
    for e in exemption:
        punktlist = punktlist.replace(e, '')
    outlist = []
    for word in inlist:
        word = word.translate(str.maketrans('','', punktlist))
        outlist.append(word)
    return outlist

def remove_regex(inlist, pattern = "@[\w]*"):
    '''
    use regular expression to remove words in text.
    removes @ someone by default.
    inlist: a list of words
    pattern: a list of re pattern
    '''
    regex = re.compile(pattern)
    filtered_list = [x for x in inlist if not regex.match(x)]
    return filtered_list

def create_wordcount(corpus):
    wordlist = list([a for b in corpus.tokens.tolist()for a in b])
    from collections import Counter
    c = dict(Counter(wordlist))
    # Remove spaces/invalid characters
    c.pop('')
    # Remove words that only appear relatively few times
    l=len(c.keys()) # Relative frequency instead of total count
    word_count={k:v*100/l for k, v in c.items() if v > l/100}
    return word_count

def clean_data(sample_size):

    settingenv()

    tweets_df = tweets()

    corpus = sampling(b=sample_size, tweets_df=tweets_df)

    corpus['tokens'] = corpus['text'].apply(tokenize)

    corpus['tokens'] = corpus['tokens'].apply(stemming)

    corpus['tokens'] = corpus['tokens'].apply(remove_stopwords)

    corpus['tokens'] = corpus['tokens'].apply(remove_punkt)

    #remove all @someone
    corpus['tokens'] = corpus['tokens'].apply(remove_regex)

    # remove all python links
    corpus['tokens'] = corpus['tokens'].apply(remove_regex, pattern = "https*")

    # remove all hashtags
    corpus['tokens'] = corpus['tokens'].apply(remove_regex, pattern = "#[\w]*")

    # remove all retweets
    corpus['tokens'] = corpus['tokens'].apply(remove_regex, pattern = "rt")

    # create word count
    words=create_wordcount(corpus)
    return words

if __name__=='__main__':
    words=clean_data(sample_size=200)
    print(words)
