

from db_mongo import connect, get_db

connect('mongodb://server-grapefruit.quving.com:27027/textminer')
db = get_db()

first_article = db.noz.find_one()
first_article.get('content')

