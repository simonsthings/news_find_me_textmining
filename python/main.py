import copy

from db_mongo import connect, get_db
from helper import cleanhtml, translate

connect('mongodb://server-grapefruit.quving.com:27027/textminer')
db = get_db()

first_article = db.noz.find_one()
first_article.get('content')

# tranlate first 500 Articles with google translate it and write it to mongo db

count = 0
for article in db.noz.find().limit(500):
    content = article.get('content')
    clean_article = cleanhtml(content)
    translation = translate(clean_article)
    article_en = copy.deepcopy(article)
    article_en['content_en'] = translation
    db.noz_en.update_one(
        article_en,
        {'$set': {'_id': article_en['_id']}},
        upsert=True)
    count += 1
    print(count)
