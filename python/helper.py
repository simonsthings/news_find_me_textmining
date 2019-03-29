import re
# tranlate first 500 Articles with google translate it and write it to mongo db
from google.cloud import translate


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    cleantext.replace('&nbsp;', ' ')
    cleantext.replace('&quot;', ' ')

    return cleantext


target = 'en'
translate_client = translate.Client()


def translate(text):
    translation = translate_client.translate(
        text,
        target_language=target
    )['translatedText']
    return translation
