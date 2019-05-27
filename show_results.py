import pandas as pd
import numpy as np
import nltk
import os
import re
import string

def show_wordcloud(words):
    '''
    generate a wordcloud from corpus tokens.
    '''
    assert isinstance(words,dict)

    from wordcloud import WordCloud
    from collections import Counter
    import matplotlib.pyplot as plt

    wordcloud = WordCloud(
        width = 1500,
        height = 1000,
        background_color = 'black').generate_from_frequencies(words)

    fig = plt.figure(
        figsize = (8, 6),
        facecolor = 'k',
        edgecolor = 'k')

    plt.imshow(wordcloud, interpolation = 'bilinear')
    plt.axis('off')
    plt.tight_layout(pad=0)
    plt.show()

def show_histogram(words_dict):
    '''
    :param words: Counter dictionary of words and their frequencies
    :type: dict

    Creates a histogram with the following characteristics
    Axes
    :x: words
    :y: number of occurances
    '''
    # SETUP #
    assert isinstance(words_dict,dict)
    import matplotlib.pyplot as plt

    # Create list and sort in descending order
    tups=list(words_dict.items())
    tups.sort(key=lambda tup: tup[1],reverse=True)  # sort by values
    m=list(map(list,zip(*tups)))  # Unzip tuples into 2 lists
    x=m[0]
    y=m[1]
    plt.bar(x, y, color='#ab4435')
    plt.xticks(rotation=90)
    plt.title('Russian Twitter Bot Word Frequency')
    plt.ylabel('Frequency (%)')
    plt.show()

def show_histograms(words, title):
    assert isinstance(words,dict)
    assert isinstance(title,str)
    import matplotlib.pyplot as plt

    # Create list and sort in descending order
    tups=list(words.items())
    tups.sort(key=lambda tup: tup[1],reverse=True)  # sort by values
    m=list(map(list,zip(*tups)))  # Unzip tuples into 2 lists
    x=m[0]
    y=m[1]
    plt.bar(x, y, color='#ab4435')
    plt.xticks(rotation=90)
    plt.title(title)
    plt.ylabel('Frequency (%)')
    plt.show()

def show_results():
    from clean_data import clean_data
    from process_data import match_error
    trollWords = clean_data(sample_size=30000, path='tweets.csv')
    normalWords = clean_data(sample_size=30000, path='election_day_tweets.csv')
    matched = match_error(normalWords, trollWords, ['vote', 'trump', 'hillari', 'hillary', 'clinton', 'amp'])
    print(matched)
    #show_wordcloud(words = words)
    show_histograms(trollWords,title='Russian Twitter Bot Word Frequency')
    show_histograms(normalWords,title='User Political Tweet Word Frequency')
if __name__=='__main__':
    show_results()
