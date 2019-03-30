import re

# doc1 = "Sugar is bad to consume. My sister likes to have sugar, but not my father."
# doc2 = "My father spends a lot of time driving my sister around to dance practice."
# doc3 = "Doctors suggest that driving may cause increased stress and blood pressure."
# doc4 = "Sometimes I feel pressure to perform well at school, but my father never seems to drive my sister to do better."
# doc5 = "Health experts say that Sugar is not good for your lifestyle."
# 
# # compile documents
# doc_complete = [doc1, doc2, doc3, doc4, doc5]
# doc_complete


from db_mongo import connect, get_db

connect('mongodb://server-grapefruit.quving.com:27027/textminer')
db = get_db()

NUM_DOCUMENTS = 50

content_dict = {}
for article in db.noz_en.find().limit(NUM_DOCUMENTS):
    pattern = re.compile('-\d+')
    key = re.sub(pattern, '', article.get('slug'))
    content = article.get('content_en')
    if content:
        content_dict[key] = content

print(f"Using {len(content_dict.values())} unique documents out of {NUM_DOCUMENTS} total.")

# for headline, content in content_dict.items():
#     print('KEY: '+str(headline))
#     print('CONTENT: '+str(content))
#     print()

doc_complete = [str(doc) for doc in content_dict.values()]
doc_complete

# Cleaning and Preprocessing
from nltk.corpus import stopwords 
from nltk.stem.wordnet import WordNetLemmatizer
import string
stop = set(stopwords.words('english'))
exclude = set(string.punctuation) 
exclude
lemma = WordNetLemmatizer()
def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized

doc_clean = [clean(doc).split() for doc in doc_complete]  
doc_clean
len(doc_clean)

# Preparing Document-Term Matrix

# Importing Gensim
import gensim
from gensim import corpora

# Creating the term dictionary of our courpus, where every unique term is assigned an index. 
dictionary = corpora.Dictionary(doc_clean)
dictionary

# Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]
doc_term_matrix

# Running LDA Model

# Creating the object for LDA model using gensim library
Lda = gensim.models.ldamodel.LdaModel

# Running and Trainign LDA model on the document term matrix.
ldamodel = Lda(doc_term_matrix, num_topics=5, id2word = dictionary, passes=50)


# Results

print(ldamodel.print_topics(num_topics=5, num_words=3))

ldamodel.print_topics(num_topics=-1, num_words=400)


ldamodel.__dict__

ldamodel.get_document_topics()
topics = ldamodel.get_topics()
type(topics)










