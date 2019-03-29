import copy
import time

from db_mongo import connect, get_db
from helper import cleanhtml, translate

connect('mongodb://server-grapefruit.quving.com:27027/textminer')
db = get_db()

first_article = db.noz.find_one()
first_article.get('content')

# tranlate first 500 Articles with google translate it and write it to mongo db

repetition = 0
article_count = 303
while True:
    repetition += 1
    try:
        for article in db.noz.find().skip(article_count).limit(2000):
            content = article.get('content')
            clean_article = cleanhtml(content)
            translation = translate(clean_article)
            article_en = copy.deepcopy(article)
            article_en['content_en'] = translation
            db.noz_en.update_one(
                article_en,
                {'$set': {'_id': article_en['_id']}},
                upsert=True)
            print(article_count)
            article_count += 1
    except Exception as e:
        time.sleep(140)
        print("After {} articles, {} occurred again: Starting repetition {}...".format(article_count, e, repetition))
