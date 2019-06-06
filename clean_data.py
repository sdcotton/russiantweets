'''
This script retrieves tweets from a csv file and cleans the data into useable form
'''
import pandas as pd
import nltk
import re
import string

def settingenv():
    ''' download packages required by nltk '''
    if not nltk.data.find('corpora/stopwords'):
        nltk.download('stopwords')
    if not nltk.data.find('tokenizers/punkt'):
        nltk.download('punkt')

def tweets(path = "tweets.csv"):
    '''
    import tweets csv file into a pandas dataframe

    :param path: system path to tweets csv file, format "filename.csv"
    :type: string
    :returns: dataframe
    '''
    import pandas as pd
    assert isinstance(path,str)
    tweets = pd.read_csv(path)
    return tweets

def sampling(tweets_df, count=20):
    '''
    slice a sample from the original tweets. Useful for testing small batches.

    :param tweets: tweets data frame
    :type: dataframe
    :param count: range of sampling
    :type: int
    returns a corpus data frame.
    '''
    import pandas as pd
    assert isinstance(tweets_df, pd.DataFrame)
    assert isinstance(count,int)
    # Use whole dataframe if sample not provided or "invalid"
    if count <= 0 or count is None:
        sample = tweets_df
    else:
        sample = tweets_df.sample(n=count)
    corpus = sample.loc[:,['text']]
    corpus['text_index'] = corpus.index
    corpus.text = corpus.text.astype(str)

    return corpus

def tokenize(insent):
    '''
    input sentence as a string, returns a list of words

    :param insent: input sentence
    :type: str
    :returns: list of words
    :example: "walk the dog" returns [walk,the,dog]
    '''
    tokenlist = insent.split()
    return tokenlist

def stemming(inlist):
    '''
    Takes words and returns the stem of those words.

    :param inlist: input list
    :type: list
    :returns: list of stemmed words
    :example: "running" and "runs" both return the stem "run"
    '''
    assert isinstance(inlist,list)
    outlist = []
    stemmer = nltk.SnowballStemmer('english')
    for word in inlist:
        outlist.append(stemmer.stem(word))
    return outlist

def remove_stopwords(inlist):
    '''
    input list of words, returns list of words w/o stopwords. these words are
    very common and not contribute anything to analysis. this function focuses
    the analysis on the words that matter.

    :stopwords: {‘ourselves’, ‘hers’, ‘between’, ‘yourself’, ‘but’, ‘again’,
    ‘there’, ‘about’, ‘once’, ‘during’, ‘out’, ‘very’, ‘having’, ‘with’, ‘they’,
    ‘own’, ‘an’, ‘be’, ‘some’, ‘for’, ‘do’, ‘its’, ‘yours’, ‘such’, ‘into’,
    ‘of’, ‘most’, ‘itself’, ‘other’, ‘off’, ‘is’, ‘s’, ‘am’, ‘or’, ‘who’, ‘as’,
    ‘from’, ‘him’, ‘each’, ‘the’, ‘themselves’, ‘until’, ‘below’, ‘are’, ‘we’,
    ‘these’, ‘your’, ‘his’, ‘through’, ‘don’, ‘nor’, ‘me’, ‘were’, ‘her’, ‘more’,
    ‘himself’, ‘this’, ‘down’, ‘should’, ‘our’, ‘their’, ‘while’, ‘above’,
    ‘both’, ‘up’, ‘to’, ‘ours’, ‘had’, ‘she’, ‘all’, ‘no’, ‘when’, ‘at’, ‘any’,
    ‘before’, ‘them’, ‘same’, ‘and’, ‘been’, ‘have’, ‘in’, ‘will’, ‘on’, ‘does’,
    ‘yourselves’, ‘then’, ‘that’, ‘because’, ‘what’, ‘over’, ‘why’, ‘so’, ‘can’,
    ‘did’, ‘not’, ‘now’, ‘under’, ‘he’, ‘you’, ‘herself’, ‘has’, ‘just’,
    ‘where’, ‘too’, ‘only’, ‘myself’, ‘which’, ‘those’, ‘i’, ‘after’, ‘few’,
    ‘whom’, ‘t’, ‘being’, ‘if’, ‘theirs’, ‘my’, ‘against’, ‘a’, ‘by’, ‘doing’,
    ‘it’, ‘how’, ‘further’, ‘was’, ‘here’, ‘than’}

    :param inlist: list of words
    :type: list
    :returns: list of words without stopwords
    :example: [walk,the,dog] returns [walk,dog]
    '''
    from nltk.corpus import stopwords
    assert isinstance(inlist,list)
    stop_words = set(stopwords.words("english"))
    outlist = []
    for word in inlist:
        if word not in stop_words:
            outlist.append(word)
    return outlist

def remove_punkt(inlist, exemption = ['@', '#']):
    '''
    input list of words, returns list of words w/o punctuation. By default,
    @ and # are not removed since they are important features of tweets so
    they have been added as an exemption with the exemption list variable

    :param inlist: list of words
    :type: list
    :param exemption: additional characters to remove
    :type: list of str
    :returns: list of words without stopwords
    '''
    assert all(isinstance(var,list) for var in [inlist,exemption])
    assert all(isinstance(char,str) for char in exemption)

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

    :param inlist: list of words
    :type: list
    :param pattern: regular expression pattern to remove
    :type: str
    :returns: list
    :example: [@realDonaldTrump,make,america,great] returns [make,america,great]
    '''
    import re
    assert isinstance(inlist,list)
    assert isinstance(pattern,str)

    regex = re.compile(pattern)
    filtered_list = [x for x in inlist if not regex.match(x)]
    return filtered_list

def create_wordcount(corpus):
    '''
    creates Counter dictionary with keys as each unique word and values as number
    of occurances in tweets DataFrame corpus

    :param corpus: tweets dataframe, should be cleaned already for important words
    :type: DataFrame
    :returns: Counter dict
    :example: output {'walk':100,'dog':20,'cat':10,'lizard':70}
    '''
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
    return word_count

def clean_data(sample_size, path = "tweets.csv"):
    '''
    Main function to clean data. Uses all above functions to clean the tweets
    csv file for only meaningful words and returns a dictionary with unique
    words and the number of times they appear in the selection of tweets

    :param sample_size: number of tweets to analyze
    :type: int
    :param path: system path to tweets csv file
    :type: str
    :returns: Counter dict
    '''
    assert isinstance(sample_size,int)
    assert isinstance(path,str)
    assert sample_size>0 or sample_size is None

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
    '''Run clean_data if called, default sample size is 200 for quick testing'''
    words=clean_data(sample_size=200)
    print(words)
