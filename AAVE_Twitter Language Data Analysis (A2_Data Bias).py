#!/usr/bin/env python
# coding: utf-8

# # AAVE On Twitter: Exploring Language Data Bias (via Perspective API Tool)

# Below I analyze how Google's Perspective API tool detects and categorizes Black language data, also known as AAVE (African-American Vernacular English), from Twitter. My goal is to ascertain whether or not the Perspective API tool will flag AAVE as being toxic. I will also attempt to verify if it does so at a frequency level higher than with other types of language data (i.e. expletives, racial slurs, etc.). Since there is some precedence for this done in previous studies, it is my hypothesis that the language of Black culture will be marked biasedly as offensive language and cumulatively given a higher than or similar rating of toxicity as other linguistic obscenities.

# **References**
# 
# • The Risk of Racial Bias in Hate Speech Detection: https://homes.cs.washington.edu/~msap/pdfs/sap2019risk.pdf 
# 
# • Racial Bias in Hate Speech and Abusive Language Detection Datasets: https://arxiv.org/pdf/1905.12516.pdf

# In[194]:

import pandas as pd
import time

df = pd.read_csv('labeled_and_scored_comments.csv')

# # Exploring The Dataset

# In[195]:

#where the data begins
df.head()

# In[196]:

#where the data ends
df.tail()

# I use the sort_values() function to organize the scores:

# In[197]:

df.sort_values(['score'])

# I use the len() function to find out the length of the data set:

# In[198]:

print(len(df))

# I also find out the the data frame type by using the type() function:

# In[199]:

print(type(df))

# Using the describe() function, I take a look at the potential quantitative characteristics present in the data:

# In[200]:

df.describe()

# Checking for the presence of any null values that might effect the accuracy of the results:

# In[201]:

df.isnull().sum() #there are no null values

# # Setting Up A Perspective API KEY

# In[202]:

from googleapiclient.discovery import build
import json
    
def get_toxicity_score(comment):
    
  API_KEY = '' #place your assigned API key here
    
  client = build(
  "commentanalyzer",
  "v1alpha1",
  developerKey=API_KEY,
  discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
  static_discovery=False,
  )

  analyze_request = {
  'comment': { 'text': comment },
  'requestedAttributes': {'TOXICITY': {}}
  }
    
  response = client.comments().analyze(body=analyze_request).execute()
  toxicity_score = response["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
    
  return toxicity_score

# # Testing For Language Bias 

# To explore the Twitter data set for linguistic bias, I tested ten AAVE phrases commonly used in the Black community:

# In[203]:

get_toxicity_score('Nigga, please!')

# In[204]:

get_toxicity_score('The devil is a liar!')

# In[205]:

get_toxicity_score('Damn straight')

# In[206]:

get_toxicity_score('You a lie from hell!')

# In[207]:

get_toxicity_score('And yo mama said you ugly')

# In[208]:

get_toxicity_score('You so tender-headed')

# In[209]:

get_toxicity_score('You so nappy-headed')

# In[210]:

get_toxicity_score("Booboo da fool")

# In[211]:

get_toxicity_score('What a bobohead')

# In[212]:

get_toxicity_score("Imma whoop yo ass")


# # Making A Comparison (Visual Inspection Results)

# Compared to other similar phrases conveying similar sentiments, AAVE is flagged as having a higher level of toxicity: 

# In[213]:

comment_list = ['Man, please!', 'Girl, please!', 'Nigga, please!']

for comment in comment_list:
    score = get_toxicity_score(comment)
    print(comment, score)
    time.sleep(1)

# In[214]:

comment_list = ['The devil lies', "The devil's a lie!", 'The devil is a liar!']

for comment in comment_list:
    score = get_toxicity_score(comment)
    print(comment, score)
    time.sleep(1)

# In[215]:

comment_list = ['Dang, straight!', 'Doggone, straight!', 'Damn straight!']

for comment in comment_list:
    score = get_toxicity_score(comment)
    print(comment, score)
    time.sleep(1)

# In[216]:

comment_list = ['You lie!', "You're lying!", 'You a lie from hell!']

for comment in comment_list:
    score = get_toxicity_score(comment)
    print(comment, score)
    time.sleep(1)

# In[217]:

comment_list = ["Your mom said that you're unloveable.", "Your mother calls you a plain Jane.", 'Yo mama said you ugly']

for comment in comment_list:
    score = get_toxicity_score(comment)
    print(comment, score)
    time.sleep(1)

# In[218]:

comment_list = ["You are so delicate", "You're so sensitive", 'You so tender-headed']

for comment in comment_list:
    score = get_toxicity_score(comment)
    print(comment, score)
    time.sleep(1)

# In[219]:

comment_list = ['Your hair is so curly', "You are so curly-haired", 'You so nappy-headed']

for comment in comment_list:
    score = get_toxicity_score(comment)
    print(comment, score)
    time.sleep(1)

# In[220]:

comment_list = ['Booboo', 'Booboo the fool', 'Booboo da fool']

for comment in comment_list:
    score = get_toxicity_score(comment)
    print(comment, score)
    time.sleep(1)

# In[221]:

comment_list = ['What a dummy', 'What a clown', 'What a bobohead']

for comment in comment_list:
    score = get_toxicity_score(comment)
    print(comment, score)
    time.sleep(1)

# In[222]:

comment_list = ['I will beat you', 'I will fight you', 'Imma whoop yo ass']

for comment in comment_list:
    score = get_toxicity_score(comment)
    print(comment, score)
    time.sleep(1)

# # Analyzing The Results (Conclusion)

# From conducting this analysis, I learned that my initial hypothesis was correct. While scoring the toxicity of Black colloquialisms based on the dataset from Twitter, Google's Perspective API tool tended to demonstrate a stronger language bias towards AAVE. As can be seen in the Visual Inspection portion of my data analysis, each common AAVE phrase from the Black community generated a higher false positive score than non-AAVE phrases conveying similar meanings. For example, it would seem that the terms "curly" and "curly-haired" generate lower toxicity scores than "nappy-headed" when referencing the texture of an individual's hair; "curly" at 0.36 (rounded), "curly-haired" at 0.44, and "nappy-headed" at a score of 0.66. Unsurprisingly, any use of profanity or objectively derogatory racial terms were given a higher rating of toxicity (trend); the n-word got a toxicity score of 0.86 in the first query and the mention of one's posterior resulted in a severe toxicity score of 0.95 (rounded) in the last query. 

# Interestingly enough, the AAVE phrase "Damn straight" does not actually mean something bad; many people in the Black community use it as an expression of confirmation or agreement. And yet, the Perspective API tool gave it a toxic score of 0.64 simply for having the swear word "damn" in it. This might just be a natural language processing issue, but computers tend not to pick up on the meaning or the social context that a phrase or word references. Certain words themselves may have a general reputation for being perceived as bad, but the Perspective API tool fails to factor in that much of what is deemed as toxic depends on who the terminology is being used by and how it is being used. I did not agree with the first query (containing the n-word) being labeled as toxic because I know that it roughly translates in AAVE to "give me a break!" when said in a disbelieving tone and by one Black person to another. However - if this phrase were used in a comment by someone not of the Black community - I would agree with the toxicity level because in that case it would be considered offensive. 
