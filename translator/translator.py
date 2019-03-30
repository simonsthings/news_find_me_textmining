import re

from pymongo import MongoClient

mongo_host = 'server-grapefruit.quving.com'
mongo_port = 27027

client = MongoClient(mongo_host, mongo_port)
db = client.textminer
collection_in = db.noz
collection_out = db.noz_enpy
from googletrans import Translator

translator = Translator()


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    cleantext.replace('&nbsp;', ' ')
    cleantext.replace('&quot;', ' ')

    return cleantext


for doc in collection_in.find():
    content_de = cleanhtml(doc["content"])
    try:
        content_en = translator.translate(content_de).text
        doc["content_en"] = content_en
        doc.pop("_id", None)
        print(collection_out.insert_one(doc))
    except Exception as e:
        print("Something went wrong.")
