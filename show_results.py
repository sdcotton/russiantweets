'''
This script takes cleaned data and displays them in interesting ways.
'''
import pandas as pd
import numpy as np
import nltk
import os
import re
import string

def show_wordcloud(words):
    '''
    generate a wordcloud from dictionary of words and their frequencies
    :param words: dictionary with keys as unique words, values as number of occurances
    :type: dict
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

def show_comparison(comparisons):
    '''
    Generates a histogram plot from a dictionary value with a two-length tuple
    for values from two datasets. Meant to plot from match_samples().
    Very simplistic output

    :param comparisons: dictionary of items to compare with tuples for relative frequency as keys
    :format: dict(str:(float,float))
    :type: dict
    '''
    assert isinstance(comparisons,dict)
    import matplotlib.pyplot as plt
    for word,value in comparisons.items():
        title=word
        plt.figure()
        ax1 = plt.subplot(121)
        ax1.title.set_text('Normal Users')
        x=word
        x_holder = [1]
        y1=value[0]
        ax1.bar(x_holder, [y1], color='#ab4435')
        bottom1, top1 = ax1.get_ylim()   # Find y1 limit
        plt.xticks(x_holder, [x])
        ax2 = plt.subplot(122)
        ax2.title.set_text('Russian Trolls')
        y2=value[1]
        ax2.bar([1], [y2], color='b')
        bottom2, top2 = ax2.get_ylim()    # Find y2 limit
        # Set y limit to highest value for both
        plt.ylim(bottom=0)
        if top2<top1:
            ax1.set_ylim(top=top1)
            ax2.set_ylim(top=top1)
        else:
            ax1.set_ylim(top=top2)
            ax2.set_ylim(top=top2)
        plt.xticks(x_holder, [x])
        plt.show()

def show_individual_comparison(comparisons, list1, list2):
    '''
    Generates a histogram plot from a dictionary value with a two-length tuple
    for values from two datasets. x axis is the individual value of list1 and list2

    :param comparisons: dict(str:(float,float))
    :type: dict
    :param list1:
    :type: list
    :param list2:
    :type: list
    '''
    assert isinstance(comparisons,dict)
    assert isinstance(list1, list) and isinstance(list2, list)
    import matplotlib.pyplot as plt
    import matplotlib as mpl
    mpl.style.use('seaborn')
    first_group_normal = {}
    second_group_normal = {}
    first_group_russian = {}
    second_group_russian = {}
    ha = {'center': 'center', 'right': 'left', 'left': 'right'}
    offset = {'center': 0, 'right': 1, 'left': -1}
    xpos = 'center'
    for word, value in comparisons.items():
        if word in list1:
            first_group_normal[word] = value[0]
            first_group_russian[word] = value[1]

        if word in list2:
            second_group_normal[word] = value[0]
            second_group_russian[word] = value[1]

    plt.figure()
    ax1 = plt.subplot(121)
    ax1.title.set_text('Normal Users')
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    x_place_holder = range(len(first_group_normal))
    rect1 = ax1.bar(x_place_holder, first_group_normal.values(), width = 0.8, color='gold', edgecolor = 'darkgoldenrod', linewidth=1.1)
    bottom1, top1 = ax1.get_ylim()   # Find y1 limit
    for rect in rect1:
        rect.set_hatch('-')
        height = rect.get_height()
        ax1.annotate('{:.2f}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(offset[xpos]*3, 3),  # use 3 points offset
                    textcoords="offset points",  # in both directions
                    ha=ha[xpos], va='bottom')
    plt.xticks(x_place_holder, first_group_normal.keys())
    plt.ylabel('percentage')

    ax2 = plt.subplot(122)
    ax2.title.set_text('Russian Trolls')
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    rect2 = ax2.bar(x_place_holder, first_group_russian.values(), width=0.8, color='seagreen', edgecolor = 'darkgreen', linewidth=1.1)
    for rect in rect2:
        rect.set_hatch('|')
        height = rect.get_height()
        ax2.annotate('{:.2f}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(offset[xpos]*3, 3),  # use 3 points offset
                    textcoords="offset points",  # in both directions
                    ha=ha[xpos], va='bottom')
    bottom2, top2 = ax2.get_ylim()    # Find y2 limit
    # Set y limit to highest value for both
    plt.ylim(bottom=0)
    if top2<top1:
        ax1.set_ylim(top=top1)
        ax2.set_ylim(top=top1)
    else:
        ax1.set_ylim(top=top2)
        ax2.set_ylim(top=top2)
    plt.xticks(x_place_holder, first_group_russian.keys())
    plt.show()

    plt.figure()
    ax3 = plt.subplot(121)
    ax3.title.set_text('Normal Users')
    ax3.spines["top"].set_visible(False)
    ax3.spines["right"].set_visible(False)
    x_place_holder = range(len(second_group_normal))
    rect3 = ax3.bar(x_place_holder, second_group_normal.values(), color='r', edgecolor = 'black', linewidth=1.8)
    bottom3, top3 = ax3.get_ylim()   # Find y1 limit
    plt.xticks(x_place_holder, second_group_normal.keys())
    for rect in rect3:
        rect.set_hatch('\\')
        height = rect.get_height()
        ax3.annotate('{:.2f}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(offset[xpos]*3, 3),  # use 3 points offset
                    textcoords="offset points",  # in both directions
                    ha=ha[xpos], va='bottom')
    plt.ylabel('percentage')

    ax4 = plt.subplot(122)
    ax4.title.set_text('Russian Trolls')
    ax4.spines["top"].set_visible(False)
    ax4.spines["right"].set_visible(False)
    rect4 = ax4.bar(x_place_holder, second_group_russian.values(), color='dodgerblue', edgecolor = 'black',linewidth=1.8)
    bottom4, top4 = ax4.get_ylim()    # Find y2 limit
    # Set y limit to highest value for both
    plt.ylim(bottom=0)
    for rect in rect4:
        rect.set_hatch('\\')
        height = rect.get_height()
        ax4.annotate('{:.2f}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(offset[xpos]*3, 3),  # use 3 points offset
                    textcoords="offset points",  # in both directions
                    ha=ha[xpos], va='bottom')
    if top4<top3:
        ax3.set_ylim(top=top3)
        ax4.set_ylim(top=top3)
    else:
        ax3.set_ylim(top=top4)
        ax4.set_ylim(top=top4)
    plt.xticks(x_place_holder, second_group_russian.keys())
    plt.show()



def show_cumulative_comparison(comparisons, list1, list2):
    '''
    Generates a histogram plot from a dictionary value with a two-length tuple
    for values from two datasets. x axis is the cumulative value of list1

    :param comparisons: output from match_samples
    :type: dict
    :param list1: list of words to compare from dataset 1, used for axes
    :type: list
    :param list2: list of words to compare from dataset 2, used for axes
    :type: list
    '''
    assert isinstance(comparisons,dict)
    assert isinstance(list1, list) and isinstance(list2, list)
    import matplotlib.pyplot as plt
    first_cumulative = [0.0, 0.0]
    second_cumulative = [0.0, 0.0]
    x_axis_print = ["Hillary Clinton", "Donald Trump"]
    ha = {'center': 'center', 'right': 'left', 'left': 'right'}
    offset = {'center': 0, 'right': 1, 'left': -1}
    xpos = 'center'
    for word, value in comparisons.items():
        if word in list1:
            first_cumulative[0] += value[0]
            first_cumulative[1] += value[1]
        elif word in list2:
            second_cumulative[0] += value[0]
            second_cumulative[1] += value[1]

    plt.figure()
    ax1 = plt.subplot(121)
    ax1.title.set_text('Normal Users')
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    x_place_holder = [1,2]
    rect1 = ax1.bar(x_place_holder, [first_cumulative[0], second_cumulative[0]], width=0.5, color='r', edgecolor = 'black', linewidth=1.8)
    bottom1, top1 = ax1.get_ylim()   # Find y1 limit
    for rect in rect1:
        rect.set_hatch('x')
        height = rect.get_height()
        ax1.annotate('{:.2f}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(offset[xpos]*3, 3),  # use 3 points offset
                    textcoords="offset points",  # in both directions
                    ha=ha[xpos], va='bottom')
    plt.ylabel('percentage')

    plt.xticks(x_place_holder,x_axis_print)
    ax2 = plt.subplot(122)
    ax2.title.set_text('Russian Trolls')
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    rect2 = ax2.bar(x_place_holder, [first_cumulative[1], second_cumulative[1]], width=0.5, color='dodgerblue', edgecolor = 'black', linewidth=1.8)
    bottom2, top2 = ax2.get_ylim()    # Find y2 limit
    for rect in rect2:
        rect.set_hatch('x')
        height = rect.get_height()
        ax2.annotate('{:.2f}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(offset[xpos]*3, 3),  # use 3 points offset
                    textcoords="offset points",  # in both directions
                    ha=ha[xpos], va='bottom')
    # Set y limit to highest value for both
    plt.ylim(bottom=0)
    if top2<top1:
        ax1.set_ylim(top=top1)
        ax2.set_ylim(top=top1)
    else:
        ax1.set_ylim(top=top2)
        ax2.set_ylim(top=top2)
    plt.xticks(x_place_holder, x_axis_print)
    plt.show()


def show_special_comparison(comparisons, list1, list2):
    '''
    Generates a histogram plot from a dictionary value with a two-length tuple
    for values from two datasets. x axis is the individual value of list1 and list2
    Used as an alternative to show_individual_comparison

    :param comparisons: output from match_samples
    :type: dict
    :param list1: list of words to compare from dataset 1, used for axes
    :type: list
    :param list2: list of words to compare from dataset 2, used for axes
    :type: list
    '''
    assert isinstance(comparisons,dict)
    assert isinstance(list1, list) and isinstance(list2, list)
    import matplotlib.pyplot as plt
    import matplotlib as mpl
    mpl.style.use('seaborn')
    first_group_normal = {}
    second_group_normal = {}
    first_group_russian = {}
    second_group_russian = {}
    ha = {'center': 'center', 'right': 'left', 'left': 'right'}
    offset = {'center': 0, 'right': 1, 'left': -1}
    xpos = 'center'
    for word, value in comparisons.items():
        if word in list1:
            first_group_normal[word] = value[0]
            first_group_russian[word] = value [1]

        if word in list2:
            second_group_normal[word] = value[0]
            second_group_russian[word] = value [1]

    plt.figure()
    ax1 = plt.subplot(121)
    ax1.title.set_text('Normal Users')
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    x_place_holder = range(len(first_group_normal))
    rect1 = ax1.bar(x_place_holder, first_group_normal.values(), width = 0.8, color='gold', edgecolor = 'darkgoldenrod', linewidth=1.1)
    bottom1, top1 = ax1.get_ylim()   # Find y1 limit
    for rect in rect1:
        rect.set_hatch('-')
        height = rect.get_height()
        ax1.annotate('{:.2f}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(offset[xpos]*3, 3),  # use 3 points offset
                    textcoords="offset points",  # in both directions
                    ha=ha[xpos], va='bottom')
    plt.xticks(x_place_holder, first_group_normal.keys())
    plt.ylabel('percentage')

    ax2 = plt.subplot(122)
    ax2.title.set_text('Russian Trolls')
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    rect2 = ax2.bar(x_place_holder, first_group_russian.values(), width=0.8, color='seagreen', edgecolor = 'darkgreen', linewidth=1.1)
    for rect in rect2:
        rect.set_hatch('|')
        height = rect.get_height()
        ax2.annotate('{:.2f}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(offset[xpos]*3, 3),  # use 3 points offset
                    textcoords="offset points",  # in both directions
                    ha=ha[xpos], va='bottom')
    bottom2, top2 = ax2.get_ylim()    # Find y2 limit
    # Set y limit to highest value for both
    plt.ylim(bottom=0)
    if top2<top1:
        ax1.set_ylim(top=top1)
        ax2.set_ylim(top=top1)
    else:
        ax1.set_ylim(top=top2)
        ax2.set_ylim(top=top2)
    plt.xticks(x_place_holder, first_group_russian.keys())
    plt.show()

    plt.figure()
    ax3 = plt.subplot(111)
    ax3.title.set_text('Trump vs Hillary')
    ax3.spines["top"].set_visible(False)
    ax3.spines["right"].set_visible(False)
    #x_place_holder = range(len(second_group_normal))
    print(second_group_normal.keys())
    x_place_holder = np.arange(len(second_group_normal))
    x_place_holder2 = [x + 0.4 for x in x_place_holder]

    rect3 = ax3.bar(x_place_holder, second_group_normal.values(), width=0.4, color='r', edgecolor = 'black', linewidth=0.1, label='Normal Users')
    rect44 = ax3.bar(x_place_holder2, second_group_russian.values(), width=0.4, color='dodgerblue', edgecolor = 'black', linewidth=0.1, label="Russian Trolls")
    bottom3, top3 = ax3.get_ylim()   # Find y1 limit
    plt.xticks(x_place_holder, second_group_normal.keys())
    for rect in rect3:
        rect.set_hatch('\\')
        height = rect.get_height()
        ax3.annotate('{:.2f}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(offset[xpos]*3, 3),  # use 3 points offset
                    textcoords="offset points",  # in both directions
                    ha=ha[xpos], va='bottom')
    for rect in rect44:
        rect.set_hatch('//')
        height = rect.get_height()
        ax3.annotate('{:.2f}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(offset[xpos]*3, 3),  # use 3 points offset
                    textcoords="offset points",  # in both directions
                    ha=ha[xpos], va='bottom')
    ax3.legend()
    plt.ylabel('percentage')
    ax4 = plt.subplot(122)
    ax4.title.set_text('Russian Trolls')
    ax4.spines["top"].set_visible(False)
    ax4.spines["right"].set_visible(False)
    rect4 = ax4.bar(x_place_holder, second_group_russian.values(), color='dodgerblue', edgecolor = 'black',linewidth=1.8)
    bottom4, top4 = ax4.get_ylim()    # Find y2 limit
    # Set y limit to highest value for both
    plt.xticks(x_place_holder, second_group_normal.keys())
    for rect in rect4:
        rect.set_hatch('\\')
        height = rect.get_height()
        ax4.annotate('{:.2f}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(offset[xpos]*3, 3),  # use 3 points offset
                    textcoords="offset points",  # in both directions
                    ha=ha[xpos], va='bottom')
    plt.ylim(bottom=0)
    if top4<top3:
        ax3.set_ylim(top=top3)
        ax4.set_ylim(top=top3)
    else:
        ax3.set_ylim(top=top4)
        ax4.set_ylim(top=top4)
    plt.xticks(x_place_holder, second_group_russian.keys())
    plt.show()

def show_histogram(words, title):
    '''
    Creates a histogram with the following characteristics
    Axes:
        :x: words
        :y: number of occurances
    :param words: Counter dictionary of words and their frequencies
    :type: dict
    :param title: graph title
    :type: str
    '''
    assert isinstance(words,dict)
    assert isinstance(title,str)
    import matplotlib.pyplot as plt
    import matplotlib as mpl
    mpl.style.use('dark_background')
    #plt.style.use(['dark_background','presentation'])
    # Create list and sort in descending order
    tups=list(words.items())
    tups.sort(key=lambda tup: tup[1],reverse=True)  # sort by values
    m=list(map(list,zip(*tups)))  # Unzip tuples into 2 lists
    x=m[0]
    y=m[1]
    x_holder = range(len(x))
    plt.bar(x_holder, y, color='gold')
    plt.xticks(x_holder, x)
    plt.xticks(rotation=90)
    plt.title(title)
    plt.ylabel('Frequency (%)')
    plt.show()


def show_results():
    '''
    Main function: this function will run all of the above functions. Originally
    named "main()" but it could be confused with other scripts' main functions
    '''
    # Import other scripts' functions
    from clean_data import clean_data
    from process_data import match_error, match_samples
    # Clean data
    trollWords = clean_data(sample_size=300, path='tweets.csv')
    normalWords = clean_data(sample_size=300, path='election_day_tweets.csv')
    # Analyze
    matched = match_error(normalWords, trollWords, ['vote'])
    comparison_words=['vote', 'trump', 'hillary', 'hillari', 'clinton', 'donald','amp']
    comparisons=match_samples(normalWords, trollWords, comparison_words)
    # Display results
    show_comparison(comparisons)
    list1 = ['hillari', 'clinton', 'hillary']
    list2 = ['donald', 'trump']
    show_cumulative_comparison(comparisons, list1, list2)
    list1 = ['hillari', 'hillary']
    list2 = ['hillari',  'hillary','clinton','donald','trump']
    show_special_comparison(comparisons, list1, list2)
    show_wordcloud(words = words)
    show_histogram(trollWords,title='Russian Twitter Troll Word Frequency')
    show_histogram(normalWords,title='User Political Tweet Word Frequency')
    show_histogram(matched,title='Word Comparison')

if __name__=='__main__':
    show_results()
