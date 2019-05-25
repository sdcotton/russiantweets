import pandas as pd
import nltk
import re
import string

def settingenv():
    ''' download nltk packages '''
    if not nltk.data.find('corpora/stopwords'):
        nltk.download('stopwords')
    # I wasn't able to download the word_tokenize, don't know pat
#    nltk.download('word_tokenize')
    if not nltk.data.find('tokenizers/punkt'):
        nltk.download('punkt')

def tweets(path = "tweets.csv"):
    '''import tweets csv into a pandas dataframe'''
    tweets = pd.read_csv(path)
    return tweets

def sampling(tweets_df, count=20):
    '''
    slice a sample from the original tweets
    tweets: tweets data frame
    a, b: range of sampling
    returns a corpus data frame.
    '''
    if count <= 0:
        sample = tweets_df
    else:
        sample = tweets_df.sample(n=count)
    corpus = sample.loc[:,['text']]
    corpus['text_index'] = corpus.index
    corpus.text = corpus.text.astype(str)

    return corpus

def tokenize(insent):
    '''
    input sentence, returns a list of words
    '''
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
    wordlist = list([a for b in corpus.tokens.tolist() for a in b])
    from collections import Counter
    counter = Counter(wordlist)
    c = dict(counter)
    # Remove spaces/invalid characters
    c.pop('')
    # Remove words that only appear relatively few times
    l=sum(c.values()) # Relative frequency instead of total count
    # Words that should stay in graph, regardless of freq. Needed to keep 'hillary'
    important_words=['hillary','clinton','donald','trump','obama','USA','vote',
    'elect','president','democrat','republican','democrats','republicans',
    'crooked','emails']
    most_common = dict(counter.most_common(30)).keys()
    word_count={k:v*100/l for k, v in c.items() if v > l/50 or k in important_words or k in most_common}
    #import code; code.interact(local=locals()) #DEBUG
    return word_count

def clean_data(sample_size, path = "tweets.csv"):

    print('setting up environment...')
    settingenv()
    print('set up environment')
    
    print('loading tweets from file...')
    tweets_df = tweets(path)
    print('loaded tweets from file')
    
    print('selecting sample of tweets...')
    corpus = sampling(count=sample_size, tweets_df=tweets_df)
    print('selected sample of tweets')
    
    print('tokenizing tweets...')
    corpus['tokens'] = corpus['text'].apply(tokenize)
    print('tokenized tweets')

    print('stemming tweets...')
    corpus['tokens'] = corpus['tokens'].apply(stemming)
    print('stemmed tweets')

    print('removing stopwords...')
    corpus['tokens'] = corpus['tokens'].apply(remove_stopwords)
    print('removed stopwords')

    print('removing puncutation...')
    corpus['tokens'] = corpus['tokens'].apply(remove_punkt)
    print('removed punctuation')

    #remove all @someone
    print('removing @someones...')
    corpus['tokens'] = corpus['tokens'].apply(remove_regex)
    print('removed @someones')

    # remove all python links
    print('removing links...')
    corpus['tokens'] = corpus['tokens'].apply(remove_regex, pattern = "https*")
    print('removed links')

    # remove all hashtags
    print('removing hashtags...')
    corpus['tokens'] = corpus['tokens'].apply(remove_regex, pattern = "#[\w]*")
    print('removed hashtags')

    # remove all retweets
    print('removing retweets')
    corpus['tokens'] = corpus['tokens'].apply(remove_regex, pattern = "rt")
    print('removed retweets')

    # create word count
    print('generating word count...')
    words=create_wordcount(corpus)
    print('generated word count')

    return words

if __name__=='__main__':
    words=clean_data(sample_size=200)
    print(words)
