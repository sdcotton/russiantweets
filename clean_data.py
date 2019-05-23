import pandas as pd
import numpy as np
import nltk
import os
import re
import string

def settingenv():
    nltk.download('stopwords')
    nltk.download('word_tokenize')
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


#note: the following function is extremely slow. Havn't figure out why.

def show_wordcloud(corpus):
    '''
    generate a wordcloud from corpus tokens.
    '''
    from wordcloud import WordCloud
    import matplotlib.pyplot as plt

    wordlist = list([a for b in corpus.tokens.tolist()for a in b])
    from collections import Counter
    c = dict(Counter(wordlist))

    wordcloud = WordCloud(
        width = 3000,
        height = 2000,
        background_color = 'black').generate_from_frequencies(c)

    fig = plt.figure(
        figsize = (40, 30),
        facecolor = 'k',
        edgecolor = 'k')

    plt.imshow(wordcloud, interpolation = 'bilinear')
    plt.axis('off')
    plt.tight_layout(pad=0)
    plt.show()

if __name__=='__main__':
    settingenv()

    tweets_df = tweets()

    corpus = sampling(b = 200, tweets_df=tweets_df)

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


    #understanding what's left in the data:
    show_wordcloud(corpus = corpus)
