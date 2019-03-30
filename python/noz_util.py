#!/usr/bin/env python
# coding: utf-8

# In[9]:


import re, time
from collections import OrderedDict

# Visualisation / Data handling
import pandas as pd
import seaborn as sns

# Cleaning and Preprocessing
from nltk.corpus import stopwords 
from nltk.stem.wordnet import WordNetLemmatizer
import string

# Importing Gensim
import gensim
from gensim import corpora

# database 
from db_mongo import connect, get_db

connect('mongodb://server-grapefruit.quving.com:27027/textminer')
db_cursor = get_db().noz_en.find()

NUM_DOCUMENTS = 5000
NUM_TOPICS = 20
TESTSET_SIZE = 2

def get_texts(db_cursor, num_documents):
    actual_docs_count = 0
    content_dict0 = OrderedDict()
    for article in db_cursor.limit(num_documents):
        actual_docs_count += 1
        pattern = re.compile("-\d+")
        key = re.sub(pattern, '', article.get('slug'))
        content = article.get('content_en')
        if content:
            content_dict0[key] = content

    print(f"Using {len(content_dict0)} unique documents out of {actual_docs_count} total retrieved. ({num_documents} requested)")

    # for headline, content in content_dict0.items():
    #     print('KEY: '+str(headline))
    #     print('CONTENT: '+str(content))
    #     print()
    
    return content_dict0


# In[10]:


def prepare_texts(content_dict0):
    doc_complete = [str(doc) for doc in content_dict0.values()]
    # doc_complete

    stop = set(stopwords.words('english'))
    exclude = set(string.punctuation) 
    # exclude
    lemma = WordNetLemmatizer()
    def clean(doc):
        stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
        punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
        normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
        return normalized

    doc_clean = [clean(doc).split() for doc in doc_complete]  
    # doc_clean
    # len(doc_clean)

    # Preparing Document-Term Matrix

    # Creating the term dictionary of our courpus, where every unique term is assigned an index. 
    dictionary = corpora.Dictionary(doc_clean)
    # dictionary

    # Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]
    # doc_term_matrix

    return doc_complete, doc_clean, dictionary, doc_term_matrix


# In[11]:


content_dict = get_texts(db_cursor, num_documents=NUM_DOCUMENTS)
keys_train = list(content_dict.keys())[:-TESTSET_SIZE]
keys_test = list(content_dict.keys())[-TESTSET_SIZE:]
print(f"{len(keys_train)} docs for training and {len(keys_test)} docs for testing.")


# In[ ]:





# In[ ]:





# In[12]:


list(content_dict.keys())[:3]


# In[13]:


content_dict_train = {k:v for k,v in content_dict.items() if k in keys_train}
doc_complete, doc_clean, dictionary, doc_term_matrix = prepare_texts(content_dict_train)
len(content_dict_train)


# In[14]:


content_dict_test = {k:v for k,v in content_dict.items() if k in keys_test}
doc_complete2, doc_clean2, dictionary2, doc_term_matrix2 = prepare_texts(content_dict_test)
# content_dict_test
len(content_dict_test)


# In[15]:


set(content_dict_train.keys()) & set(content_dict_test.keys())  # should be empty, so no overlap


# In[ ]:





# In[16]:


import time
NUM_TOPICS = 20


# In[17]:


# Running LDA Model
start_time = time.time()
# Creating the object for LDA model using gensim library
Lda = gensim.models.ldamodel.LdaModel

# Running and Trainign LDA model on the document term matrix.
ldamodel = Lda(doc_term_matrix, num_topics=NUM_TOPICS, id2word = dictionary, passes=50)
elapsed_time = time.time() - start_time
print(f"Training the LDA model with {len(doc_term_matrix)} documents took {elapsed_time} seconds.")


# In[18]:


topics = ldamodel.get_topics()

# Results

# print(ldamodel.print_topics(num_topics=5, num_words=3))
# ldamodel.print_topics(num_topics=-1, num_words=400)

for i in range(min(ldamodel.num_topics,3)):
    print(ldamodel.print_topic(i))
#     print()


# In[69]:


# dictionary.id2token


# In[19]:


import pandas as pd
import seaborn as sns


# In[235]:


# df_topics = pd.DataFrame(ldamodel.get_topics())
# df_topics.rename(columns=dictionary.id2token, inplace=True)
# # df_topics['police']
# df_topics


# ## Visualise LDA model:

# In[21]:


# import pyLDAvis
# import pyLDAvis.gensim  # don't skip this
# pyLDAvis.enable_notebook()


# In[236]:


# start_time = time.time()
# vis = pyLDAvis.gensim.prepare(ldamodel, corpus=doc_term_matrix, dictionary=dictionary)
# elapsed_time = time.time() - start_time
# print(f"Visualising the LDA model with {len(doc_term_matrix)} documents took {elapsed_time} seconds.")


# In[23]:


# vis


# In[93]:


def format_topics_sentences(ldamodel, corpus, texts):
    # Init output
    sent_topics_df = pd.DataFrame()

    # Get main topic in each document
    for i, row in enumerate(ldamodel[corpus]):
        # print(row)
        row = sorted(row, key=lambda x: (x[1]), reverse=True)
        # Get the Dominant topic, Perc Contribution and Keywords for each document
        for j, (topic_num, prop_topic) in enumerate(row):
            if j == 0:  # => dominant topic
                wp = ldamodel.show_topic(topic_num)
                topic_keywords = ", ".join([word for word, prop in wp])
                sent_topics_df = sent_topics_df.append(pd.Series([int(topic_num), round(prop_topic,4), topic_keywords]), ignore_index=True)
            else:
                break
    sent_topics_df.columns = ['Dominant_Topic', 'Perc_Contribution', 'Topic_Keywords']

    # Add original text to the end of the output
    contents = pd.Series(texts)
    sent_topics_df = pd.concat([sent_topics_df, contents], axis=1)
    return(sent_topics_df)


# ## Make docs-to-topics mapping:

# In[142]:


def format_all_topics_for_documents(ldamodel, corpus, texts):
    min_prob_backup = ldamodel.minimum_probability
    ldamodel.minimum_probability = 0.0
    # Init output
    props_df = pd.DataFrame(columns=[i for i in range(NUM_TOPICS)], dtype='float64')

    # Get main topic in each document
    for i, row in enumerate(ldamodel[corpus]):
        # print(row)
        row = sorted(row, key=lambda x: (x[1]), reverse=True)
        # Get the Dominant topic, Perc Contribution and Keywords for each document
        for j, (topic_num, prop_topic) in enumerate(row):
            props_df.loc[i, topic_num] = prop_topic
#     props_df.columns = ['Dominant_Topic', 'Perc_Contribution', 'Topic_Keywords']

    column_map = {topic_num: f"Topic {topic_num}" for topic_num in range(NUM_TOPICS)}
    row_map = {doc_num: f"Doc {doc_num}" for doc_num in range(len(topics_df))}
    props_df.rename(column_map, axis='columns', inplace=True)
    props_df.rename(row_map, axis='index', inplace=True)

    ldamodel.minimum_probability = min_prob_backup
    return(props_df)
props_df = format_all_topics_for_documents(ldamodel=ldamodel, corpus=doc_term_matrix, texts=doc_clean)
props_df


# In[121]:


props_df.sum(axis=1).unique()


# In[136]:


props_df.info()


# In[75]:


len(doc_clean)


# In[61]:


ldamodel.show_topic(3)


# In[92]:


def get_topics_prettier(ldamodel, show_percentages=True):
    topics_df = pd.DataFrame()
    probs_df = pd.DataFrame()
    full_df = pd.DataFrame()
    for topic_num in range(NUM_TOPICS):    
        topic_data = ldamodel.show_topic(topic_num)
        for i, (term, prob) in enumerate(topic_data):
            topics_df.loc[i, topic_num] = f"{term}"
            probs_df.loc[i, topic_num] = prob
            full_df.loc[i, topic_num] = f"{term}: {prob*100:.3f}%"
    column_map = {topic_num: f"Topic {topic_num}" for topic_num in range(NUM_TOPICS)}
    row_map = {term_num: f"Term {term_num}" for term_num in range(len(topics_df))}
    topics_df.rename(column_map, axis='columns', inplace=True)
    topics_df.rename(row_map, axis='index', inplace=True)
    probs_df.rename(column_map, axis='columns', inplace=True)
    probs_df.rename(row_map, axis='index', inplace=True)
    full_df.rename(column_map, axis='columns', inplace=True)
    full_df.rename(row_map, axis='index', inplace=True)
    return topics_df, probs_df, full_df
topics_df, probs_df, full_df = get_topics_prettier(ldamodel, show_percentages=True)
topics_df


# In[76]:


# doc_clean[0]


# In[77]:


# doc_complete[0]


# In[78]:


# len(doc_term_matrix)


# In[79]:


# doc_term_matrix


# In[30]:


# whos
min_prob = ldamodel.minimum_probability 
min_prob


# In[48]:


ldamodel.minimum_probability = 0.01


# In[103]:


df_topic_sents_keywords = format_topics_sentences(ldamodel=ldamodel, corpus=doc_term_matrix, texts=doc_clean)
# Format
df_dominant_topic = df_topic_sents_keywords.reset_index()
df_dominant_topic.columns = ['Document_No', 'Dominant_Topic', 'Topic_Perc_Contrib', 'Keywords', 'Text']

# Show
df_dominant_topic.head()


# In[104]:


df_dominant_topic.shape


# In[27]:


ldamodel.__dict__


# In[ ]:





# In[ ]:





# ## PCA (brute force)

# In[196]:


from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


# In[197]:


list(content_dict_train.keys())[:5]


# In[198]:


props_df


# In[199]:





# In[231]:


# x_diff = (x == x_old)
# x_old = x
# x_diff.all()


# In[252]:


# Separating out the features
scaler = StandardScaler()
# Standardizing the features
x = scaler.fit_transform(props_df.values)
# x_df = pd.DataFrame(x)
# x_df
# x_df.sum(axis=1)

# pca = PCA(n_components=2)
pca = PCA()
principalComponents = pca.fit_transform(x)
principal_df = pd.DataFrame(principalComponents)
principal_df


# In[253]:


sns.scatterplot(x=principal_df[0], y=principal_df[1])


# In[270]:


def get_coords_for_text(content_dict_web):
    """
    Parameters
    ==========
    content_dict_test: dict
        mapping from some uuid to the text to be placed in the coord system    
    """
    
    # transform via LDA:
    doc_complete3, doc_clean3, dictionary3, doc_term_matrix3 = prepare_texts(content_dict_web)
    
    props_df = format_all_topics_for_documents(ldamodel=ldamodel, corpus=doc_term_matrix3, texts=doc_clean3)
    
    x = scaler.transform(props_df.values)
    principalComponents = pca.transform(x)  
    principal_df = pd.DataFrame(principalComponents[:,:2], columns=['x','y'])
    return principal_df
    


# In[271]:


content_dict_web = {'my_uuid': 'Albert Pierrepoint (30 March 1905 – 10 July 1992) was an English hangman who executed between 435 and 600 people in a 25-year career that ended in 1956. His first execution was in December 1932, assisting his uncle Thomas. His father Henry had also been a hangman. In October 1941 he undertook his first hanging as lead executioner. During his tenure he hanged 200 people who had been convicted of war crimes in Germany and Austria, as well as several high-profile murderers—including Gordon Cummins (the Blackout Ripper), John Haigh (the Acid Bath Murderer) and John Christie (the Rillington Place Strangler). He undertook several contentious executions, including Timothy Evans, Derek Bentley and Ruth Ellis. He executed William Joyce (also known as Lord Haw-Haw) and John Amery for high treason, and Theodore Schurch for treachery. In the 2005 film Pierrepoint he was portrayed by Timothy Spall. '}
get_coords_for_text(content_dict_web)


# In[272]:


get_coords_for_text(content_dict_test)


# In[ ]:




