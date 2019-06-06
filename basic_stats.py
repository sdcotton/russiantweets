# -*- coding: utf-8 -*-
"""
Created on Thu May 23 12:02:03 2019

Testing script for developers
@author: hyifan
"""

import pandas as pd
import numpy as np
import nltk
import os
import re
import string



corpus2.loc[corpus2.retweets == 0, 'retweeted'] = 0
corpus2.loc[corpus2.retweets != 0, 'retweeted'] = 1
corpus3 = corpus2[corpus2.retweets != 0]
corpus3['lg_rt'] = np.log(corpus3.retweets)
ax = corpus3.lg_rt.plot.kde()



if __name__=='__main__':
